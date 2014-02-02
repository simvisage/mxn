'''
Created on Jan 30, 2014

@author: rch
'''

'''rectangular concrete cross section with steel reinforcement
'''

from mxn import \
    CrossSection, SteelBar, MatrixCrossSection

sb = SteelBar(position=[0.1, 0.4], area=0.0002)
cs = CrossSection(reinf=[sb],
                         matrix_cs=MatrixCrossSection(width=0.3, height=0.5,
                                                         n_cj=20),
                         eps_lo=0.002,
                         eps_up= -0.0033,
                         )

print 'normal force', cs.N
print 'moment', cs.M
print 'sigma_bar', sb.sig
