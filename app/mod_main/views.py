# -*- coding: UTF-8 -*-

# -*- coding: UTF-8 -*-

from . import mod_main
from flask import render_template, flash,redirect, request,url_for,g, current_app,session, abort
from config import Config
from gettext import gettext

@mod_main.before_request
def before_mod_man_request():
    print("mod_main.before_request")

@mod_main.url_defaults
def add_language_code(endpoint, values):
    '''
    if current_app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code
        #g.lang_code = session['lang_code']
    '''
    values.setdefault('lang_code', g.lang_code)


@mod_main.url_value_preprocessor
def pull_lang_code(endpoint, values):
    print("mod_main.url_value_preprocessor")
'''
    lang_code = values.pop('lang_code')
    g.lang_code = lang_list[lang_codes.index(lang_code)]
'''

@mod_main.route('/',methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')


@mod_main.route('/change/<new_lang_code>')
def change(new_lang_code):
    session['lang_code']=new_lang_code
    return redirect(url_for('main.index'))
