'''
Created on Jun 24, 2014

@author: Vancikv
'''

from mxn import \
    CrossSection, CrossSectionView

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

from mxn.reinf_laws import \
    ReinfFabric, ReinfLawBilinear, ReinfLawCubic, \
    ReinfLawFBM, ReinfLawLinear

if ReinfFabric.db.get('test_fabric', None):
    del ReinfFabric.db['test_fabric']
ReinfFabric.db['test_fabric'] = ReinfFabric()
ReinfFabric.db['test_fabric'].key = 'test_fabric'

test_fabric_laws = {'bilinear':
               ReinfLawBilinear(sig_tex_u=1216., eps_u=0.014,
                                var_a=0.8, eps_el_fraction=0.0001),
              'cubic':
               ReinfLawCubic(sig_tex_u=1216., eps_u=0.016,
                                var_a=-5e+6),
              'fbm':
               ReinfLawFBM(sig_tex_u=1216., eps_u=0.014,
                           m=0.5),
              'linear':
               ReinfLawLinear(eps_u=0.014, E_tex=80000.),
              'linear_different':
               ReinfLawLinear(eps_u=0.014, E_tex=160000.),
              'fbm_different':
               ReinfLawFBM(sig_tex_u=1500., eps_u=0.014,
                           m=0.7),
               }

ReinfFabric.db['test_fabric'].mtrl_laws = test_fabric_laws
ReinfFabric.db['test_fabric'].save()

tex_layers = RLCTexUniform(n_layers=12, material='default_fabric')
ge = MCSGeoRect(height=0.06, width=0.2)
'''Cross section geometry
'''

cs = CrossSection(reinf=[tex_layers],
                  matrix_cs=MatrixCrossSection(geo=ge,
                                               n_cj=20,
                                               material='default_mixture'),
                  eps_lo=0.002,
                  eps_up=-0.0033
                  )

csw = CrossSectionView(cs=cs)

# tex_layers.fabric = 'default_fabric'
# tex_layers.fabric = 'test_fabric'
# tex_layers.ecb_law = 'fbm_different'
# print tex_layers.ecb_law_
csw.configure_traits()
# csw.configure_traits()
