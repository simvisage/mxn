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
    MatrixLawBase, MatrixLawBlock, MatrixMixture, MatrixLawQuadratic

import numpy as np

import pickle

from mxn.utils import \
    get_outfile

if MatrixMixture.db.get('mixture-test', None):
    del MatrixMixture.db['mixture-test']
MatrixMixture.db['mixture-test'] = MatrixMixture(f_ck=53.7,
                                                eps_c_u=0.0033,
                                                mtrl_laws={'constant':
                                                                MatrixLawBlock(f_ck=55.7, eps_c_u=0.0033,
                                                                    high_strength_level=50.0, E_c=28e+3),
                                                                'quadratic':
                                                                MatrixLawQuadratic(f_ck=55.7, eps_c_u=0.0033,
                                                                    high_strength_level=50.0, E_c=28e+3),
                                         })
MatrixMixture.db['mixture-test'].key = 'mixture-test'

def test_matrix_law_states():
    '''Test the moment and normal force calculated for a cross section
    with changing matrix law.
    '''
    cp = CrossSection(reinf=[RLCTexUniform(n_layers=6, ecb_law_key='fbm-default')],
                         matrix_cs=MatrixCrossSection(geo=MCSGeoRect(width=0.1, height=0.05),
                                                      n_cj=20, cc_law_type='constant', mm_key='default_mixture'),
                         eps_lo=0.014,
                         eps_up=-0.0033,
                         )

    assert np.allclose([cp.M, cp.N], [1.3465387287796249, 2.3335097542460943])
    cp.matrix_cs_with_state.mm_key = 'mixture-test'

    object_file = get_outfile(folder_name='.mxn',
                             file_name='test09_reinf_law.pkl')
    pickle.dump(cp, open(object_file, 'wb'), 1)

    assert np.allclose([cp.M, cp.N], [1.3140950375716971, 3.8701260913315991])
    MatrixMixture.db['mixture-test'].f_ck = 70.0
    assert np.allclose([cp.M, cp.N], [1.5155334535680236, -5.0522452437834104])
    MatrixMixture.db['mixture-test'].f_ck = 53.7
    assert np.allclose([cp.M, cp.N], [1.3140950375716971, 3.8701260913315991])

    loaded_cp = pickle.load(open(object_file, 'rb'))
    assert np.allclose([loaded_cp.M, loaded_cp.N], [1.3140950375716971, 3.8701260913315991])
    MatrixMixture.db['mixture-test'].f_ck = 70.0
    assert np.allclose([loaded_cp.M, loaded_cp.N], [1.5155334535680236, -5.0522452437834104])
    assert np.allclose([cp.M, cp.N], [1.5155334535680236, -5.0522452437834104])

if __name__ == '__main__':
    test_matrix_law_states()