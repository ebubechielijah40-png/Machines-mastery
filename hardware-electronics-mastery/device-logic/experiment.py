"""Actual synthetic device/timing experiments; parameters are not a datasheet."""
import hashlib,json,platform,sys
from datetime import datetime,timezone
from pathlib import Path
from devices import carriers,conductivity,resistor_load_dc,transient,timing_slacks


def crossing(trace,level,rising):
    for a,b in zip(trace,trace[1:]):
        if (a['output_V']<level<=b['output_V']) if rising else (a['output_V']>level>=b['output_V']):
            return a['t_s']+(b['t_s']-a['t_s'])*(level-a['output_V'])/(b['output_V']-a['output_V'])
    return None


def run():
    carrier_rows=[]
    for nd,na in ((0,0),(1e18,0),(1e20,0),(1e22,0),(1e22,1e22),(0,1e22)):
        c=carriers(1e16,nd,na)
        carrier_rows.append(dict(donors_per_m3=nd,acceptors_per_m3=na,**c,
                                conductivity_S_per_m=conductivity(*c.values(),.1,.05)))
    dc=[dict(input_V=i/10,**resistor_load_dc(i/10,5,10000,.001,1)) for i in range(51)]
    low=dc[-1]['output_V'];transients=[]
    for dt in (2e-10,1e-10,5e-11):
        for gate,v0,rising in ((0,low,True),(5,5,False)):
            result=transient(gate,v0,5,10000,1e-11,.001,1,dt,round(300e-9/dt))
            transients.append({'input_V':gate,'step_s':dt,'half_supply_crossing_s':crossing(result['trace'],2.5,rising),
                               'final_V':result['trace'][-1]['output_V'],'energy':result['energy'],
                               'sampled_trace':result['trace'][::max(1,len(result['trace'])//100)]+[result['trace'][-1]]})
    bad_step=None
    try:transient(0,0,5,10000,1e-11,.001,1,1e-6,1)
    except ValueError as exc:bad_step=str(exc)
    timing=[]
    for period,skew in ((10e-9,0),(10e-9,.2e-9),(100e-9,.2e-9),(6e-9,0)):
        timing.append(dict(period_s=period,capture_minus_launch_skew_s=skew,**timing_slacks(period,.2e-9,1e-9,.3e-9,5e-9,1e-9,.4e-9,skew)))
    return {'executed_at_utc':datetime.now(timezone.utc).isoformat(),'kind':'actual execution of assumed semiconductor/circuit/timing models; no physical device measurement',
            'python':sys.version,'platform':platform.platform(),'code_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),Path(__file__).with_name('devices.py'))},
            'assumptions':{'intrinsic_per_m3':1e16,'mobility_n_m2_per_Vs':.1,'mobility_p_m2_per_Vs':.05,
                           'supply_V':5,'pullup_ohm':10000,'load_F':1e-11,'beta_A_per_V2':.001,'threshold_V':1},
            'carrier_rows':carrier_rows,'dc_transfer':dc,'transients':transients,'rejected_step':bad_step,'timing':timing,
            'limits':'No junction-Poisson solution, subthreshold leakage, body effect, velocity saturation, physical timing or metastability simulation. Assumed clocks and ideal rail-valued switches only.'}

if __name__=='__main__':print(json.dumps(run(),indent=2))
