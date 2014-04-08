'''
Created on 26. 2. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection, CrossSectionView

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCSteelBar

bar = RLCSteelBar(x=0.1, z=0.45, area=0.0002)
'''Single steel reinforcement bar
'''

ge = MCSGeoRect(height=0.5, width=0.3)
'''Cross section geometry
'''

cs = CrossSection(reinf=[bar],
                  matrix_cs=MatrixCrossSection(geo=ge,
                                               n_cj=20),
                  eps_lo=0.002,
                  eps_up=-0.0033
                  )

csw = CrossSectionView(cs=cs)
csw.configure_traits()
