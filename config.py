# -*- coding: UTF-8 -*-

import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY='set a secret key here'
  DEBUG = True
  DEF_LANGUAGE = 'en'
  LANGUAGES = {
      'en': {
          'LANG_CODE':'en2',
          'OLD_CODES':['en', 'en1']
      },
      'fr': {
          'LANG_CODE':'fr',
          'OLD_CODES':[None]
      }
  }

  @staticmethod
  def init_app(app):
    pass

class TestingConfig(Config):
  TESTING = False

class ProductionConfig(Config):
  pass

config = {
  'testing' : TestingConfig,
  'production': ProductionConfig
}
