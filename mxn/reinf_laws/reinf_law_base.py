'''
Created on Aug 23, 2012

@author: rch
'''

from etsproxy.traits.api import \
    List

from constitutive_law import CLBase

from mxn.view import \
    MxNLeafNode

class ReinfLawBase(CLBase, MxNLeafNode):
    '''Base class for Effective Crack Bridge Laws.'''

    u0 = List([0.0, 0.0])
    node_name = 'Constitutive law'

if __name__ == '__main__':
    from constitutive_law import ConstitutiveLawModelView
    #ecbl = ECBLFBM()
    ecbl = ECBLPiecewiseLinear()
    ew = ConstitutiveLawM odelView(model = ecbl)
    ew.configure_traits()
