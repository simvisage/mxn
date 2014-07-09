'''
Created on 2. 4. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection, MxNDiagram

from mxn.view import \
    MxNTreeView

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

ge = MCSGeoRect(height=0.06, width=0.2)
mcs = MatrixCrossSection(geo=ge, n_cj=20, material='default_mixture', material_law='quadratic')
uni_layers = RLCTexUniform(n_layers=12, material='default_fabric', material_law='cubic')

cs = CrossSection(matrix_cs=mcs, reinf=[uni_layers])
mxn = MxNDiagram(cs=cs)

mxn_view = MxNTreeView(root=mxn)
mxn_view.configure_traits()
