# General settings
system:
  user: vagrant
  group: vagrant
  home: /home/vagrant

# Searcher
searchers:
  elastic:
    url: 'http://10.198.67.167:9200'
    index: 'datal'

application:
  install_dir: /home/vagrant/
  path: app
  cdn: 'datastore.dev:8888/resources/datal_cdn/'
  api_key: '576bba0dd5a27df9aaac12d1d7ec25c8411fe29e'
  public_key: '9d6508cced6919e1a132d47d9c85896132aaf516'
  statics_dir: static
  settings:
    secret_key: '1'
    debug: True
    root_urlconf: 'workspace.urls'
    workspace_protocol: 'http'
    domains:
      microsites: 'microsites.dev:8080'
      workspace: 'workspace.dev:8080'
      api: 'api.dev:8080'
      website: 'website.dev:8080'
    domains_engine:
      microsites: 'microsites.dev:8080'
      workspace: 'workspace.dev:8080'
      api: 'api.dev:8080'

virtualenv:
  path: env
  requirements: app/requirements.txt
  plugins_requirements: app/plugins/requirements.txt

database:
  user: datal
  name: ao_datal
  password: datal
  host: localhost
  port: 3306
  engine: mysql
  