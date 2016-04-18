nodejs:
  pkgrepo.managed:
    - humanname: NodeJS Repository
    - ppa: chris-lea/node.js
    - dist: trusty
  pkg.installed:
    - require:
      - pkgrepo: nodejs
