from numpy import linspace, zeros, sin, exp, random, sqrt, pi, sign
from scipy.optimize import leastsq
import pylab

from lmfit import Parameters, Minimizer
from lmfit.utilfuncs import gauss, loren

from testutils import report_errors

def residual(pars, x, data=None):
    g1 = gauss(x, pars['a1'].value, pars['c1'].value, pars['w1'].value)
    g2 = gauss(x, pars['a2'].value, pars['c2'].value, pars['w2'].value)
    model = g1 + g2
    if data is None:
        return model
    return (model - data)

n    = 601
xmin = 0.
xmax = 15.0
noise = random.normal(scale=.65, size=n)
x = linspace(xmin, xmax, n)

fit_params = Parameters()
fit_params.add_many(('a1', 12.0, True, None, None),
                    ('c1',  5.3, True, None, None),
                    ('w1',  1.0, True, None, None),
                    ('a2',  9.1, True, None, None),
                    ('c2',  8.1, True, None, None),
                    ('w2',  2.5, True, None, None))

data  = residual(fit_params, x) + noise

pylab.plot(x, data, 'r+')

fit_params = Parameters()
fit_params.add_many(('a1',  8.0, True, None, 14.),
                    ('c1',  5.0, True, None, None),
                    ('w1',  0.7, True, None, None),
                    ('a2',  3.1, True, None, None),
                    ('c2',  8.8, True, None, None))
fit_params.add('w2', expr='2.5*w1')

myfit = Minimizer(residual, fit_params,
                  fcn_args=(x,), fcn_kws={'data':data})

myfit.prepare_fit()

init = residual(fit_params, x)

pylab.plot(x, init, 'b--')

myfit.leastsq()

print ' N fev = ', myfit.nfev
print myfit.chisqr, myfit.redchi, myfit.nfree

report_errors(fit_params)

fit = residual(fit_params, x)

pylab.plot(x, fit, 'k-')
pylab.show()





