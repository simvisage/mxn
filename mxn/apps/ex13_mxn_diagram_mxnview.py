'''
Created on 2. 4. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection, MxNDiagram, ECBCalib

from mxn.view import \
    MxNTreeView

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

ge = MCSGeoRect(height=0.06,width=0.2)
mcs = MatrixCrossSection(geo=ge,n_cj=20,cc_law_type='constant')
uni_layers = RLCTexUniform(n_layers=12, ecb_law_type='bilinear')

cs = CrossSection(matrix_cs=mcs,reinf=[uni_layers])

calib = ECBCalib(cs=cs, Mu=3.5)
mxn = MxNDiagram(calib=calib)
mxn_view = MxNTreeView(root=mxn)
mxn_view.configure_traits()