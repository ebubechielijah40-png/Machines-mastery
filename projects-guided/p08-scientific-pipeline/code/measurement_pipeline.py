"""Bounded original synthetic measurement analysis with explicit uncertainty model.

A content digest records identity; it does not authenticate data or establish
physical truth. Independent repeatability and a shared calibration component are
assumptions supplied by the experimenter, not facts inferred from the CSV.
"""
from fractions import Fraction
import hashlib
import math
from pathlib import Path
import re

MAX_BYTES=200_000
MAX_ROWS=10_000


def parse_samples(raw):
    if not isinstance(raw,bytes):raise TypeError('CSV input must be immutable bytes')
    if len(raw)>MAX_BYTES:raise ValueError('input byte budget exceeded')
    try:text=raw.decode('ascii')
    except UnicodeError as exc:raise ValueError('restricted ASCII CSV required') from exc
    if not text.endswith('\n'):raise ValueError('complete final row/newline required')
    lines=text.split('\n')
    if lines[0]!='seq,value_milli_c':raise ValueError('exact named/unit header required')
    rows=lines[1:-1]
    if not 2<=len(rows)<=MAX_ROWS:raise ValueError('two to MAX_ROWS observations required')
    values=[]
    for expected,line in enumerate(rows,1):
        cells=line.split(',')
        if len(cells)!=2 or not re.fullmatch(r'[1-9][0-9]{0,4}',cells[0]):raise ValueError('invalid sequence field')
        if int(cells[0])!=expected:raise ValueError('sequence must be contiguous and ordered')
        if re.fullmatch(r'-?(0|[1-9][0-9]{0,5})',cells[1]) is None or cells[1]=='-0':raise ValueError('invalid integer measurement')
        value=int(cells[1])
        if not -50000<=value<=150000:raise ValueError('measurement outside declared range')
        values.append(value)
    return values


def _rational(value):
    return {'numerator':value.numerator,'denominator':value.denominator}


def summarize(raw,*,offset_milli_c=0,calibration_u_milli_c=0):
    for value in [offset_milli_c,calibration_u_milli_c]:
        if type(value) is not int:raise ValueError('calibration parameters must be integer milli-celsius')
    if not -10000<=offset_milli_c<=10000 or not 0<=calibration_u_milli_c<=10000:
        raise ValueError('calibration parameters outside teaching bounds')
    samples=parse_samples(raw);n=len(samples)
    mean=Fraction(sum(samples),n)
    sample_variance=sum((Fraction(x)-mean)**2 for x in samples)/(n-1)
    repeatability_variance=sample_variance/n
    combined_variance=repeatability_variance+calibration_u_milli_c**2
    return {'transform':'independent-mean-plus-shared-offset/v1','input_sha256':hashlib.sha256(raw).hexdigest(),
            'source_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'configuration':{'offset_milli_c':offset_milli_c,'calibration_u_milli_c':calibration_u_milli_c},
            'n':n,'corrected_mean_milli_c':_rational(mean+offset_milli_c),
            'sample_variance_milli_c_squared':_rational(sample_variance),
            'repeatability_variance_of_mean_milli_c_squared':_rational(repeatability_variance),
            'combined_variance_milli_c_squared':_rational(combined_variance),
            'combined_standard_uncertainty_celsius':math.sqrt(float(combined_variance))/1000,
            'assumptions':['independent repeated reading errors under unchanged conditions',
                           'one shared offset estimate independent of repeated reading errors',
                           'calibration standard uncertainty is supplied, not inferred from sample scatter'],
            'physical_measurements_performed':False}


def read_bounded(path):
    with Path(path).open('rb') as stream:return stream.read(MAX_BYTES+1)
