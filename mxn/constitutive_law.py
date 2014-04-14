'''
Created on Aug 23, 2012

@author: rch
'''

from etsproxy.traits.api import \
    HasStrictTraits, Property, WeakRef, \
    cached_property, on_trait_change

from etsproxy.traits.ui.api import \
    View, Item

import numpy as np

from mathkit.mfn import MFnLineArray

class CLBase(HasStrictTraits):
    '''Base class for Effective Crack Bridge Laws.'''

    cs = WeakRef(transient=True)
    
    def __getstate__ ( self ):
        '''Overriding __getstate__ because of WeakRef usage
        '''
        state = super( HasStrictTraits, self ).__getstate__()
        
        for key in [ 'cs', 'cs_', ]:
            if state.has_key( key ):
                del state[ key ]

        return state

    def __init__(self, *args, **kw):
        super(HasStrictTraits, self).__init__(*args, **kw)
        self.on_trait_change(self._notify_cs, '+input')

    @on_trait_change('+input')
    def _notify_cs(self):
        if self.cs:
            self.cs.law_changed = True
        pass

    def set_cparams(self, *args):
        for name, value in zip(self.cnames, args):
            setattr(self, name, value)
        self._notify_cs()

    arr = Property()
    def _get_arr(self):
        return self.eps_arr, self.sig_arr

    mfn = Property()
    def _get_mfn(self):
        return MFnLineArray(xdata=self.eps_arr,
                            ydata=self.sig_arr)

    mfn_vct = Property()
    def _get_mfn_vct(self):
        return np.vectorize(self.mfn.get_value, otypes=[np.float])

    def plot(self, fig):
        ax = fig.add_subplot(1, 1, 1)
        self.plot_ax(ax)

    def plot_ax(self, ax):
        ax.plot(*self.arr)

    def default_traits_view(self):

        input_traits = self.traits(input=lambda x: x != None)

        citems = [Item(name) for name in input_traits ]
        return View(*citems,
                    buttons=['OK', 'Cancel']
                    )
