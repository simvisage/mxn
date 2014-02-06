'''
Created on Jan 30, 2014

@author: rch
'''

'''rectangular concrete cross section with steel reinforcement
'''

from mxn import \
    CrossSection, SteelBar, MatrixCrossSection, GeoRect

sb = SteelBar(position=[0.1, 0.45], area=0.0002)
ge = GeoRect(height=0.5, width=0.3)
cs = CrossSection(reinf=[sb],
                         matrix_cs=MatrixCrossSection(geo=ge,
                                                         n_cj=20),
                         eps_lo=0.002,
                         eps_up= -0.0033,
                         )

print 'normal force', cs.N
print 'moment', cs.M
