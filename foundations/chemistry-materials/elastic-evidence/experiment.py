"""Controlled synthetic measurements, never a physical tensile experiment."""
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
import platform
from pathlib import Path
import random
import sys
from materials import BondLaw, Bar, fit_extension, infer_modulus, infer_two_lengths


def run():
    bond = BondLaw(1e-19, 2e-10, 8)
    bond_trace = []
    for ratio in (.98,.99,1,1.01,1.02,1.1,1.25,1.5,2):
        r = ratio*bond.spacing_m
        bond_trace.append(dict(ratio=ratio, energy_J=bond.energy_J(r),
                               required_force_N=bond.required_force_N(r),
                               tangent_N_per_m=bond.tangent_N_per_m(r)))
    area, modulus, frame, offset = 1e-6, 200e9, 1e-7, 2e-6
    forces = list(range(0, 101, 10)); rng = random.Random(421)
    specimens = []
    for length in (.1,.2):
        bar = Bar(length,area,modulus)
        measured = [bar.response(f)['extension_m']+frame*f+offset+rng.uniform(-5e-8,5e-8) for f in forces]
        fit = fit_extension(forces, measured)
        wrong_origin = sum(f*y for f,y in zip(forces,measured))/sum(f*f for f in forces)
        specimens.append(dict(length_m=length,forces_N=forces,observed_extensions_m=measured,
                              fit=asdict(fit),apparent_modulus_Pa=infer_modulus(length,area,fit.slope_m_per_N),
                              corrected_known_frame_modulus_Pa=infer_modulus(length,area,fit.slope_m_per_N,frame),
                              wrong_forced_origin_modulus_Pa=infer_modulus(length,area,wrong_origin)))
    combined = infer_two_lengths(.1,specimens[0]['fit']['slope_m_per_N'],.2,specimens[1]['fit']['slope_m_per_N'],area)
    pairs = [{'modulus_Pa':200e9,'frame_compliance_m_per_N':1e-7},
             {'modulus_Pa':250e9,'frame_compliance_m_per_N':2e-7}]
    for pair in pairs:
        pair['identical_single_length_total_compliance_m_per_N'] = .1/area/pair['modulus_Pa']+pair['frame_compliance_m_per_N']
    return {'executed_at_utc':datetime.now(timezone.utc).isoformat(),'kind':'actual execution of synthetic models; no physical measurements',
            'python':sys.version,'platform':platform.platform(),'code_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),Path(__file__).with_name('materials.py'))},
            'assumed_parameters':dict(area_m2=area,modulus_Pa=modulus,frame_compliance_m_per_N=frame,offset_m=offset,noise_halfwidth_m=5e-8,seed=421),
            'bond_assumed_parameters':asdict(bond),'bond_trace':bond_trace,
            'bond_force_peak_separation_ratio':bond.force_peak_separation_m()/bond.spacing_m,
            'ideal_parallel_chain_modulus_Pa':bond.ideal_chain_modulus_Pa(),
            'specimens':specimens,'two_length_estimate':combined,'nonidentifiable_parameter_pairs':pairs,
            'limits':'Illustrative energy law, parallel-chain geometry and linear constant-frame model; no calibrated material, fracture, fatigue, creep, thermal expansion or fixture validation.'}

if __name__ == '__main__': print(json.dumps(run(),indent=2))
