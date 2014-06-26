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

#===============================================================================
# Input values
#===============================================================================
# 16 rovings in 14cm wide cross section recalculated for unit cross sectional width
n_rovings_pm = int(16 / 0.14)
# ultimate moment recalculated for unit cs width
Mu_pm = 3.11 / 0.20

ge = MCSGeoRect(height=0.06, width=1.0)
mcs = MatrixCrossSection(geo=ge, n_cj=20, material='default_mixture', material_law='constant')
uni_layers = RLCTexUniform(n_layers=12, material='default_fabric', material_law='fbm')

cs = CrossSection(matrix_cs=mcs, reinf=[uni_layers])
calib = ECBCalib(cs=cs, Mu=Mu_pm)

eps_lo1, eps_up1 = mcs.material_.eps_c_u, -mcs.material_.eps_c_u
eps_lo2, eps_up2 = -mcs.material_.eps_c_u, mcs.material_.eps_c_u

# 1st calibration
cs.set(eps_up=eps_up1, eps_lo=eps_lo1)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ', cs.M
print 'N = ', cs.N

cs.set(eps_up=eps_up2, eps_lo=eps_lo2)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ', cs.M
print 'N = ', cs.N

# 2nd calibration - change Mu
calib.Mu = Mu_pm * 1.1
calib_law = calib.calibrated_ecb_law

cs.set(eps_up=eps_up1, eps_lo=eps_lo1)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ', cs.M
print 'N = ', cs.N

cs.set(eps_up=eps_up2, eps_lo=eps_lo2)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ', cs.M
print 'N = ', cs.N

# 3rd calibration - change ecb law type
uni_layers.material_law = 'linear'
calib_law = calib.calibrated_ecb_law

cs.set(eps_up=eps_up1, eps_lo=eps_lo1)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ', cs.M
print 'N = ', cs.N

cs.set(eps_up=eps_up2, eps_lo=eps_lo2)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ', cs.M
print 'N = ', cs.N

# 4th calibration - change f_ck
mcs.material_.f_ck = 60.0
calib_law = calib.calibrated_ecb_law

cs.set(eps_up=eps_up1, eps_lo=eps_lo1)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ', cs.M
print 'N = ', cs.N

cs.set(eps_up=eps_up2, eps_lo=eps_lo2)
print 'MN for eps_up = ', cs.eps_up, ', eps_lo = ', cs.eps_lo
print '====================================================='
print 'M = ', cs.M
print 'N = ', cs.N
