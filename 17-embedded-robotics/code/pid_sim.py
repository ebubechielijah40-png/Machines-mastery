from dataclasses import dataclass
@dataclass
class PID:
    kp:float; ki:float; kd:float; integ:float=0.0; prev:float=0.0
    def step(self,error,dt):
        if dt<=0: raise ValueError
        self.integ += error*dt
        deriv=(error-self.prev)/dt
        self.prev=error
        return self.kp*error+self.ki*self.integ+self.kd*deriv

def simulate(controller, target=1.0, dt=.01, steps=1000, damping=.4):
    x=v=0.0; out=[]
    for _ in range(steps):
        u=controller.step(target-x,dt)
        a=u-damping*v
        v += a*dt; x += v*dt; out.append(x)
    return out
