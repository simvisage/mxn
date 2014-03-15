'''
Created on 15. 3. 2014

@author: Vancikv
'''

'''MxN diagram for a rectangular concrete cross section 
with steel reinforcement
'''

from mxn import \
    CrossSection, MxNDiagram, MxNDiagramView
    
from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCSteelBar

bar1 = RLCSteelBar(position=[0.1, 0.45], area=0.002)
bar2 = RLCSteelBar(position=[0.1, 0.05], area=0.002)
'''Single steel reinforcement bar
'''

ge = MCSGeoRect(height=0.5, width=0.3)
'''Cross section geometry
'''

cs = CrossSection(reinf=[bar1, bar2],
                         matrix_cs=MatrixCrossSection(geo=ge,n_cj=20),
                         eps_lo=0.002,
                         eps_up=-0.0033
                         )

mn = MxNDiagram(cs=cs)
mnw = MxNDiagramView(mxn=mn)
mnw.configure_traits()