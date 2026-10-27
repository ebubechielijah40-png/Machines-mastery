"""Execute original deterministic linear sensitivity and update experiments."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import json
import math
from pathlib import Path
import platform
import sys

from discrete import extended_gcd, modular_power
from linear import gradient_steps, matmul, matvec, solve


def run():
    z=2-1j
    angle=math.pi/4
    rotated=z*complex(math.cos(angle),math.sin(angle))
    sensitivity=[]
    epsilon=1e-7
    for delta in [1e-1,1e-3,1e-6,1e-9]:
        a=[[1.,1.],[1.,1.+delta]]
        original_b=matvec(a,[1.,1.])
        perturbed_b=[original_b[0],original_b[1]+epsilon]
        x=solve(a,perturbed_b)
        residual=[v-b for v,b in zip(matvec(a,x),perturbed_b)]
        sensitivity.append({
            'delta':delta,'epsilon_requested':epsilon,'actual_b':perturbed_b,
            'actual_matrix':a,'solution':x,
            'ideal_real_solution':[1-epsilon/delta,1+epsilon/delta],
            'perturbed_residual_inf':max(map(abs,residual)),
            'distance_from_original_solution_inf':max(abs(v-1) for v in x)})
    traces=[{'learning_rate':rate,
             'history':gradient_steps([[1.,0.],[0.,2.]],[0.,0.],[1.,1.],rate,30)}
            for rate in [.1,.4,.5,.6]]
    quadrature=[]
    for n in [4,8,16,32,64]:
        area=math.fsum([(0.+1.)/2]+[(k/n)**2 for k in range(1,n)])/n
        quadrature.append({'panels':n,'area':area,'float_error':area-1/3,
                           'exact_quadratic_error':str(Fraction(1,6*n*n))})
    return {'schema_version':1,'kind':'executed deterministic mathematical experiments',
            'executed_utc':datetime.now(timezone.utc).isoformat(),
            'python':sys.version,'platform':platform.platform(),
            'randomness':'none','complex_rotation':{
                'z':[z.real,z.imag],'phase_angle_radians':angle,
                'complex_product':[rotated.real,rotated.imag],
                'real_equations':[z.real*math.cos(angle)-z.imag*math.sin(angle),
                                  z.real*math.sin(angle)+z.imag*math.cos(angle)],
                'squared_modulus_before':abs(z)**2,
                'squared_modulus_after':abs(rotated)**2},
            'composition':{
                'BA':matmul([[1,0],[-1,1]],[[2,1],[0,3]]),
                'B_A_x':matvec([[1,0],[-1,1]],matvec([[2,1],[0,3]],[2,1]))},
            'sensitivity':sensitivity,'gradient_stability':traces,
            'trapezoid':quadrature,
            'exact_integer_examples':{'gcd_bezout_84_30':extended_gcd(84,30),
                                      '3_power_13_mod_17':modular_power(3,13,17)},
            'limits':['Floating coefficients are rounded representations of the stated decimal model.',
                      'A small residual does not prove measurement accuracy or small forward error.',
                      'The diagonal quadratic is not a neural-network benchmark.',
                      'No physical measurements or timing performance claims.']}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=json.dumps(run(),indent=2,allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(result,encoding='utf-8')
    else:
        print(result,end='')
