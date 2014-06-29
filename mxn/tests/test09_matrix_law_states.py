'''
Created on 23. 4. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

from mxn.matrix_laws import \
    MatrixLawBase, MatrixLawBlock, MatrixLawQuadratic

from mxn.material_types import \
    MTMatrixMixture

import numpy as np

import pickle

from mxn.utils import \
    get_outfile

if MTMatrixMixture.db.get('mixture-test', None):
    del MTMatrixMixture.db['mixture-test']
MTMatrixMixture.db['mixture-test'] = MTMatrixMixture(f_ck=53.7,
                                                eps_c_u=0.0033,
                                                mtrl_laws={'constant':
                                                                MatrixLawBlock(f_ck=55.7, eps_c_u=0.0033,
                                                                    high_strength_level=50.0, E_c=28e+3),
                                                                'quadratic':
                                                                MatrixLawQuadratic(f_ck=55.7, eps_c_u=0.0033,
                                                                    high_strength_level=50.0, E_c=28e+3),
                                         })
MTMatrixMixture.db['mixture-test'].key = 'mixture-test'

def test_matrix_law_states():
    '''Test the moment and normal force calculated for a cross section
    with changing matrix law.
    '''
    cp = CrossSection(reinf=[RLCTexUniform(n_layers=6, material='default_fabric', material_law='fbm')],
                         matrix_cs=MatrixCrossSection(geo=MCSGeoRect(width=0.1, height=0.05),
                                                      n_cj=20, material_law='constant', material='default_mixture'),
                         eps_lo=0.014,
                         eps_up=-0.0033,
                         )

    cp.reinf_components_with_state[0].material_law_.set(sig_tex_u=1216., eps_u=0.014, m=0.5)
    cp.reinf_components_with_state[0].material_.set(s_0=0.00416, A_roving=0.461)

    assert np.allclose([cp.M, cp.N], [1.3465387287796249, 2.3335097542460943])
    cp.matrix_cs_with_state.material = 'mixture-test'

    object_file = get_outfile(folder_name='.mxn',
                             file_name='test09_reinf_law.pkl')
    pickle.dump(cp, open(object_file, 'wb'), 1)
    assert np.allclose([cp.M, cp.N], [1.3140950375716971, 3.8701260913315991])

    MTMatrixMixture.db['mixture-test'].f_ck = 70.0
    assert np.allclose([cp.M, cp.N], [1.5155334535680236, -5.0522452437834104])
    MTMatrixMixture.db['mixture-test'].f_ck = 53.7
    assert np.allclose([cp.M, cp.N], [1.3140950375716971, 3.8701260913315991])

    loaded_cp = pickle.load(open(object_file, 'rb'))
    assert np.allclose([loaded_cp.M, loaded_cp.N], [1.3140950375716971, 3.8701260913315991])
    MTMatrixMixture.db['mixture-test'].f_ck = 70.0
    assert np.allclose([loaded_cp.M, loaded_cp.N], [1.5155334535680236, -5.0522452437834104])
    assert np.allclose([cp.M, cp.N], [1.5155334535680236, -5.0522452437834104])

if __name__ == '__main__':
    test_matrix_law_states()
