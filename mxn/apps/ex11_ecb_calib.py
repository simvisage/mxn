'''
Created on 20. 3. 2014

@author: Vancikv
'''

'''Multiple calibrations of ecb law for 
various parameter changes:

1st calibration - default
2nd calibration - change Mu
3rd calibration - change ecb law type
4th calibration - change f_ck
'''

from mxn import \
    CrossSection, ECBCalib

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

ge = MCSGeoRect(height=0.06,width=0.2)
mcs = MatrixCrossSection(geo=ge,n_cj=20,cc_law_type='constant',f_ck=55.0)
uni_layers = RLCTexUniform(n_layers=12, ecb_law_type='fbm')

cs = CrossSection(matrix_cs=mcs,reinf=[uni_layers])
calib = ECBCalib(cs=cs, Mu=3.5)

eps_lo1, eps_up1 = mcs.eps_c_u, -mcs.eps_c_u 
eps_lo2, eps_up2 = -mcs.eps_c_u, mcs.eps_c_u 

#1st calibration
cs.set(eps_up=eps_up1,eps_lo=eps_lo1)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ',cs.M
print 'N = ',cs.N

cs.set(eps_up=eps_up2,eps_lo=eps_lo2)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ',cs.M
print 'N = ',cs.N

#2nd calibration - change Mu
calib.Mu = 3.0
calib_law = calib.calibrated_ecb_law

cs.set(eps_up=eps_up1,eps_lo=eps_lo1)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ',cs.M
print 'N = ',cs.N

cs.set(eps_up=eps_up2,eps_lo=eps_lo2)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ',cs.M
print 'N = ',cs.N

#3rd calibration - change ecb law type
uni_layers.ecb_law_type = 'linear'
calib_law = calib.calibrated_ecb_law

cs.set(eps_up=eps_up1,eps_lo=eps_lo1)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ',cs.M
print 'N = ',cs.N

cs.set(eps_up=eps_up2,eps_lo=eps_lo2)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ',cs.M
print 'N = ',cs.N

#4th calibration - change f_ck
mcs.f_ck = 60.0
calib_law = calib.calibrated_ecb_law

cs.set(eps_up=eps_up1,eps_lo=eps_lo1)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ',cs.M
print 'N = ',cs.N

cs.set(eps_up=eps_up2,eps_lo=eps_lo2)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ',cs.M
print 'N = ',cs.N
