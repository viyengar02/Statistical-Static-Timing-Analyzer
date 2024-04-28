import math
from scipy.integrate import quad
from scipy.special import erf, erfc
SMALLPHI_COEFF = 1 / math.sqrt(2 * math.pi)


def variance(values):
    total = sum(values)
    num_values = len(values)
    mean = total / num_values

    variance = sum((val - mean) ** 2 for val in values) / num_values

    return variance

def sigma(a):
    return math.sqrt(a.a[1] ** 2 + a.a[2] ** 2 + a.a[3] ** 2)

def rho(a, b, sigmaA, sigmaB):
    return ((a.a[1] * b.a[1]) + (a.a[2] * b.a[2])) / (sigmaA * sigmaB)

def theta(sigmaA, sigmaB, rho):
    return math.sqrt(sigmaA ** 2 + sigmaB ** 2 - 2 * sigmaA * sigmaB * rho)

def bigphi(y):
    if y < 0:
        return 0.5 * erfc(abs(y) / math.sqrt(2))
    else:
        return 0.5 + 0.5 * erf(y / math.sqrt(2))
    
def smallphi(x):
    return SMALLPHI_COEFF * math.exp(-(x ** 2) / 2)

def maxmean(a, b, bigphi, theta, smallphi):
    return a.a[0] * bigphi + b.a[0] * (1.0 - bigphi) + theta * smallphi

def minmean(a, b, bigphi, theta, smallphi):
    return a.a[0] * (1.0 - bigphi) + b.a[0] * bigphi - theta * smallphi

def maxvariance(a, b, sigmaA, sigmaB, theta, bigphi, smallphi, mean):
    return (sigmaA ** 2 + a.a[0] ** 2) * bigphi + (sigmaB ** 2 + b.a[0] ** 2) * (1.0 - bigphi) + (a.a[0] + b.a[0]) * theta * smallphi - mean ** 2

def minvariance(a, b, sigmaA, sigmaB, theta, bigphi, smallphi, mean):
    return (sigmaA ** 2 + a.a[0] ** 2) * (1.0 - bigphi) + (sigmaB ** 2 + b.a[0] ** 2) * bigphi - (a.a[0] + b.a[0]) * theta * smallphi - mean ** 2

def max_Obj(a, b):
    sigmaA = sigma(a)
    sigmaB = sigma(b)
    _rho = rho(a, b, sigmaA, sigmaB)
    _theta = theta(sigmaA, sigmaB, _rho)
    x = 0  # placeholder for calc_x function
    _bigphi = bigphi(x)
    _smallphi = smallphi(x)
    mean = maxmean(a, b, _bigphi, _theta, _smallphi)
    variance = maxvariance(a, b, sigmaA, sigmaB, _theta, _bigphi, _smallphi, mean)
    
    g = Wire()
    g.a[0] = mean
    g.a[1] = a.a[1] * _bigphi + b.a[1] * (1.0 - _bigphi)
    g.a[2] = a.a[2] * _bigphi + b.a[2] * (1.0 - _bigphi)
    tmp = variance - (g.a[1] ** 2) - (g.a[2] ** 2)
    if tmp < 0:
        print("Error: max function cannot take square root of a negative value!", tmp)
        exit(-1)
    g.a[3] = math.sqrt(tmp)
    return g

def minObj(a, b):
    sigmaA = sigma(a)
    sigmaB = sigma(b)
    _rho = rho(a, b, sigmaA, sigmaB)
    _theta = theta(sigmaA, sigmaB, _rho)
    x = 0  # placeholder for calc_x function
    _bigphi = bigphi(x)
    _smallphi = smallphi(x)
    mean = minmean(a, b, _bigphi, _theta, _smallphi)
    variance = minvariance(a, b, sigmaA, sigmaB, _theta, _bigphi, _smallphi, mean)
    
    g = Wire()
    g.a[0] = mean
    g.a[1] = a.a[1] * (1.0 - _bigphi) + b.a[1] * _bigphi
    g.a[2] = a.a[2] * (1.0 - _bigphi) + b.a[2] * _bigphi
    g.a[3] = math.sqrt(variance - (g.a[1] ** 2) - (g.a[2] ** 2))
    return g
