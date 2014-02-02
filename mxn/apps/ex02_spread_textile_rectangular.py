'''
Created on 1. 2. 2014

@author: Vancikv
'''

'''rectangular concrete cross section with textile reinforcement input as single layers
'''

from mxn import \
    CrossSection, ReinfTexLayer, MatrixCrossSection, GeoRect
    
tl1 = ReinfTexLayer(n_rovings=20, A_roving=0.5, z_coord=0.4)
tl2 = ReinfTexLayer(n_rovings=30, A_roving=0.5, z_coord=0.45)
ge = GeoRect(height=0.5, width=0.3)

cs = CrossSection(reinf=[tl1, tl2],
                         matrix_cs=MatrixCrossSection(geo=ge,
                                                         n_cj=20),
                         eps_lo=0.008,
                         eps_up= -0.0033,
                         )

print 'normal force', cs.N
print 'moment', cs.M
print 'sigma_layer1', tl1.sig_t
