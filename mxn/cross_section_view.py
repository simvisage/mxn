'''
Created on 26. 2. 2014

@author: Vancikv
'''

from traits.api import \
    HasStrictTraits, Instance, Button
    
from traitsui.api import \
    TreeEditor, TreeNode, View, Item, Group, HSplit, VGroup, HGroup

from cross_section import \
    CrossSection
    
from reinf_layout import \
    RLCTexUniform, RLCTexLayer, RLCSteelBar

from matrix_cross_section import \
    MatrixCrossSection
    
from util.traits.editors.mpl_figure_editor import \
    MPLFigureEditor

from matplotlib.figure import \
    Figure

tree_editor = TreeEditor(
            nodes=[
                   TreeNode( node_for = [CrossSection],
                             auto_open = True,
                             children = '',
                             label = '=Cross section',
                            ),
                   TreeNode( node_for = [CrossSection],
                             auto_open = True,
                             children = 'reinf_components_with_state',
                             label = '=Reinforcement',
                             view = View(),
                             add = [RLCTexUniform, RLCTexLayer, RLCSteelBar]
                            ),
                   TreeNode( node_for = [RLCTexUniform, RLCTexLayer, RLCSteelBar],
                             auto_open = True,
                             label = 'name'
                            ),
                   TreeNode( node_for = [MatrixCrossSection],
                              auto_open = True,
                            ),
                   ],
                         orientation='vertical'
                         )

class CrossSectionView(HasStrictTraits):
    cs = Instance(CrossSection)
    
    figure = Instance(Figure)
    def _figure_default(self):
        figure = Figure(facecolor='white')
        figure.add_axes([0.08, 0.13, 0.85, 0.74])
        return figure

    replot = Button
    def _replot_fired(self):
        self.figure.clear()
        fig = self.figure
        ax1 = fig.add_subplot(111)

        self.cs.plot_geometry(ax1)
        
    clear = Button()
    def _clear_fired(self):
        self.figure.clear()

    view = View(HSplit(Group(Item('cs',
                            editor = tree_editor,
                            resizable = True,
                            show_label=False),
                           ),
                       Group(HGroup(Item('replot', show_label=False),
                                    Item('clear', show_label=False),
                                   ),
                             Item('figure', editor=MPLFigureEditor(),
                             resizable=True, show_label=False),
                             label='plot sheet',
                             dock='tab',
                             )
                    ),
                    width=0.5,
                    height=0.4,
                    buttons=['OK', 'Cancel'],
                    resizable=True)
