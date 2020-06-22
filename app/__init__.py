# -*- coding: UTF-8 -*-

import os
from flask import Flask, g, request, flash, redirect, session, current_app, abort
from config import config
from flask_babel import Babel

babel = Babel()

def create_app(config_name):
    app = Flask(__name__)


    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    babel.init_app(app)

    from .mod_main import mod_main as main_blueprint
    app.register_blueprint(main_blueprint,url_prefix='/<lang_code>')

    # If someone navigates to the site domain without the lang code
    # we append the lang code to the request url and redirect
    @app.before_request
    def before_request():
        print("before_request full_path:{}".format(request.full_path))
        print("request.view_args:{}".format(request.view_args))
        lang_codes = [value['LANG_CODE']  for l, value in current_app.config['LANGUAGES'].items()]
        old_codes_list = [value['OLD_CODES']  for l, value in current_app.config['LANGUAGES'].items()]
        lang_list = list(current_app.config['LANGUAGES'].keys())

        #return
        # filter static for develop
        url = request.full_path.split('/')
        for m in ['favicon.ico','robots.txt','static']:
            if url[1] == 'robots.txt':
                abort(404)
            if url[1].startswith(m):
                return

        # no view_args if last '/' of /lang'/' not exit
        #if request.view_args == None:
        if url[1] == '?':
            # root path, reredict according to request location or default config
            lang = request.accept_languages.best_match(current_app.config['LANGUAGES'].keys()) or current_app.config['DEF_LANGUAGE']
            lang_code = lang_codes[lang_list.index(lang)]
            return redirect( lang_code + request.full_path, 301)
        else:
            #may no need check due to prefix in blueprint 
            if request.view_args is not None and 'lang_code' in request.view_args:
                request.view_args.pop('lang_code')

            lang_code = url[1] if url[1][-1] != '?' else url[1][:-1]
            
            print("request.full_path:{} lang_code:{}".format(request.full_path, lang_code))
            #lang_code in latest url list 
            if lang_code in lang_codes:
                if request.view_args == None:
                    redirect(request.full_path + '/', 301)
                # lang corredt just set lang code
                g.lang_code = lang_list[lang_codes.index(lang_code)]
                return

            # old urls, redict to new urls
            for i in range(len(lang_list)):
                if lang_code in old_codes_list[int(i)]:
                    full_path = request.full_path.split('/')
                    full_path[1] = lang_codes[int(i)]
                    full_path = '/'.join(map(str, full_path))
                    print("full_path:{} request.full_path:{} new lang_code:{}".format(full_path, request.full_path, lang_codes[int(i)]))
                    return redirect(full_path, 301)

            # lang code  not correct
            lang = request.accept_languages.best_match(current_app.config['LANGUAGES'].keys()) or current_app.config['DEF_LANGUAGE']
            lang_code = lang_codes[lang_list.index(lang)]

            return redirect( '/' + lang_code + request.full_path, 301)
    '''
    @app.before_request
    def before_request():
        u = request.full_path.split('/')
        print("before_request u:{} u[1]:{} full_path:{}".format(u, u[1], request.full_path))

        lang_urls = [value['LANG_URL']  for l, value in current_app.config['LANGUAGES'].items()]
        old_urls_list = [value['OLD_URLS']  for l, value in current_app.config['LANGUAGES'].items()]
        lang_list = list(current_app.config['LANGUAGES'].keys())
    
        for m in ['favicon.ico','robots.txt','static']:
            if u[1] == 'robots.txt':
                abort(404)
            if u[1].startswith(m):
                return
        lang_url = u[1]
        
        print("before_request u:{} lang_urls:{} lang_url:{}".format(u, lang_urls, lang_url))
        if lang_url in lang_urls:
            # lang corredt just set lang code
            g.lang_code = 'en'#lang_list[lang_urls.index(lang_url)]
            return
        elif u[1] == '?':
            # root path, redict according to request or default config
            l = request.accept_languages.best_match(current_app.config['LANGUAGES'].keys()) or current_app.config['DEF_LANGUAGE']
            print("l + request.full_path:{}{}".format(l, request.full_path))
            return redirect( l + request.full_path, 301)
        else:
            # old urls, redict to new urls
            for i in range(len(lang_list)):
                if lang_url in old_urls_list[int(i)]:
                    u[1] = lang_urls[int(i)]
                    return redirect( '/'.join(map(str, u)), 301)
                  
            # lang not correct    
            u[1] = request.accept_languages.best_match(current_app.config['LANGUAGES'].keys()) or current_app.config['DEF_LANGUAGE']
            print('/'.join(map(str, u)))
            return redirect( '/'.join(map(str, u)), 301)

        in u[1] in current_app.config['DEF_LANGUAGE']
        if 'lang_code' not in g:
            l = request.accept_languages.best_match(current_app.config['LANGUAGES'].keys()) or current_app.config['DEF_LANGUAGE']
            return redirect( l + request.full_path, 301)
        else:
            print(g.lang_code)

            print(g.lang_code)
        if request.view_args==None:
            if not 'lang_code' in session.keys():
                return redirect('/fr' + request.full_path)
      '''


    @app.context_processor
    def inject_lang():
        if 'lang_code' not in g:
            print("context_processor no g.lang_code")

        #return dict(sess_lang=session['lang_code'])
        if request.full_path:
            url = (request.full_path if request.full_path[-1] != '?' else request.full_path[:-1]).split('/')
            route_url = '/' + '/'.join(map(str, url[2:]))
        else:
            route_url = '/'

        print("context_processor g.lang_code:{}, route_url:{}".format(g.lang_code, route_url))
        return dict(sess_lang=g.lang_code, route_url=route_url)

    @babel.localeselector
    def get_locale():
        print("get_local {}".format(g.lang_code))
        #session['lang_code']=request.accept_languages.best_match()
        #g.lang_code = session['lang_code']
        #return g.get('lang_code', 'fr')
        return g.lang_code

    return app
