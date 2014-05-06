'''
Created on 7. 4. 2014

@author: Vancikv

Test example: creates
'''

from mxn import \
    CrossSection, ECBCalib

from mxn.view import \
    MxNTreeView

from mxn.matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect

from mxn.reinf_layout import \
    RLCTexUniform

import pickle

from mxn.utils import \
    get_outfile

#===============================================================================
# Input values
#===============================================================================
# 16 rovings in 14cm wide cross section recalculated for unit cross sectional width
# ultimate moment recalculated for unit cs width
Mu_pm = 3.11 / 0.20

ge = MCSGeoRect(height=0.06, width=1.0)
mcs = MatrixCrossSection(geo=ge, n_cj=20,
                         cc_law_type='constant')
uni_layers = RLCTexUniform(n_layers=12,
                           ecb_law_type='fbm')
uni_layers.fabric.s_0 = 0.14 / 17

cs = CrossSection(matrix_cs=mcs, reinf=[uni_layers])
calib = ECBCalib(cs=cs, Mu=Mu_pm)
calib_w = MxNTreeView(root=calib)
calib_w.configure_traits()
# calib.cs.reinf_components_with_state[0].ecb_law.save()

calib_file = get_outfile(folder_name='.mxn',
                          file_name='ex15_calib.pkl')

'''Save - load
'''
pickle.dump(calib, open(calib_file, 'wb'), 1)
loaded_calib = pickle.load(open(calib_file, 'rb'))
loaded_calib_w = MxNTreeView(root=loaded_calib)

loaded_calib_w.configure_traits()
