'''
Created on 26. 2. 2014

@author: Vancikv
'''

from cross_section import \
    CrossSection
    
from cross_section_view import \
    CrossSectionView

from matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from reinf_layout import \
    RLCBar

bar = RLCBar(x=0.1, z=0.45, material='bar_d10')
'''Single steel reinforcement bar
'''

ge = MCSGeoRect(height=0.5, width=0.3)
'''Cross section geometry
'''

mcs = MatrixCrossSection(geo=ge, n_cj=20, material='default_mixture')

cs = CrossSection(reinf=[bar],
                  matrix_cs=mcs,
                  eps_lo=0.002,
                  eps_up=-0.0033
                  )

csw = CrossSectionView(cs=cs)
csw.configure_traits()
