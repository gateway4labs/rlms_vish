# -*-*- encoding: utf-8 -*-*-

import sys
import json
import datetime
import uuid
import hashlib
import urllib2
import requests

from wtforms import validators
from flask.ext.wtf import TextField, PasswordField, Required, URL, ValidationError

from labmanager.forms import AddForm
from labmanager.rlms import register, Laboratory, Capabilities
from labmanager.rlms.base import BaseRLMS, BaseFormCreator, Versions

DEFAULT_SEARCH_TYPES = [ 'Excursion', 'Embed', 'Web application', 'Flash Object' ]
DEFAULT_NUMBER = 100

class ViSHAddForm(AddForm):

    DEFAULT_LOCATION = u'Europe'
    DEFAULT_URL = u'http://vishub.org/'

    number = TextField("Number of results", validators = [validators.NumberRange(min=1)], default = DEFAULT_NUMBER)
    search_types = TextField("Search types", description = "Separated by commas, those resources that will be displayed", default = ','.join(DEFAULT_SEARCH_TYPES)) 

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
        self.number = self.configuration.get('number', DEFAULT_NUMBER)
        self.search_types = self.configuration.get('search_types', ','.join(DEFAULT_SEARCH_TYPES))

    def get_version(self):
        return Versions.VERSION_1

    def get_capabilities(self):
        return [ Capabilities.WIDGET, Capabilities.FORCE_SEARCH ] 

    def get_laboratories(self):
        return []

    def search(self, query, page, **kwargs):
        final_query = "http://vishub.org/apis/search?type=%s&n=%s&q=%s" % (urllib2.quote(self.search_types), self.number, urllib2.quote(query))
        results = requests.get(final_query).json()
        laboratories = []
        for result in results:
            laboratories.append(Laboratory(name = u'%s - %s' % (result['type'], result['title']), laboratory_id = result['id'], description = result['description'], autoload = True))

        return {
            'total_results' : len(results),
            'pages' : 1,
            'laboratories' : laboratories,
        }

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
