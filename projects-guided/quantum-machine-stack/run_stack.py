"""Bounded ideal vector -> density -> synthetic noise -> ideal recovery path."""
import hashlib
import json
import math
import platform
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
for relative in ['20-quantum-computing/code','20-quantum-computing/noise-correction']:
    sys.path.insert(0,str(ROOT/relative))
import simulator
import noise


def serial(a):return [[[z.real,z.imag] for z in row] for row in a]


def build_report():
    a,b=math.sqrt(.8),1j*math.sqrt(.2)
    state=simulator.State.from_amplitudes([a,b]);state.apply1(0,simulator.H)
    density_from_vector=noise.pure(*state.amp)
    density_by_gate=noise.channel(noise.pure(a,b),[noise.H])
    residual=max(abs(density_from_vector[i][j]-density_by_gate[i][j]) for i in range(2) for j in range(2))
    encoded=noise.encode(a,b)
    syndrome,prob,restored=noise.recover(noise.flip_mask(encoded,2))[0]
    files=[Path(__file__),Path(simulator.__file__),Path(noise.__file__)]
    return {'scope':'ideal/synthetic software mechanisms; no native compilation, pulse/device job or advantage claim',
            'environment':{'python':sys.version,'platform':platform.platform()},
            'implementation_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
            'vector_gate_probabilities':state.probs(),'density_after_gate':serial(density_by_gate),
            'vector_density_residual':residual,
            'noise':{'phase_flip_probability':.5,'output_density':serial(noise.phase_flip(noise.pure(a,b),.5)),
                     'output_purity':noise.purity(noise.phase_flip(noise.pure(a,b),.5))},
            'recovery':{'injected_mask':2,'syndrome':syndrome,'branch_probability':prob,
                        'overlap_squared':abs(sum(x.conjugate()*y for x,y in zip(encoded,restored)))**2,
                        'independent_X_probability':.1,'logical_X_probability':noise.logical_error_probability(.1)}}

if __name__=='__main__':print(json.dumps(build_report(),indent=2))
