'''
Created on 6. 4. 2014

@author: Vancikv
'''

from mxn.view import \
    MxNTreeView

from mxn.use_cases import \
    UseCaseContainer, UCParametricStudy

mxn_ps = UCParametricStudy()
mxn_ps.element_to_add = 'mxndiagram'
mxn_ps.add_element = True
mxn_ps.add_element = True

ucc = UseCaseContainer()
ucc.tree_node_list.append(mxn_ps)

mxn_ps_view = MxNTreeView(root=ucc)
mxn_ps_view.configure_traits()
