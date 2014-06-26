'''
Created on 26. 6. 2014

@author: Vancikv
'''

from traits.api import \
    Instance, Button, Str

from traitsui.api import \
    View, Item, HGroup, Handler, spring, UIInfo

class MxNClassExtHandler(Handler):
    '''Handles adding and removing of ReinfFabric database
    objects through user interface.
    '''

    # The UIInfo object associated with the view:
    info = Instance(UIInfo)

    ok = Button('OK')
    delete = Button('OK')
    cancel = Button('Cancel')

    material_name = Str

    # The pop-up customization view:
    new_view = View(
        HGroup(
            spring,
            Item('material_name'),
            Item('ok', show_label=False),
            Item('cancel', show_label=False),
        ),
        kind='popup'
    )

    # Event handlers:
    def object_new_material_changed (self, info):
        if info.initialized:
            self.info = info
            self._ui = self.edit_traits(parent=info.new_material.control, view='new_view')

    def _ok_fired (self):
        object = self.info.object
        if self.material_name == '':
            print 'Please enter material name!'
        elif object.get(self.material_name, None):
            print 'Material name already occupied!'
        else:
            object[self.material_name] = object.klass()
            self._ui.dispose()
            self.info.ui.parent.updated = True

    def _cancel_fired (self):
        self._ui.dispose()
