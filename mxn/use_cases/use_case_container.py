'''
Created on 1. 7. 2014

@author: Vancikv
'''

from traits.api import \
    HasStrictTraits, List, Str, Button, \
    Trait, Instance

from traitsui.api import \
    View, Item, VGroup

from mxn.view import \
    MxNTreeNode

from use_case_parametric_study import \
    UCParametricStudy

from mxn import \
    MxNDiagram, ECBCalib

from use_case_database import \
    UCDatabase

class UseCaseContainer(MxNTreeNode):
    '''Contains MxN diagrams wrapped in MxNDescription classes.
    MxNDescription controls plotting of particular MxNDiagram
    that can added/removed or modified ,e.g. via tree editor.
    '''

    node_name = Str('Use cases')

    use_case_to_add = Trait('pstudy', {'pstudy'      :   UCParametricStudy,
                                       'calibration' :   ECBCalib,
                                       'prognosis'   :   MxNDiagram}
                            )

    add_use_case = Button('Add use case')
    def _add_use_case_fired(self):
        self.tree_node_list.append(self.use_case_to_add_())

    tree_view = View(Item('use_case_to_add', show_label=False),
                Item('add_use_case'))

    tree_node_list = List(Instance(MxNTreeNode))
    def _tree_node_list_default(self):
        return [UCDatabase()]