#-------------------------------------------------------------------------------
#
# Copyright (c) 2009, IMB, RWTH Aachen.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in simvisage/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.simvisage.com/licenses/BSD.txt
#
# Thanks for using Simvisage open source!
#
# Created on Aug 7, 2009 by: rchx

from traits.api import \
    TraitType, HasTraits, TraitError, \
    Bool, Property, Button

from traitsui.api import \
     View, Item, InstanceEditor, EnumEditor

from mxn.reinf_laws import \
     ReinfLawBase, ReinfLawFBM

class KeyRef(TraitType):

    def __init__(self, default=None, db=None, keys=None, **metadata):
        self._database = db
        self._default = default
        self._keys = keys
        super(KeyRef, self).__init__(**metadata)

    def validate(self, object, name, value):
        ''' Set the trait value '''
        if value in self._database.keys():
            new_value = value
        else:
            raise TraitError, 'assigned value must be one of %s but a value of %s was provided' % \
                (self._database.keys(), value)
        return new_value

    def get_default_value(self):
        '''Take the default value'''
        if self._default in self._database.keys():
            value = self._default
        else:
            raise TraitError, 'assigned default value must be one of %s but a value of %s was provided' % \
                (self._database.keys(), self._default)
        return (0, value)

    ref_keys = Property
    def _get_ref_keys(self):
        return self._database.keys()

    def get_editor (self, trait=None):
        return self.create_editor()

    def create_editor(self):
        return EnumEditor(name=self._keys)  # ## added by RCH
        return EnumEditor(values=self._database.keys())

if __name__ == '__main__':

    class UseKeyRef(HasTraits):
        '''Testclass containing attribute of type KeyRef
        '''
        new_law = Button
        def _new_law_fired(self):
            '''Adds a new fbm law to database and sets it as
            value of the ref attribute
            '''
            print self.ref.ref_keys
            law_name = 'new_fbm_law_1'
            count = 1
            while ReinfLawBase.db.get(law_name, None):
                count += 1
                law_name = 'new_fbm_law_' + str(count)
            ReinfLawBase.db[law_name] = ReinfLawFBM()
            self.ref = law_name

            v = self.trait_view()
            v.updated = True
            '''View gets updated to acknowledge the change in database
            '''

        del_law = Button
        def _del_law_fired(self):
            '''Deletes currently selected law from database
            '''
            law_name = self.ref
            self.ref = 'fbm-default'
            ReinfLawBase.db.__delitem__(key=law_name)

            v = self.trait_view()
            v.updated = True
            '''View gets updated to acknowledge the change in database
            '''

        reinf_law_keys = Property
        def _get_reinf_law_keys(self):
            return ReinfLawBase.db.keys()

        ref = KeyRef(default='fbm-default', db=ReinfLawBase.db, keys='reinf_law_keys')
        traits_view = View(Item('ref', style='simple'),
                           Item('new_law'),
                           Item('del_law'),
                          resizable=True)

    ukr = UseKeyRef()

    ukr.configure_traits()
    '''View the testclass - the default database keys
    are available in the dropdown list.
    '''

    ReinfLawBase.db['FBM_keyref_test'] = ReinfLawFBM()
    '''Adding a new item to database.
    '''

    ukr.ref = 'FBM_keyref_test'
    '''Attribute of the testclass set to the new value.
    '''

    ukr.configure_traits()
    '''View the testclass - dropdown list should include
    the new database item.
    '''

    del ReinfLawBase.db['FBM_keyref_test']
    ukr.ref = 'fbm_keyref_test'
    '''New item got deleted - further attempt at
    referencing it raises an error.
    '''
