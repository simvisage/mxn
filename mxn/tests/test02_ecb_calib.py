'''
Created on Nov 21, 2013

@author: rch
'''

from mxn import \
    ECBCalib, CrossSection

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

from mxn import \
    ReinfLawBase, ReinfLawFBM

import numpy as np

import pickle

from mxn.utils import \
    get_outfile

def xtest_ecb_law_calib():
    '''Test the calibrated crack bridge law.
    '''
    #===============================================================================
    # Input values
    #===============================================================================
    # 23 rovings
    n_rovings = 23
    # roving cross sectional area
    A_rov = 0.461
    # ultimate moment
    Mu = 3.50

    ge = MCSGeoRect(height=0.06, width=0.2)
    mcs = MatrixCrossSection(geo=ge, n_cj=20, mm_key='default_mixture', cc_law_type='constant')

    # prepare a new law to be calibrated - this will disapear
    # once the laws are embedded in the reinforcement component
    if ReinfLawBase.db.get('new_fbm_law', None):
        del ReinfLawBase.db['new_fbm_law']
    ReinfLawBase.db['new_fbm_law'] = ReinfLawFBM()

    uni_layers = RLCTexUniform(n_layers=12,
                               n_rovings=n_rovings,
                               A_roving=A_rov,
                               ecb_law_key='new_fbm_law')

    cs = CrossSection(matrix_cs=mcs, reinf=[uni_layers])

    calib = ECBCalib(cs=cs, Mu=Mu)
    test_eps_arr = np.linspace(0.0, 0.005, 10)
    calib_file = get_outfile(folder_name='.mxn',
                             file_name='test02_calib.pkl')

    assert np.allclose(calib.calibrated_ecb_law.mfn_vct(test_eps_arr),
                       np.array([0., 169.56745719, 308.0713995, 426.15150252,
                                 528.22368093, 617.57902395, 696.18106351,
                                 765.44225452, 826.76851637, 881.07603382],
                                dtype=float))

    assert np.allclose(cs.reinf_components_with_state[0].layer_lst[0].ecb_law.mfn_vct(test_eps_arr),
                       np.array([0., 169.56745719, 308.0713995, 426.15150252,
                                 528.22368093, 617.57902395, 696.18106351,
                                 765.44225452, 826.76851637, 881.07603382],
                                dtype=float))
    pickle.dump(calib, open(calib_file, 'wb'), 1)

    uni_layers.ecb_law_key = 'cubic-default'

    assert np.allclose(calib.calibrated_ecb_law.mfn_vct(test_eps_arr),
                       np.array([0., 128.33734405, 247.41169038, 357.44885771,
                                 458.78005031, 551.89774542, 636.94074038,
                                 714.45215726, 784.72942118, 848.06386907],
                                dtype=float))

    uni_layers.ecb_law_key = 'linear-default'

    assert np.allclose(calib.calibrated_ecb_law.mfn_vct(test_eps_arr),
                       np.array([0., 51.40222925, 102.8044585, 154.20668775,
                                 205.608917, 257.01114625, 308.41337551,
                                 359.81560476, 411.21783401, 462.62006326],
                                dtype=float))

    uni_layers.ecb_law_key = 'bilinear-default'

    assert np.allclose(calib.calibrated_ecb_law.mfn_vct(test_eps_arr),
                       np.array([0., 858.01243898, 873.058472, 888.10450501,
                                 903.15053803, 918.19657105, 933.24260407,
                                 948.28863708, 963.3346701, 978.38070312],
                                dtype=float))

    mcs.cc_law_type = 'quadratic'
    uni_layers.ecb_law_key = 'fbm-default'
    calib.Mu = 3.49

    assert np.allclose(calib.calibrated_ecb_law.mfn_vct(test_eps_arr),
                       np.array([0., 300.73451126, 489.25642137, 628.66800959,
                                 737.65269075, 825.20174306, 896.67226786,
                                 955.78175683, 1004.84170587, 1045.86868703],
                                dtype=float))

    loaded_calib = pickle.load(open(calib_file, 'rb'))

    assert np.allclose(loaded_calib.calibrated_ecb_law.mfn_vct(test_eps_arr),
                       np.array([0., 169.56745719, 308.0713995, 426.15150252,
                                 528.22368093, 617.57902395, 696.18106351,
                                 765.44225452, 826.76851637, 881.07603382],
                                dtype=float))

if __name__ == '__main__':
    test_ecb_law_calib()
