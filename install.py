#! /usr/bin/python

from subprocess import call

SALT_INSTALLER_COMMAND = "curl -L https://bootstrap.saltstack.com | sudo sh"


def install_salt():
    print("Instalando SaltStack / Installing SaltStack")
    return call(SALT_INSTALLER_COMMAND, shell=True)

install_salt()
