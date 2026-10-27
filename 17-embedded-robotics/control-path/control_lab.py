"""Original SI-unit DC motor and sampled controller models, not hardware firmware.

The voltage source and load torque are constant within each RK4 step. Parameters
are hypothetical. Kt=Ke=k is imposed so electromechanical energy conversion agrees
in coherent SI units. RK4 is explicit, without adaptive error/stability control.
"""
from collections import deque
from dataclasses import dataclass
import math
import random


def finite(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(name+' must be a finite real number')
    return float(x)


@dataclass(frozen=True)
class Motor:
    inertia: float = .02       # kg m^2
    damping: float = .02       # N m s / rad
    resistance: float = 2.0    # ohm
    inductance: float = .02    # H
    k: float = .1             # N m/A, numerically V s/rad in coherent SI

    def __post_init__(self):
        for name in ['inertia', 'resistance', 'inductance']:
            if finite(getattr(self,name),name) <= 0: raise ValueError(name+' must be positive')
        for name in ['damping','k']:
            if finite(getattr(self,name),name) < 0: raise ValueError(name+' must be nonnegative')

    def derivative(self, state, voltage, load=0.0):
        current, speed, angle = state
        return ((voltage-self.resistance*current-self.k*speed)/self.inductance,
                (self.k*current-self.damping*speed-load)/self.inertia, speed)

    def energy(self, state):
        current,speed,_=state
        return .5*self.inductance*current*current+.5*self.inertia*speed*speed

    def step(self, state, voltage, dt, load=0.0):
        if len(state) != 3: raise ValueError('state is (current A, speed rad/s, angle rad)')
        state=tuple(finite(x,'state') for x in state)
        voltage,dt,load=(finite(x,n) for x,n in [(voltage,'voltage'),(dt,'dt'),(load,'load')])
        if dt <= 0: raise ValueError('dt must be positive')
        def slope(x):return self.derivative(x,voltage,load)
        def add(x,k,factor):return tuple(a+factor*b for a,b in zip(x,k))
        a=slope(state);b=slope(add(state,a,dt/2));c=slope(add(state,b,dt/2));d=slope(add(state,c,dt))
        result=tuple(x+dt*(aa+2*bb+2*cc+dd)/6 for x,aa,bb,cc,dd in zip(state,a,b,c,d))
        return tuple(finite(x,'integrated state') for x in result)


@dataclass
class BoundedPID:
    kp: float
    ki: float
    kd: float
    limit: float = 6.0
    anti_windup: bool = True
    derivative_tau: float = .01
    integral: float = 0.0
    previous_measurement: float | None = None
    filtered_derivative: float = 0.0

    def __post_init__(self):
        for name in ['kp','ki','kd','derivative_tau']:
            if finite(getattr(self,name),name) < 0: raise ValueError(name+' must be nonnegative')
        if finite(self.limit,'limit') <= 0: raise ValueError('limit must be positive')
        finite(self.integral,'integral')

    def step(self, target, measurement, dt):
        target,measurement,dt=(finite(x,n) for x,n in [(target,'target'),(measurement,'measurement'),(dt,'dt')])
        if dt <= 0: raise ValueError('dt must be positive')
        error=target-measurement
        raw_derivative=0.0 if self.previous_measurement is None else -(measurement-self.previous_measurement)/dt
        derivative=self.filtered_derivative+dt/(self.derivative_tau+dt)*(raw_derivative-self.filtered_derivative)
        candidate=self.integral+error*dt
        proposed=self.kp*error+self.ki*candidate+self.kd*derivative
        outward=(proposed>self.limit and self.ki*error>0) or (proposed < -self.limit and self.ki*error<0)
        integral=self.integral if self.anti_windup and outward else candidate
        command=self.kp*error+self.ki*integral+self.kd*derivative
        # Validate before mutating controller memory, including overflow.
        for x in [integral,derivative,command]: finite(x,'controller intermediate')
        self.integral=integral;self.filtered_derivative=derivative;self.previous_measurement=measurement
        return max(-self.limit,min(self.limit,command))


class Sensor:
    def __init__(self, delay_steps=0, bias=0.0, noise_sd=0.0, quantum=0.0, seed=0):
        if type(delay_steps) is not int or not 0 <= delay_steps <= 100_000:
            raise ValueError('delay_steps must be an integer from0 through100000')
        self.bias=finite(bias,'bias');self.noise_sd=finite(noise_sd,'noise_sd');self.quantum=finite(quantum,'quantum')
        if self.noise_sd<0 or self.quantum<0:raise ValueError('noise and quantum must be nonnegative')
        self.delay_steps=delay_steps;self.queue=deque();self.rng=random.Random(seed)

    def read(self, value):
        value=finite(value,'sensor input')
        sample=value+self.bias+self.rng.gauss(0,self.noise_sd)
        if self.quantum:sample=round(sample/self.quantum)*self.quantum
        if not self.queue:
            self.queue.extend([sample]*self.delay_steps)  # initial sample held for prehistory
        self.queue.append(sample)
        return self.queue.popleft()


def reflected_inertia(load_inertia, ratio):
    load_inertia,ratio=finite(load_inertia,'load inertia'),finite(ratio,'ratio')
    if load_inertia<0 or ratio<=0:raise ValueError('nonnegative inertia and positive ratio required')
    return load_inertia/ratio/ratio


def closed_loop(controller, motor=None, sensor=None, dt=.002, steps=4000, switch_time=4.0):
    if type(steps) is not int or not 1<=steps<=1_000_000:raise ValueError('bounded positive steps required')
    if finite(dt,'dt')<=0:raise ValueError('dt must be positive')
    finite(switch_time,'switch time')
    motor=motor or Motor();sensor=sensor or Sensor();state=(0.0,0.0,0.0);records=[]
    for index in range(steps):
        t=index*dt;target=20.0 if t<switch_time else 2.0
        measurement=sensor.read(state[1]);voltage=controller.step(target,measurement,dt)
        records.append(dict(time_s=t,target_rad_s=target,current_A=state[0],speed_rad_s=state[1],
                            measurement_rad_s=measurement,voltage_V=voltage,integral_rad=controller.integral))
        state=motor.step(state,voltage,dt)
    return records
