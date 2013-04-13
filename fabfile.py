from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm

code_dir = '/home/peter/deployment-test'
repo     = 'git@github.com:petersuhm/laravel-deployment.git'

def deploy():
    with settings(warn_only=True):
        if run("cd %s" % code_dir).failed:
            run("git clone %s %s" % repo % code_dir)
    with cd(code_dir):
        run("git pull")
    run_composer()

def run_composer():
    with cd(code_dir):
        run("curl -sS https://getcomposer.org/installer | php")
        run("php composer.phar install")