'''
Created on 14. 4. 2014

@author: Vancikv

This example shows tree view of the material database
which is the sole default subnode of UseCaseContainer
'''

from view import \
    MxNTreeView

from use_cases import \
    UseCaseContainer

uc_view = MxNTreeView(root=UseCaseContainer())
uc_view.configure_traits()
