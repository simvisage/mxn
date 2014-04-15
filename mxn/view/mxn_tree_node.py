'''
Created on 14. 4. 2014

@author: Vancikv
'''

from traits.api import \
    HasStrictTraits, Str, List, WeakRef

from traitsui.api import \
    View

class MxNLeafNode(HasStrictTraits):
    '''Base class of all model classes that can appear in a tree node.
    '''
    node_name = Str('<unnamed>')

    def plot(self, fig):
        return

class MxNTreeNode(HasStrictTraits):
    '''Base class of all model classes that can appear in a tree node.
    '''
    node_name = Str('<unnamed>')

    tree_node_list = List([])

    tree_view = View()

    plot_state = WeakRef(transient=True)
    '''Allows for passing a reference to cross section
    to reinforcement layout node for purposes of plotting
    '''
    def __getstate__ (self):
        '''Overriding __getstate__ because of WeakRef usage
        '''
        state = super(HasStrictTraits, self).__getstate__()

        for key in [ 'plot_state', 'plot_state_' ]:
            if state.has_key(key):
                del state[ key ]

        return state

    def plot(self, fig):
        if self.plot_state:
            ax = fig.add_subplot(1, 1, 1)
            self.plot_state.plot_geometry(ax)
        return
