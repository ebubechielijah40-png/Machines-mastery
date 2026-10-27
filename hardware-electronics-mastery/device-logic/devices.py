"""Explicit ideal low-field/long-channel teaching models, SI units throughout."""
from dataclasses import dataclass
import math

Q = 1.602176634e-19  # exact elementary charge in coulombs (SI definition)


def finite(v, name='value', *, positive=False, nonnegative=False):
    if type(v) not in (int, float): raise ValueError(f'{name}: real scalar required')
    try: v=float(v)
    except (OverflowError, ValueError): raise ValueError(f'{name}: unrepresentable') from None
    if not math.isfinite(v) or (positive and v<=0) or (nonnegative and v<0):
        raise ValueError(f'{name}: outside finite range')
    return v


def carriers(intrinsic_per_m3, donors_per_m3=0, acceptors_per_m3=0):
    ni=finite(intrinsic_per_m3,'ni',positive=True)
    nd=finite(donors_per_m3,'donors',nonnegative=True)
    na=finite(acceptors_per_m3,'acceptors',nonnegative=True)
    if max(ni,nd,na)>1e25: raise ValueError('outside declared numerical concentration envelope')
    d=nd-na
    majority=.5*abs(d)+.5*math.hypot(d,2*ni)
    minority=ni*(ni/majority)  # avoids subtracting almost equal roots
    n,p=(majority,minority) if d>=0 else (minority,majority)
    return {'electrons_per_m3':finite(n,positive=True),'holes_per_m3':finite(p,positive=True)}


def conductivity(n,p,mobility_n,mobility_p):
    n,p,mn,mp=(finite(v,positive=True) for v in (n,p,mobility_n,mobility_p))
    return finite(Q*(n*mn+p*mp),'conductivity_S_per_m',positive=True)


def nmos_current(vgs,vds,beta,threshold):
    vg=finite(vgs,'vgs'); vd=finite(vds,'vds',nonnegative=True)
    b=finite(beta,'beta',positive=True); vt=finite(threshold,'threshold',positive=True)
    over=vg-vt
    if over<=0: return 0.0
    if vd<over: result=b*vd*(over-.5*vd)
    else: result=.5*b*over*over
    return finite(result,'current_A',nonnegative=True)


def resistor_load_dc(vin,vdd,resistance,beta,threshold):
    supply=finite(vdd,'vdd',positive=True);r=finite(resistance,'R',positive=True)
    v=finite(vin,'vin')
    # Validate device parameters even for an endpoint answer.
    nmos_current(v,0,beta,threshold)
    lo,hi=0.0,supply
    for _ in range(80):
        mid=(lo+hi)/2
        net=(supply-mid)/r-nmos_current(v,mid,beta,threshold)
        if net>0: lo=mid
        else: hi=mid
    out=(lo+hi)/2
    current=finite((supply-out)/r,nonnegative=True)
    return {'output_V':out,'supply_current_A':current,'supply_power_W':finite(supply*current,nonnegative=True)}


def transient(vin,v0,vdd,resistance,capacitance,beta,threshold,step_s,steps):
    v=finite(v0,'v0',nonnegative=True);supply=finite(vdd,'vdd',positive=True)
    r=finite(resistance,'R',positive=True);c=finite(capacitance,'C',positive=True)
    dt=finite(step_s,'step',positive=True);gate=finite(vin,'vin')
    if v>supply or type(steps) is not int or not 1<=steps<=100000:
        raise ValueError('initial voltage/step count outside envelope')
    nmos_current(gate,0,beta,threshold)
    initial=v;energy_in=heat_r=heat_m=quadratic_error=0.0
    trace=[{'t_s':0.0,'output_V':v}]
    for i in range(steps):
        ir=finite((supply-v)/r);im=nmos_current(gate,v,beta,threshold)
        dv=finite(dt*(ir-im)/c)
        next_v=finite(v+dv)
        if not 0<=next_v<=supply:
            raise ValueError('Euler voltage left rails: reduce step; no clipping is performed')
        energy_in+=supply*ir*dt;heat_r+=ir*ir*r*dt;heat_m+=v*im*dt
        quadratic_error+=.5*c*dv*dv
        v=next_v;trace.append({'t_s':(i+1)*dt,'output_V':v})
    stored_change=.5*c*(v*v-initial*initial)
    return {'trace':trace,'energy':{'supply_J':finite(energy_in),'resistor_heat_J':finite(heat_r),
            'mos_heat_J':finite(heat_m),'capacitor_change_J':finite(stored_change),
            'balance_residual_J':finite(energy_in-heat_r-heat_m-stored_change),
            'predicted_euler_residual_J':finite(-quadratic_error)}}


def gate_network(kind,a,b):
    if kind not in ('nand','nor') or type(a) is not int or type(b) is not int or a not in (0,1) or b not in (0,1):
        raise ValueError('two binary inputs and nand/nor kind required')
    # Ideal complementary switch networks: true means a conducting path.
    if kind=='nand': down=bool(a and b); up=bool((not a) or (not b))
    else: down=bool(a or b); up=bool((not a) and (not b))
    if up==down: raise ValueError('floating or contending network')
    return int(up)


def timing_slacks(period_s,cq_min_s,cq_max_s,logic_min_s,logic_max_s,setup_s,hold_s,skew_s=0,uncertainty_s=0):
    period=finite(period_s,'period',positive=True)
    qmin,qmax,dmin,dmax,setup,hold,u=(finite(v,nonnegative=True) for v in
        (cq_min_s,cq_max_s,logic_min_s,logic_max_s,setup_s,hold_s,uncertainty_s))
    skew=finite(skew_s,'capture minus launch skew')
    if qmax<qmin or dmax<dmin:raise ValueError('minimum delay cannot exceed maximum')
    return {'setup_slack_s':finite(period+skew-u-qmax-dmax-setup),
            'hold_slack_s':finite(qmin+dmin-skew-u-hold),
            'minimum_period_s':finite(qmax+dmax+setup+u-skew)}


def ripple_add(a,b,width):
    if type(width) is not int or not 1<=width<=32:raise ValueError('width in [1,32] required')
    if type(a) is not int or type(b) is not int or not 0<=a<1<<width or not 0<=b<1<<width:
        raise ValueError('unsigned inputs outside width')
    carry=0;out=0
    for bit in range(width):
        x=(a>>bit)&1;y=(b>>bit)&1
        out|=(x^y^carry)<<bit
        carry=(x&y)|(x&carry)|(y&carry)
    return out,carry
