'''
Created on 31. 1. 2014

@author: Vancikv
'''

from etsproxy.traits.api import \
    Float, Property, cached_property, \
    Trait, Instance

from etsproxy.traits.ui.api import \
    View, Item, VGroup, Group

from reinf_layout_component import \
    ReinfLayoutComponent, \
    STATE_LAW_AND_GEOMETRY_CHANGE, \
    STATE_AND_GEOMETRY_CHANGE

from mxn.reinf_laws import \
    ReinfLawSteel

from mxn.reinf_laws import \
    ReinfLawBase

from mxn.utils import \
    KeyRef

class RLCBar(ReinfLayoutComponent):
    '''base class for bar reinforcement
    '''
    def __init__(self, *args, **metadata):
        '''Default value of law must be set here to ensure
        it has been set before an editor for it is requested
        '''
        default_law = metadata.get('ecb_law', None)
        if default_law:
            self.ecb_law = default_law
        else:
            self.ecb_law = 'steel-default'

        super(RLCBar, self).__init__(**metadata)

    x = Float(0.1, auto_set=False, enter_set=True, geo_input=True)
    z = Float(0.45, auto_set=False, enter_set=True, geo_input=True)
    '''position of the bar with respect to upper left
    corner of reinforced cross section
    '''

    area = Float(0.0002, auto_set=False, enter_set=True, geo_input=True)
    '''area of the bar
    '''

    ecb_law = KeyRef(db=ReinfLawBase.db)

    eps = Property(depends_on=STATE_AND_GEOMETRY_CHANGE)
    '''Strain of the bar
    '''
    @cached_property
    def _get_eps(self):
        # ------------------------------------------------------------------------
        # geometric params independent from the value for 'eps_t'
        # ------------------------------------------------------------------------
        height = self.matrix_cs.geo.height
        eps_lo = self.state.eps_lo
        eps_up = self.state.eps_up
        # strain at the height of reinforcement bar [-]:
        #
        return eps_up + (eps_lo - eps_up) * self.z / height

    sig = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Stress of the bar
    '''
    @cached_property
    def _get_sig(self):
        return self.ecb_law_.mfn.get_value(self.eps)

    f = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''force in the bar [kN]:
    '''
    @cached_property
    def _get_f(self):
        sig = self.sig
        A_bar = self.area
        return sig * A_bar * self.unit_conversion_factor

    N = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Get the resulting normal force.
    '''
    @cached_property
    def _get_N(self):
        return self.f

    M = Property(depends_on=STATE_LAW_AND_GEOMETRY_CHANGE)
    '''Get the resulting moment.
    '''
    @cached_property
    def _get_M(self):
        return self.f * self.z

    def plot_geometry(self, ax, clr='DarkOrange'):
        '''Plot geometry'''
        ax.plot(self.x, self.matrix_cs.geo.height - self.z, 'o', color=clr)

    def plot_eps(self, ax):
        h = self.matrix_cs.geo.height
        ax.hlines([h - self.z], [0], [-self.eps], lw=4, color='DarkOrange')

    def plot_sig(self, ax):
        h = self.matrix_cs.geo.height
        ax.hlines([h - self.z], [0], [-self.f], lw=4, color='DarkOrange')

    tree_view = View(VGroup(
                       Item('area'),
                       Group(
                       Item('x'),
                       Item('z'),
                       label='Position'
                       ),
                       Group(
                       Item('ecb_law', show_label=False),
                       label='Reinforcement law'
                       ),
                       springy=True
                       ),
                       resizable=True,
                       buttons=['OK', 'Cancel']
                       )

if __name__ == '__main__':
    pass
