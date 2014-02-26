'''
Created on Aug 23, 2012

@author: rch
'''

from etsproxy.traits.api import \
    List

from constitutive_law import CLBase

class ReinfLawBase(CLBase):
    '''Base class for Effective Crack Bridge Laws.'''

    u0 = List([0.0, 0.0])

if __name__ == '__main__':
    from constitutive_law import ConstitutiveLawModelView
    #ecbl = ECBLFBM()
    ecbl = ECBLPiecewiseLinear()
    ew = ConstitutiveLawModelView(model = ecbl)
    ew.configure_traits()
