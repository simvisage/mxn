'''
Created on Aug 23, 2012

@author: rch
'''

from etsproxy.traits.api import \
    List

from constitutive_law import CLBase

from mxn.view import \
    MxNLeafNode
    
from matresdev.db.simdb import \
    SimDBClass, SimDBClassExt

class ReinfLawBase(CLBase, MxNLeafNode, SimDBClass):
    '''Base class for Effective Crack Bridge Laws.'''

    u0 = List([0.0, 0.0])
    node_name = 'Constitutive law'

ReinfLawBase.db = SimDBClassExt(
            klass = ReinfLawBase,
            verbose = 'io',
            )

if __name__ == '__main__':
    ReinfLawBase.db.configure_traits()