'''
Created on 22. 4. 2014

@author: Vancikv
'''

from mxn import \
    CrossSection

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

from mxn.reinf_laws import \
    ReinfLawBase, ReinfLawFBM

import numpy as np

import pickle

from mxn.utils import \
    get_outfile

if ReinfLawBase.db.get('fbm-test', None):
    del ReinfLawBase.db['fbm-test']
ReinfLawBase.db['fbm-test'] = ReinfLawFBM(sig_tex_u=1216.,
                                            eps_u=0.014,
                                            m=0.5)
ReinfLawBase.db['fbm-test'].key = 'fbm-test'

def test_reinf_law_states():
    '''Test the moment and normal force calculated for a cross section
    with changing reinforcement law.
    '''
    cp = CrossSection(reinf=[RLCTexUniform(n_layers=6, ecb_law_key='cubic-default')],
                         matrix_cs=MatrixCrossSection(geo=MCSGeoRect(width=0.1, height=0.05),
                                                      n_cj=20, cc_law_type='constant', mm_key='default_mixture'),
                         eps_lo=0.014,
                         eps_up=-0.0033,
                         )

    assert np.allclose([cp.M, cp.N], [1.3464526369891257, -10.291789885114646])
    cp.reinf_components_with_state[0].ecb_law_key = 'fbm-test'

    object_file = get_outfile(folder_name='.mxn',
                             file_name='test08_reinf_law.pkl')
    pickle.dump(cp, open(object_file, 'wb'), 1)

    assert np.allclose([cp.M, cp.N], [1.3465387287796249, 2.3335097542460943])
    ReinfLawBase.db['fbm-test'].sig_tex_u = 1000.
    assert np.allclose([cp.M, cp.N], [1.2920501456587206, -6.8288234069052649])
    ReinfLawBase.db['fbm-test'].sig_tex_u = 1216.
    assert np.allclose([cp.M, cp.N], [1.3465387287796249, 2.3335097542460943])

    loaded_cp = pickle.load(open(object_file, 'rb'))
    assert np.allclose([loaded_cp.M, loaded_cp.N], [1.3465387287796249, 2.3335097542460943])
    ReinfLawBase.db['fbm-test'].sig_tex_u = 1000.
    assert np.allclose([loaded_cp.M, loaded_cp.N], [1.2920501456587206, -6.8288234069052649])
    assert np.allclose([cp.M, cp.N], [1.2920501456587206, -6.8288234069052649])

if __name__ == '__main__':
    test_reinf_law_states()
