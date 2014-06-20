'''
Created on 13. 5. 2014

@author: Vancikv
'''

from traits.api import \
    Instance, Button, Str

from traitsui.api import \
    View, Item, HGroup, Handler, spring, UIInfo

from mxn.reinf_laws import \
    ReinfFabric

class FabricHandler(Handler):
    '''Handles adding and removing of ReinfFabric database
    objects through user interface.
    '''

    # The UIInfo object associated with the view:
    info = Instance(UIInfo)

    ok = Button('OK')
    delete = Button('OK')
    cancel = Button('Cancel')

    fabric_name = Str

    # The pop-up customization view:
    new_view = View(
        HGroup(
            spring,
            Item('fabric_name'),
            Item('ok', show_label=False),
            Item('cancel', show_label=False),
        ),
        kind='popup'
    )

    del_view = View(
        HGroup(
            spring,
            Item(name='', label='Really delete?'),
            Item('delete', show_label=False),
            Item('cancel', show_label=False),
        ),
        kind='popup'
    )

    # Event handlers:
    def xobject_new_fabric_changed (self, info):
        if info.initialized:
            self.info = info
            self._ui = self.edit_traits(parent=info.new_fabric.control, view='new_view')

    def xobject_del_fabric_changed (self, info):
        if info.initialized:
            self.info = info
            self._ui = self.edit_traits(parent=info.del_fabric.control, view='del_view')

    def x_ok_fired (self):
        object = self.info.object
        if self.fabric_name == '':
            print 'Please enter fabric name!'
        elif ReinfFabric.db.get(self.fabric_name, None):
            print 'Fabric name already occupied!'
        else:
            ReinfFabric.db[self.fabric_name] = ReinfFabric()
            object.fabric = self.fabric_name
            self._ui.dispose()
            self.info.ui.parent.updated = True

    def x_delete_fired (self):
        object = self.info.object
        ReinfFabric.db.__delitem__(key=object.fabric)
        object.fabric = ReinfFabric.db.inst_list[0].key
        self._ui.dispose()
        self.info.ui.parent.updated = True

    def x_cancel_fired (self):
        self._ui.dispose()
