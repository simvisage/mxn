'''
Created on 2. 4. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection, MxNDiagram, \
    MatrixLawBase, ReinfLawBase

from mxn.view import \
    MxNTreeView, MxNTreeNode

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

ge = MCSGeoRect(height=0.06, width=0.2)
mcs = MatrixCrossSection(geo=ge, n_cj=20, mm_key='default_mixture', cc_law_type='quadratic')
uni_layers = RLCTexUniform(n_layers=12, ecb_law_key='fbm-default')

cs = CrossSection(matrix_cs=mcs, reinf=[uni_layers])

mxn = MxNDiagram(cs=cs)

root_node = MxNTreeNode(tree_node_list=[MatrixLawBase.db,
                                                 ReinfLawBase.db,
                                                 mxn],
                                 node_name='database')

mxn_view = MxNTreeView(root=root_node)
mxn_view.configure_traits()

print ReinfLawBase.db.constants.keys()
print ReinfLawBase.db.instances.keys()
