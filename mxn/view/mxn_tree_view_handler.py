'''
Created on 14. 4. 2014

@author: Vancikv
'''

from traitsui.api import \
    TreeEditor, TreeNode, View, Item, Group, \
    HSplit, HGroup, Handler, UIInfo

from traitsui.menu import \
    Action

from traitsui.file_dialog import \
    open_file, save_file

from traits.api import \
    Button, Instance

from mxn.utils import \
    get_outfile

import pickle

plot_self = Action(name='Plot', action='plot_node')
'''Menu action for plotting tree nodes
'''
menu_save = Action(name='Save', action='menu_save')
'''Menubar action for saving the root node to file
'''
menu_open = Action(name='Open', action='menu_open')
'''Menubar action for loading root node from file
'''
menu_exit = Action(name='Exit', action='menu_exit')
'''Menubar action for terminating the view
'''

class MxNTreeViewHandler(Handler):
    '''Handler for MxNTreeView class
    '''
    # The UIInfo object associated with the view:
    info = Instance(UIInfo)

    ok = Button('OK')
    cancel = Button('Cancel')
    exit_dialog = ('Do you really wish to end '
                   'the session? Any unsaved data '
                   'will be lost.')

    exit_view = View(Item(name='', label=exit_dialog),
                     HGroup(Item('ok', show_label=False, springy=True),
                            Item('cancel', show_label=False, springy=True)
                            ),
                     title='Exit dialog',
                     kind='live'
                     )

    def plot_node(self, info, node):
        '''Handles context menu action Plot for tree nodes
        '''
        info.object.figure.clear()
        node.plot(info.object.figure)
        info.object.data_changed = True

    def menu_save(self, info):
        file_name = get_outfile(folder_name='.mxn', file_name='')
        file_ = save_file(file_name=file_name)
        pickle.dump(info.object.root, open(file_, 'wb'), 1)

    def menu_open(self, info):
        file_name = get_outfile(folder_name='.mxn', file_name='')
        file_ = open_file(file_name=file_name)
        info.object.root = pickle.load(open(file_, 'rb'))

    def menu_exit(self, info):
        if info.initialized:
            self.info = info
            self._ui = self.edit_traits(view='exit_view')

    def _ok_fired (self):
        self._ui.dispose()
        self.info.ui.dispose()

    def _cancel_fired (self):
        self._ui.dispose()
