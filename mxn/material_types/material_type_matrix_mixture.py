'''
Created on Aug 23, 2012

@author: rch
'''

from traits.api import \
    Property, cached_property, Dict, Str, \
    Float

from traitsui.api import \
    View, Item

from mxn.view import \
    MxNClassExt

from matrix_laws import \
    MatrixLawBilinear, MatrixLawBlock, \
    MatrixLawLinear, MatrixLawQuad, \
    MatrixLawQuadratic, MatrixLawBase

from material_type_base import \
    MaterialTypeBase

basic_laws = {'bilinear':
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
                                     }
class MTMatrixMixture(MaterialTypeBase):
    '''Base class for concrete constitutive laws.'''

    f_ck = Float(55.7, auto_set=False, enter_set=True,
                 law_input=True)
    '''Ultimate compression stress  [MPa]
    '''

    eps_c_u = Float(0.0033, auto_set=False, enter_set=True,
                    law_input=True)
    '''Strain at failure of the matrix in compression [-]
    '''

    mtrl_laws = Dict((Str, MatrixLawBase))
    def _mtrl_laws_default(self):
        return basic_laws

    named_mtrl_laws = Property(depends_on='mtrl_laws,+law_input')
    @cached_property
    def _get_named_mtrl_laws(self):
        for key, mtrl_law in self.mtrl_laws.items():
            mtrl_law.node_name = key
            mtrl_law.f_ck = self.f_ck
            mtrl_law.eps_c_u = self.eps_c_u
        return self.mtrl_laws

    #===========================================================================
    # UI-related functionality
    #===========================================================================

    traits_view = View(Item('f_ck'),
                       Item('eps_c_u'))

MTMatrixMixture.db = MxNClassExt(
            klass=MTMatrixMixture,
            verbose='io',
            node_name='Reinforcement fabrics'
            )

print 'XXXXX'
if MTMatrixMixture.db.get('default_mixture', None):
    del MTMatrixMixture.db['default_mixture']
MTMatrixMixture.db['default_mixture'] = MTMatrixMixture()

if __name__ == '__main__':
    MTMatrixMixture.db.configure_traits()