'''
Created on 19. 3. 2014

@author: Vancikv
'''

'''Example of plotting of mxn diagram for textile
reinforced concrete including crack bridge law calibration
'''

from mxn import \
    CrossSection, MxNDiagram, MxNDiagramView, ECBCalib

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

ge = MCSGeoRect(height=0.06, width=0.2)
mcs = MatrixCrossSection(geo=ge, n_cj=20, cc_law_type='constant')
uni_layers = RLCTexUniform(n_layers=12, ecb_law_type='bilinear')

cs = CrossSection(matrix_cs=mcs, reinf=[uni_layers])

mxn = MxNDiagram(cs=cs)
mxn_view = MxNDiagramView(mxn=mxn)
mxn_view.configure_traits()
