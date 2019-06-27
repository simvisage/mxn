'''
Created on 2. 4. 2014

@author: Vancikv

Standard tree view with the default database node
and added mxn_diagram node
'''

from mxn.use_cases import \
    UseCaseContainer
from mxn.view import \
    MxNTreeView


ucc = UseCaseContainer()
ucc.use_case_to_add = 'prediction'
ucc.add_use_case = True

uc_view = MxNTreeView(root=ucc)
uc_view.configure_traits()