local_hosts:
  host.present:
    - ip: 127.0.0.1
    - names:
      - '*.api.dev'
      - api.dev
      - admin.dev
      - workspace.dev
      - '*.microsites.dev'
      - microsites.dev
      - microsite.dev
      - datastore.dev

system_tools:
  pkg.installed:
    - pkgs:
      - vim
      - unzip
      - python-software-properties
      - gettext
      - git
      - libxslt1-dev
      - libxml2-dev