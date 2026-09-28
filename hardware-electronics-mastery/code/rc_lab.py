import math

def rc_charge(v_supply: float, r_ohm: float, c_farad: float, t_sec: float) -> float:
    if r_ohm<=0 or c_farad<=0 or t_sec<0: raise ValueError
    return v_supply*(1-math.exp(-t_sec/(r_ohm*c_farad)))

def time_to_threshold(v_supply,r,c,v_threshold):
    if not 0 < v_threshold < v_supply: raise ValueError
    return -r*c*math.log(1-v_threshold/v_supply)
