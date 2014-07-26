# -*-*- encoding: utf-8 -*-*-

import sys
import json
import datetime
import uuid
import hashlib
import urllib2
import requests

from flask.ext.wtf import TextField, PasswordField, Required, URL, ValidationError

from labmanager.forms import AddForm
from labmanager.rlms import register, Laboratory, Capabilities
from labmanager.rlms.base import BaseRLMS, BaseFormCreator, Versions

class ViSHAddForm(AddForm):

    DEFAULT_LOCATION = 'Europe'
    DEFAULT_URL = 'http://vishub.org/'

    def __init__(self, add_or_edit, *args, **kwargs):
        super(ViSHAddForm, self).__init__(*args, **kwargs)
        self.add_or_edit = add_or_edit

class ViSHFormCreator(BaseFormCreator):

    def get_add_form(self):
        return ViSHAddForm

FORM_CREATOR = ViSHFormCreator()

class RLMS(BaseRLMS):

    def __init__(self, configuration):
        self.configuration = json.loads(configuration or '{}')

    def get_version(self):
        return Versions.VERSION_1

    def get_capabilities(self):
        return [ Capabilities.WIDGET ] 

    def get_laboratories(self):
        # TODO
        return [ Laboratory('testing', 'testing', autoload = True) ]

    def reserve(self, laboratory_id, username, institution, general_configuration_str, particular_configurations, request_payload, user_properties, *args, **kwargs):
        # TODO
        return {
            'reservation_id' : '',
            'load_url' : ''
        }

    def list_widgets(self, laboratory_id, **kwargs):
        # TODO
        return [ 
                dict(name = u'foo', description = u'foo', height = '900px')
            ]

    def load_widget(self, reservation_id, widget_name, **kwargs):
        # TODO
        return {
            'url' : 'foo'
        }

register("ViSH", ['1.0'], __name__)
