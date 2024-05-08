import math
from scipy.integrate import quad
from scipy.special import erf, erfc
from wire import *
SMALLPHI_COEFF = 1 / math.sqrt(2 * math.pi)


def variance(values):
    total = sum(values)
    num_values = len(values)
    mean = total / num_values

    variance = sum((val - mean) ** 2 for val in values) / num_values

    return variance

def sigma(a):
    return math.sqrt(a.a1 ** 2 + a.a2 ** 2 + a.a3 ** 2)

def rho(a, b, sigmaA, sigmaB):
    return ((a.a1 * b.a1) + (a.a2 * b.a2)) / (sigmaA * sigmaB)

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
    return a.a0 * bigphi + b.a0 * (1.0 - bigphi) + theta * smallphi

def minmean(a, b, bigphi, theta, smallphi):
    return a.a0 * (1.0 - bigphi) + b.a0 * bigphi - theta * smallphi

def maxvariance(a, b, sigmaA, sigmaB, theta, bigphi, smallphi, mean):
    return (sigmaA ** 2 + a.a0 ** 2) * bigphi + (sigmaB ** 2 + b.a0 ** 2) * (1.0 - bigphi) + (a.a0 + b.a0) * theta * smallphi - mean ** 2

def minvariance(a, b, sigmaA, sigmaB, theta, bigphi, smallphi, mean):
    return (sigmaA ** 2 + a.a0 ** 2) * (1.0 - bigphi) + (sigmaB ** 2 + b.a0 ** 2) * bigphi - (a.a0 + b.a0) * theta * smallphi - mean ** 2

def max_Obj(a, b):
    sigmaA = sigma(a)
    sigmaB = sigma(b)
    _rho = rho(a, b, sigmaA, sigmaB)
    _theta = theta(sigmaA, sigmaB, _rho)
    x = (a.a0-b.a0)/_theta  
    _bigphi = bigphi(x)
    _smallphi = smallphi(x)
    mean = maxmean(a, b, _bigphi, _theta, _smallphi)
    variance = maxvariance(a, b, sigmaA, sigmaB, _theta, _bigphi, _smallphi, mean)
    
    g = Wire()
    g.a0 = mean
    g.a1 = a.a1 * _bigphi + b.a1 * (1.0 - _bigphi)
    g.a2 = a.a2 * _bigphi + b.a2 * (1.0 - _bigphi)
    tmp = variance - (g.a1 ** 2) - (g.a2 ** 2)
    if tmp < 0:
        print("Error: max function cannot take square root of a negative value!", tmp)
        exit(-1)
    g.a3 = math.sqrt(tmp)
    return g

def minObj(a, b):
    sigmaA = sigma(a)
    sigmaB = sigma(b)
    _rho = rho(a, b, sigmaA, sigmaB)
    _theta = theta(sigmaA, sigmaB, _rho)
    x = (a.a0-b.a0)/_theta 
    _bigphi = bigphi(x)
    _smallphi = smallphi(x)
    mean = minmean(a, b, _bigphi, _theta, _smallphi)
    variance = minvariance(a, b, sigmaA, sigmaB, _theta, _bigphi, _smallphi, mean)
    
    g = Wire()
    g.a0 = mean
    g.a1 = a.a1 * (1.0 - _bigphi) + b.a1 * _bigphi
    g.a2 = a.a2 * (1.0 - _bigphi) + b.a2 * _bigphi
    g.a3 = math.sqrt(variance - (g.a1 ** 2) - (g.a2 ** 2))
    return g
