#! /usr/bin/python
import apt
import sys

from subprocess import call

SALT_INSTALLER_COMMAND = "curl -L https://bootstrap.saltstack.com | sudo sh"
python_git_pkg = 'python-git'

def install_salt():
    print("Instalando SaltStack / Installing SaltStack")
    return call(SALT_INSTALLER_COMMAND, shell=True)

install_salt()

# Update APT Cache
cache = apt.cache.Cache()
cache.update()

pkg = cache[python_git_pkg]
if pkg.is_installed:
    print "{pkg_name} already installed".format(pkg_name=python_git_pkg)
else:
    pkg.mark_install()

    try:
        cache.commit()
    except Exception, arg:
        print >> sys.stderr, "Sorry, package installation failed [{err}]".format(err=str(arg))
