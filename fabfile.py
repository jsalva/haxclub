from __future__ import absolute_import
import os
import re
import json
from datetime import datetime, timedelta

from fabric.api import env, hide, settings, cd, lcd
from fabric.operations import local as lrun, run, sudo, put
from fabric.contrib.console import confirm
from fabric.tasks import execute
from fabric.context_managers import shell_env, prefix
from fabric.contrib.files import exists
from ilogue.fexpect import expect, expecting, run as erun
import pexpect
from fabric.api import task as _task

remote_requirements = os.path.abspath('requirements/base.txt')

def console(message):
    print '\n[+] %s\n' % message

def task(function):
    name = function.__name__
    def wrapped(*args,**kwargs):
        console('executing %s...' % name)
        return function(*args,**kwargs)

    wrapped.__name__ = name
    return _task(wrapped)

def parse_config(config_file):
    with open(config_file,'rb') as f:
        config = json.load(f)
    return config

def write_config(config_file, config_dict):
    config_str = json.dumps(config_dict, indent=4, sort_keys=True)

    with open(config_file, 'wb') as f:
        f.write(config_str)

    return parse_config(config_file)

config = parse_config('haxclub.conf')

@task
def local():
    env.run = erun
    env.hosts = ['localhost']

@task
def remote_setup():
    env.run = run
    env.key_filename = config.get('credentials').get('ssh_key_path')
    env.user = config.get('user')

    # make SURE python is 2.6; otherwise yum is dead.
    sudo('rm /usr/bin/python; ln -s /usr/bin/python2.6 /usr/bin/python;')

    # get updates
    sudo('yum update -y')

    # build tools
    sudo('yum install make automake gcc gcc-c++ kernel-devel git-core mysql mysql-server mysql-devel postgresql-devel patch ncurses ncurses-devel -y')

    # rabbitmq
    sudo('yum install rabbitmq-server --enablerepo=epel -y')

    # make sure python 2.7 is installed
    sudo('yum install python27-devel -y')

    python_27_dir = sudo('python27 -c "from distutils.sysconfig import get_python_lib;'\
        'print(get_python_lib())"')

    with cd(python_27_dir):
        sudo('wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | sudo python')
        sudo('easy_install pip')

    sudo('pip install virtualenv')
    sudo('pip install virtualenvwrapper')

    # install pip remote requirements (obtained from requirements/remote.txt)
    with cd('/tmp'):
        with prefix('source $(which virtualenvwrapper.sh) && workon remote'):
            put(remote_requirements,'requirements.txt')
            run('pip install -r requirements.txt')

    sudo('/etc/init.d/mysqld stop; /etc/init.d/mysqld start')
    sudo('rabbitmqctl stop; rabbitmq-server -detached',user='rabbitmq')

@task
def deploy():
    with prefix('source $(which virtualenvwrapper.sh) && workon remote'):
        settings_file = '--settings=haxclub.settings.base'
        env_vars = config.get('env_vars')
        if not exists('~/haxclub'):
            with cd('~/'):
                run('git clone https://github.com/jsalva/haxclub')
        with cd('~/haxclub/haxclub'):
            run('mkdir logs')
            run('git pull origin master')
            with shell_env(**env_vars):
                prompts = []
                prompts += expect("Type 'yes' to continue","yes")
                with expecting(prompts):
                    erun('python manage.py collectstatic %s' % settings_file)
                    erun('python manage.py migrate %s' % settings_file)
                    erun('python manage.py syncdb %s' % settings_file)
                    if exists('supervisord.pid'):
                        erun('python manage.py supervisor reload %s' % settings_file)
                    else:
                        erun('python manage.py supervisor --daemonize %s' % settings_file)

@task
def aws():
    env.hosts = config.get('aws_nodes')
    execute(remote_setup)

