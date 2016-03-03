nodejs:
  pkgrepo.managed:
    - humanname: NodeJS Repository
    - dist: trusty
    - file: /etc/apt/sources.list.d/nodejs.list
    - name: "deb http://ppa.launchpad.net/chris-lea/node.js/ubuntu trusty main"

  pkg.installed:
    - require:
      - pkgrepo: nodejs

