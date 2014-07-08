'''
Created on 14. 4. 2014

@author: Vancikv
'''

from traitsui.api import \
    Handler

from traitsui.menu import \
    Action

from traitsui.file_dialog import \
    open_file, save_file

# from mxn.utils import \
#     get_outfile

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

class MxNTreeViewHandler(Handler):
    '''Handler for MxNTreeView class
    '''
    def plot_node(self, info, node):
        '''Handles context menu action Plot for tree nodes
        '''
        info.object.figure.clear()
        node.plot(info.object.figure)
        info.object.data_changed = True

    def menu_save(self, info):
        file_name = save_file()  # file_name=get_outfile(folder_name='.mxn', file_name='')
        pickle.dump(info.object.root, open(file_name, 'wb'), 1)

    def menu_open(self, info):
        file_name = open_file()
        info.object.root = pickle.load(open(file_name, 'rb'))
