"""Original restricted identification; never imports the concealed target.

Normal equations are explicit and intentionally limited by conditioning and
noise in the regressors. This is not a statistical system-identification package.
"""
from dataclasses import dataclass
import math


def finite(value,name):
    if type(value) not in (int,float):raise ValueError(name+' must be numeric')
    try:result=float(value)
    except (ValueError,OverflowError):raise ValueError(name+' must be finite') from None
    if not math.isfinite(result):raise ValueError(name+' must be finite')
    return result


@dataclass(frozen=True)
class Calibration:
    gain:float
    offset:float
    def __post_init__(self):
        if finite(self.gain,'gain')==0:raise ValueError('nonzero gain required')
        finite(self.offset,'offset')
    def coordinate(self,reading):
        result=(finite(reading,'reading')-self.offset)/self.gain
        if not math.isfinite(result):raise ValueError('calibration overflow')
        return result


def calibrate(q0,y0,q1,y1):
    q0,y0,q1,y1=[finite(x,'calibration') for x in (q0,y0,q1,y1)]
    if q0==q1:raise ValueError('distinct calibration coordinates required')
    gain=(y1-y0)/(q1-q0);offset=y0-gain*q0
    return Calibration(gain,offset)


def stiffness(u0,y0,u1,y1,calibration):
    if type(calibration) is not Calibration:raise ValueError('Calibration required')
    delta_u=finite(u1,'drive')-finite(u0,'drive')
    delta_q=calibration.coordinate(y1)-calibration.coordinate(y0)
    if delta_u==0 or delta_q==0:raise ValueError('distinct drive/equilibria required')
    result=delta_u/delta_q
    if not math.isfinite(result) or result<=0:raise ValueError('positive finite stiffness required')
    return result


@dataclass(frozen=True)
class PoleFit:
    decay:float
    frequency:float
    coefficient_a:float
    coefficient_c:float
    residual_rms:float
    gram_separation:float
    def __post_init__(self):
        for name in ('decay','frequency','coefficient_a','coefficient_c','residual_rms','gram_separation'):
            if abs(finite(getattr(self,name),name))>1e6:raise ValueError('fit coefficient budget exceeded')
        if self.decay<0 or self.frequency<=0 or self.coefficient_c>=0 or self.residual_rms<0 or not 0<self.gram_separation<=1:
            raise ValueError('invalid pole fit')


def fit_free(coordinates,dt):
    if type(coordinates) not in (list,tuple) or not 5<=len(coordinates)<=4096:raise ValueError('5..4096 samples required')
    z=[finite(x,'sample') for x in coordinates];dt=finite(dt,'dt')
    if any(abs(x)>1e6 for x in z) or not 1e-5<=dt<=1:raise ValueError('bounded samples/dt required')
    scale=max(abs(x) for x in z)
    if scale==0:raise ValueError('zero response cannot identify poles')
    z=[x/scale for x in z]
    xx=math.fsum(x*x for x in z[1:-1]);yy=math.fsum(y*y for y in z[:-2])
    xy=math.fsum(x*y for x,y in zip(z[1:-1],z[:-2]))
    xr=math.fsum(x*r for x,r in zip(z[1:-1],z[2:]));yr=math.fsum(y*r for y,r in zip(z[:-2],z[2:]))
    determinant=xx*yy-xy*xy;separation=determinant/(xx*yy) if xx*yy else 0
    if separation<=1e-12:raise ValueError('rank-deficient or unresolved probe')
    a=(xr*yy-yr*xy)/determinant;c=(yr*xx-xr*xy)/determinant
    if c>=0:raise ValueError('outside conjugate pole model')
    radius=math.sqrt(-c)
    if not 0<radius<=1+1e-10:raise ValueError('outside non-growing model')
    cosine=a/(2*radius)
    if not -1<cosine<1:raise ValueError('outside strictly underdamped principal band')
    decay=max(0.,-math.log(radius)/dt);frequency=math.acos(cosine)/dt
    residual=scale*math.sqrt(math.fsum((r-a*x-c*y)**2 for r,x,y in zip(z[2:],z[1:-1],z[:-2]))/(len(z)-2))
    return PoleFit(decay,frequency,a,c,residual,separation)


@dataclass(frozen=True)
class Model:
    inertia:float
    loss:float
    stiffness:float
    def __post_init__(self):
        for name in ('inertia','loss','stiffness'):
            if not 0<=finite(getattr(self,name),name)<=1e12:raise ValueError('coefficient outside budget')
        if self.inertia<1e-12 or self.stiffness<1e-12 or self.loss**2>=4*self.inertia*self.stiffness:raise ValueError('positive underdamped model required')
    def response(self,t,coordinate=0.,velocity=0.,drive=0.):
        t,coordinate,velocity,drive=[finite(x,'response') for x in (t,coordinate,velocity,drive)]
        if not 0<=t<=60:raise ValueError('response time0..60 required')
        alpha=self.loss/(2*self.inertia);omega=math.sqrt(self.stiffness/self.inertia-alpha*alpha)
        equilibrium=drive/self.stiffness;cosine=coordinate-equilibrium;sine=(velocity+alpha*cosine)/omega
        result=equilibrium+math.exp(-alpha*t)*(cosine*math.cos(omega*t)+sine*math.sin(omega*t))
        if not math.isfinite(result):raise ValueError('response overflow')
        return result


def model_from_fit(fit,k):
    if type(fit) is not PoleFit:raise ValueError('PoleFit required')
    k=finite(k,'stiffness')
    if k<=0:raise ValueError('positive stiffness required')
    inertia=k/(fit.decay**2+fit.frequency**2)
    return Model(inertia,2*fit.decay*inertia,k)
