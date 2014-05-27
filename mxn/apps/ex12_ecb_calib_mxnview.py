'''
Created on 1. 4. 2014

@author: Vancikv
'''

from mxn.view import \
    MxNTreeView
    
from mxn import \
    ECBCalib
    
ec = ECBCalib(Mu=3.49)
ecw = MxNTreeView(root=ec)
ecw.configure_traits()