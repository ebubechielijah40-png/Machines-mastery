import cmath
import json
import math
import platform
import sys
from noise import *


def serial(matrix):
    return [[[z.real,z.imag] for z in row] for row in matrix]


def main():
    coherent=pure(math.sqrt(.8),1j*math.sqrt(.2))
    mixture=density(((.8,0),(0,.2)))
    y_basis=((1/math.sqrt(2),-1j/math.sqrt(2)),(1/math.sqrt(2),1j/math.sqrt(2)))
    rows=[]
    for p in [0,.01,.05,.1,.25,.5,.75,1]:
        rho=phase_flip(coherent,p)
        rows.append({'phase_flip_probability':p,'density':serial(rho),'purity':purity(rho),
                     'z_probabilities':z_probabilities(rho),'logical_X_error_probability':logical_error_probability(p),
                     'corrected_logical_density_under_X_noise':serial(corrected_bit_noise(math.sqrt(.8),1j*math.sqrt(.2),p))})
    code=encode(1/math.sqrt(2),1/math.sqrt(2))
    phase=recover(phase_error(code,0))[0]
    print(json.dumps({'kind':'exact synthetic matrix/error-mask calculations; no physical quantum execution',
        'environment':{'python':sys.version,'platform':platform.platform()},
        'controls':{'initial_state':'sqrt(.8)|0>+i sqrt(.2)|1>','noise':'phase flip or independent X per data qubit',
                    'correction':'ideal parity projection and perfect conditional gates, one cycle'},
        'coherent_density':serial(coherent),'same_Z_mixture':serial(mixture),
        'Y_basis_measurement':{'coherent':z_probabilities(channel(coherent,[y_basis])),
            'mixture':z_probabilities(channel(mixture,[y_basis]))},
        'mixture_purity':purity(mixture),'probability_sweep':rows,
        'phase_error_counterexample':{'syndrome':phase[0],'branch_probability':phase[1],
            'overlap_with_original':abs(sum(a.conjugate()*b for a,b in zip(code,phase[2])))**2}},indent=2))

if __name__=='__main__':main()
