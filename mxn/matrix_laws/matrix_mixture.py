'''
Created on Aug 23, 2012

@author: rch
'''

from traits.api import \
    Property, cached_property, Dict, Str, Float, \
    WeakRef, on_trait_change, Event, List

from traitsui.api import \
    View, Item

from constitutive_law import CLBase

from mxn.view import \
    MxNTreeNode, MxNClassExt

from matresdev.db.simdb import \
    SimDBClass

from matrix_law_bilinear import \
    MatrixLawBilinear

from matrix_law_block import \
    MatrixLawBlock

from matrix_law_linear import \
    MatrixLawLinear

from matrix_law_quad import \
    MatrixLawQuad

from matrix_law_quadratic import \
    MatrixLawQuadratic

import weakref

class MatrixMixture(MxNTreeNode, SimDBClass):
    '''Base class for concrete constitutive laws.'''

    f_ck = Float(55.7, auto_set=False, enter_set=True,
                 law_input=True)
    '''Ultimate compression stress  [MPa]
    '''

    eps_c_u = Float(0.0033, auto_set=False, enter_set=True,
                    law_input=True)
    '''Strain at failure of the matrix in compression [-]
    '''

    mtrl_laws = Dict((Str, CLBase))

    named_mtrl_laws = Property(depends_on='mtrl_laws')
    @cached_property
    def _get_named_mtrl_laws(self):
        for key, mtrl_law in self.mtrl_laws.items():
            mtrl_law.node_name = key
        return self.mtrl_laws

    def get_mtrl_law(self, key):
        law = self.named_mtrl_laws[key]
        law.f_ck = self.f_ck
        law.eps_c_u = self.eps_c_u
        return law

    #===========================================================================
    # Management of backward links
    #===========================================================================

    state_link_lst = List(transient=True)
    '''List of backward links to objects using the fabric
    '''
    def _state_link_lst_default(self):
        return []

    @on_trait_change('+law_input')
    def notify_change(self):
        for link in self.state_link_lst:
            if link():
                link().mixture_changed = True

    def add_link(self, link_to_add):
        '''Adding a backward link to the list - to be called
        from objects using the fabric
        '''
        if link_to_add not in self.state_link_lst:
            self.state_link_lst.append(weakref.ref(link_to_add))

    def del_link(self, link_to_del):
        '''Removing a backward link from the list - to be called
        from objects using the fabric
        '''
        self.state_link_lst[:] = [link for link in self.state_link_lst if link() != link_to_del]

    #===========================================================================
    # UI-related functionality
    #===========================================================================

    tree_node_list = Property(depends_on='mtrl_laws')
    @cached_property
    def _get_tree_node_list(self):
        return self.named_mtrl_laws.values()

    traits_view = View(Item('f_ck'),
                Item('eps_c_u'))

dflt_mxtr = MatrixMixture(mtrl_laws={'bilinear':
                                     MatrixLawBilinear(f_ck=55.7, eps_c_u=0.0033),
                                     'constant':
                                     MatrixLawBlock(f_ck=55.7, eps_c_u=0.0033,
                                                    high_strength_level=50.0, E_c=28e+3),
                                     'linear':
                                     MatrixLawLinear(),
                                     'quad':
                                     MatrixLawQuad(f_ck=55.7, eps_c_u=0.0033,
                                                   high_strength_level=50.0, E_c=28e+3),
                                     'quadratic':
                                     MatrixLawQuadratic(f_ck=55.7, eps_c_u=0.0033,
                                                        high_strength_level=50.0, E_c=28e+3)
                                     })

MatrixMixture.db = MxNClassExt(
            klass=MatrixMixture,
            verbose='io',
            node_name='Matrix mixtures',
            constants=dict(default_mixture=dflt_mxtr)
            )

if __name__ == '__main__':
    MatrixMixture.db.configure_traits()
