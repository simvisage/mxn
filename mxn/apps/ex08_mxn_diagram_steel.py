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
    RLCBar

bar1 = RLCBar(x=0.1, z=0.45, material='bar_d10')
bar2 = RLCBar(x=0.1, z=0.05, material='bar_d10')
'''Single steel reinforcement bar
'''

ge = MCSGeoRect(height=0.5, width=0.3)
'''Cross section geometry
'''

cs = CrossSection(reinf=[bar1, bar2],
                         matrix_cs=MatrixCrossSection(geo=ge,
                                                      n_cj=20),
                         eps_lo=0.002,
                         eps_up=-0.0033
                         )

mn = MxNDiagram(cs=cs)
mnw = MxNDiagramView(mxn=mn)
mnw.configure_traits()
