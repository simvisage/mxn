'''
Created on 6. 4. 2014

@author: Vancikv
'''

from mxn import \
    MxNParametricStudy, MxNPSView

mxn_ps = MxNParametricStudy()
mxn_ps_view = MxNPSView(root=mxn_ps)
mxn_ps_view.configure_traits()
