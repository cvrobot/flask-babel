# -*- coding: UTF-8 -*-

import os
from app import create_app
from flask_script import Manager, Shell, Server

app=create_app('testing')
manager = Manager(app)

def make_shell_context():
  return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", Server(host="0.0.0.0", port=8088))


if __name__ == '__main__':
    manager.run()
