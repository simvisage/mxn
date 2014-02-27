'''
Created on Jun 23, 2010

@author: alexander
'''

from etsproxy.traits.api import \
    Float, Instance, Array, Property, cached_property, \
    HasStrictTraits, DelegatesTo, Int, Event, Callable, Button, \
    on_trait_change

from etsproxy.traits.ui.api import \
    TreeEditor, TreeNode, View, Item, Group, HSplit, ModelView, \
    VGroup, HGroup, RangeEditor, InstanceEditor

import numpy as np
import pylab as p

from scipy.optimize import fsolve

from cross_section import \
    CrossSection

from reinf_layout import \
    RLCTexUniform, RLCTexLayer, RLCSteelBar

from matrix_cross_section import \
    MatrixCrossSection, MCSGeoRect
    
from reinf_laws import \
    ReinfLawBase

from util.traits.editors.mpl_figure_editor import  \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

from matresdev.db.simdb import SimDB
simdb = SimDB()

class ECBCalib(HasStrictTraits):

    # rupture moment and normal force measured in the calibration experiment
    # (three point bending test)
    #
    Mu = Float(3.5, calib_input=True) # [kNm]
    Nu = Float(0.0, calib_input=True) # [kN]

    #===========================================================================
    # Cross Section Specification (Geometry and Layout)
    #===========================================================================

    cs = Instance(CrossSection)
    def _cs_default(self):
        return CrossSection(reinf=[RLCTexUniform(n_layers=12)],
                               matrix_cs=MatrixCrossSection(geo=MCSGeoRect(width=0.2, height=0.06), n_cj=20))
        
    notify_change = Callable(None)

    modified = Event
    @on_trait_change('cs.changed,+calib_input')
    def _set_modified(self):
        self.modified = True
        if self.notify_change != None:
            self.notify_change()

    u0 = Property(Array(float), depends_on='cs.changed')
    '''Construct the initial vector.
    '''
    @cached_property
    def _get_u0(self):
        u0 = self.cs.reinf_components_with_state[0].ecb_law.u0

        eps_up = -self.cs.matrix_cs.eps_c_u
        eps_lo = self.cs.reinf_components_with_state[0].convert_eps_tex_u_2_lo(u0[0])

        print 'eps_up', eps_up
        print 'eps_lo', eps_lo

        return np.array([eps_lo, u0[1] ], dtype='float')

    # iteration counter
    #
    n = Int(0)
    def get_lack_of_fit(self, u):
        '''Return the difference between 'N_external' and 'N_internal' as well as 'M_external' and 'M_internal'
        N_c (=compressive force of the compressive zone of the concrete)
        N_t (=total tensile force of the reinforcement layers)
        '''

        print '--------------------iteration', self.n, '------------------------'
        self.n += 1
        # set iteration counter
        #
        eps_up = -self.cs.matrix_cs.eps_c_u
        eps_lo = u[0]

        self.cs.set(eps_lo=eps_lo, eps_up=eps_up)

        eps_tex_u = self.cs.reinf_components_with_state[0].convert_eps_lo_2_tex_u(u[0])
        self.cs.reinf_components_with_state[0].ecb_law.set_cparams(eps_tex_u, u[1])
        
        for layer in self.cs.reinf_components_with_state[0].layer_lst:
            layer.ecb_law.set_cparams(eps_tex_u, u[1])

        N_internal = self.cs.N
        M_internal = self.cs.M

        d_N = N_internal - self.Nu
        d_M = M_internal - self.Mu

        return np.array([ d_N, d_M ], dtype=float)

    u_sol = Property(Array(Float), depends_on='cs.changed,+calib_input')
    '''Solution vector returned by 'fit_response'.'''
    @cached_property
    def _get_u_sol(self):
        '''iterate 'eps_t' such that the lack of fit between the calculated
        normal forces in the tensile reinforcement and the compressive zone (concrete)
        is smaller then 'xtol' defined in function 'brentq'.
        NOTE: the method 'get_lack_of_fit' returns the relative error.
        '''

        # use scipy-functionality to get the iterated value of 'eps_t'
        # NOTE: get_lack_of_fit must have a sign change as a requirement
        # for the function call 'brentq' to work property. 

        # The method brentq has optional arguments such as
        #   'xtol'    - absolut error (default value = 1.0e-12)
        #   'rtol'    - relative error (not supported at the time)
        #   'maxiter' - maximum numbers of iterations used
        #
        return fsolve(self.get_lack_of_fit, self.u0, xtol=1.0e-5)

    calibrated_ecb_law = Property(depends_on='cs.changed,+calib_input')
    '''Calibrated ecbl_mfn
    '''
    @cached_property
    def _get_calibrated_ecb_law(self):
        print 'NEW CALIBRATION'
        self.cs.reinf_components_with_state[0].ecb_law.set_cparams(*self.u_sol)
        return self.cs.reinf_components_with_state[0].ecb_law

    view = View(Item('Mu'),
                Item('Nu'),
                buttons=['OK', 'Cancel']
                )
                
if __name__ == '__main__':

    #------------------------------------------------
    # 1) CALIBRATION:
    # get 'eps_t' and the parameter of the effective 
    # crack bridge function 'var_a' for a given 'eps_c_u'
    #------------------------------------------------
    #
    
    print '\n'
    print 'setup ECBLCalib'
    print '\n'

    ec = ECBCalib(Mu=3.49)
    ecw = ECBCalibModelView(model=ec)
    ecw.configure_traits(view=view)

