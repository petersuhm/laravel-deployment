from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm
import time

code_dir = '/home/peter/deployment-test'
repo     = 'git@github.com:petersuhm/laravel-deployment.git'
timestamp = "release_%s" % int(time.time() * 1000)

def deploy():
    fetch_repo()
    run_composer()
    update_permissions()
    update_symlinks()

def fetch_repo():
    with cd(code_dir):
        with settings(warn_only=True):
            run("mkdir releases")
    with cd("%s/releases" % code_dir):
        run("git clone %s %s" % (repo, timestamp))

def run_composer():
    with cd("%s/releases/%s" % (code_dir, timestamp)):
        run("curl -sS https://getcomposer.org/installer | php")
        run("php composer.phar install")

def update_permissions():
    with cd("%s/releases/%s" % (code_dir, timestamp)):
        run("chmod 777 -R app/storage")

def update_symlinks():
    with cd(code_dir):
        current_release_path = "%s/releases/%s" % (code_dir, timestamp)
        run("ln -nfs %s current_release" % (current_release_path))