"""Emit actual synthetic motor/control observations with reproducible inputs."""
import json
import math
import platform
import sys
from control_lab import Motor,BoundedPID,Sensor,closed_loop


def metrics(rows,dt=.002,switch=4):
    later=[r for r in rows if r['time_s']>=switch]
    return dict(final_speed_rad_s=rows[-1]['speed_rad_s'],
        absolute_error_integral_after_switch_rad=sum(abs(r['speed_rad_s']-2)*dt for r in later),
        max_integral_abs_rad=max(abs(r['integral_rad']) for r in rows),
        saturated_fraction=sum(abs(r['voltage_V'])>=6-1e-12 for r in rows)/len(rows))


def main():
    data={}
    for name,aw,sensor in [('conditional_integration',True,Sensor()),('unbounded_integrator',False,Sensor()),
                            ('delayed_sensor',True,Sensor(delay_steps=100)),
                            ('biased_sensor',True,Sensor(bias=.5)),
                            ('noisy_quantized',True,Sensor(noise_sd=.05,quantum=.1,seed=31))]:
        rows=closed_loop(BoundedPID(1,2,0,anti_windup=aw),sensor=sensor)
        data[name]={'metrics':metrics(rows),'trace_every_50_steps':rows[::50]+[rows[-1]]}
    m=Motor();state=(1.,3.,0.);i,w,_=state;di,dw,_=m.derivative(state,6,.01)
    energy=dict(storage_rate_W=m.inductance*i*di+m.inertia*w*dw,
                electrical_input_W=6*i,copper_loss_W=m.resistance*i*i,
                viscous_loss_W=m.damping*w*w,load_power_W=.01*w)
    convergence=[]
    for dt in [.004,.002,.001]:
        rows=closed_loop(BoundedPID(1,2,0),dt=dt,steps=round(8/dt))
        convergence.append(dict(dt_s=dt,**metrics(rows,dt)))
    print(json.dumps({'kind':'synthetic deterministic ODE/control experiment, no physical measurements',
        'environment':{'python':sys.version,'platform':platform.platform()},'parameters':m.__dict__,
        'protocol':{'dt_s':.002,'duration_s':8,'target_before_4s_rad_s':20,'target_after_rad_s':2,'voltage_limit_V':6,'kp':1,'ki':2,'kd':0},
        'energy_hand_case':energy,'conditions':data,'step_refinement':convergence},indent=2,allow_nan=False))

if __name__=='__main__':main()
