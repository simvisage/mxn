'''
Created on 6. 4. 2014

@author: Vancikv
'''

from traits.api import \
    HasStrictTraits, Int, Instance, Property, cached_property, DelegatesTo, \
    Event, Button, List

from traitsui.api import \
    View, Item, Group, HSplit, VGroup, HGroup, RangeEditor, InstanceEditor

from ecb_calib import \
    ECBCalib

from cross_section import \
    CrossSection

from reinf_layout import \
    RLCTexUniform

from matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

import numpy as np

from mxn_diagram import \
    MxNDiagram
    
from view import \
    MxNTreeNode
    
class MxNParametricStudy(HasStrictTraits):
    node_name = 'Parametric study'
    view=View()
    
    mxn_lst = List(MxNDiagram)
    def _mxn_lst_default(self):
        return [MxNDiagram()]
    
    mxn_lst_with_calib = Property(depends_on = 'mxn_lst')
    def _get_mxn_lst_with_calib(self):
        for mxn in self.mxn_lst:
            if not mxn.calib:
                mxn.calib = ECBCalib()
        return self.mxn_lst

#     
#     tree_node_list = Property()
#     def _get_tree_node_list(self):
#         return self.mxn_lst

    def plot(self, fig):
        ax = fig.add_subplot(1,1,1)
        for mxn in self.mxn_lst_with_calib:
            mxn.plot_MN_custom(ax=ax)
        ax.legend()
        ax.set_xlabel('M[kNm]')
        ax.set_ylabel('N[kN]')
        