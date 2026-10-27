"""Synthetic FFT mechanism/cost experiment; never an IBM7094 reproduction."""
import json
import math
import platform
import random
import statistics
import sys
import time
from fourier import direct_dft,fft_counted


def main():
    rng=random.Random(1965);rows=[]
    for n in [8,16,32,64,128,256]:
        data=[complex(rng.random(),rng.random()) for _ in range(n)]
        direct=direct_dft(data);fast,counts=fft_counted(data)
        timing={}
        for label,function in [('direct',direct_dft),('radix2',lambda data:fft_counted(data)[0])]:
            samples=[]
            for _ in range(5):
                start=time.perf_counter_ns();function(data);samples.append(time.perf_counter_ns()-start)
            timing[label]={'median_ns':statistics.median(samples),'all_samples_ns':samples}
        rows.append({'n':n,'max_absolute_error':max(abs(a-b) for a,b in zip(direct,fast)),
                     'direct_value_multiplications':n*n,'radix2_counts':counts,'elapsed':timing})
    print(json.dumps({'kind':'original synthetic complex-input experiment; no historical runtime reproduction',
        'environment':{'python':sys.version,'platform':platform.platform()},'seed':1965,'repetitions':5,
        'rows':rows,'limitations':['Python/runtime/root-generation costs differ from the paper operation model',
        'direct definition and FFT have different roundoff order; no uniform error guarantee',
        'only powers of two and small arrays tested; no IBM7094 hardware or source program']},indent=2))


if __name__=='__main__':main()
