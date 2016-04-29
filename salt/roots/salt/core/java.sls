debconf-utils:
  pkg.installed

oracle-java7-installer:
  pkgrepo.managed:
    - humanname: WebUp8Team Java Repository
    - name: "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main"
    - dist: trusty
    - file: /etc/apt/sources.list.d/webup8team.list
    - keyid: EEA14886
    - keyserver: keyserver.ubuntu.com
  pkg.installed:
    - require:
      - pkgrepo: oracle-java7-installer
  debconf.set:
   - data:
       'shared/accepted-oracle-license-v1-1': {'type': 'boolean', 'value': True}
   - require_in:
       - pkg: oracle-java7-installer
