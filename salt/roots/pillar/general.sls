# General settings
system:
  user: vagrant
  group: vagrant
  home: /home/vagrant
  # V8
  processors: 2

nginx:
  server:
    sendfile: 'off'
  vhosts:
    admin:
      name: admin.dev
    api:
      name: api.dev *.api.dev
    microsites:
      name: microsites.dev *.microsites.dev
    workspace:
      name: workspace.dev
      
# Searcher
searchers:
  searchify:
    api_url: 'http://localhost:20220'
    index: 'idx'
  elastic:
    url: 'http://localhost:9200'
    index: 'datal'

sentry_dns: ''
sentry_dns_microsites: ''
sentry_dns_workspace: ''
sentry_dns_api: ''

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

# General
datastore:
  use: 'sftp'
  bucket: 'datal'
  temporary_bucket: 'datal_temp'
  cdn_bucket: 'datal_cdn'
  sftp:
    host: 'localhost'
    port: 22
    user: vagrant
    password: datal
    privateKey:
    passphrase:
    remote_base_folder: datastore/resources/
    local_tmp_folder: datastore/tmp/
    public_base_url: 'http://datastore.dev:8888/resources'

# Amazon settings
amazon:
  accesskey: ''
  secretkey: ''

domains:
  microsites: 'microsites.dev'
  workspace: 'workspace.dev'
  api: 'api.dev'
  admin: 'admin.dev'

tomcat-manager:
  user: webappsuser
  passwd: 123456

java_opts:
  Xms: 512m
  Xmx: 1024m
  MaxPermSize: 512m
  PermSize: 256m
  G1HeapRegionSize: 512M
  Xss: 128m
  ParallelGCThreads: 0
  ConcGCThreads: 0

# Redis configuration
redis:
  read_host: localhost
  read_port: 6379
  write_host: localhost
  write_port: 6379

jaxer:
  endpoint: 'http://jaxer-balancer-383544228.us-west-1.elb.amazonaws.com:8081/agileoffice/AjaxScraper.html'

crawler:
  media: http://workspace.dev:8080/static/core/styles

scraper:
  maxcols: 50
  maxcolsever: 20
  maxrows: 100
  maxrowsbynode: 5000
  maxrowsever: 5000

xml:
  maxrowsbynode: 1000

reducer:
  maxcolsbyrow: 50

xls:
  maxrowsinmemory: 1000

processor:
  maxrows: 100
  maxcols: 50

alchemist:
  maxmarkers: 1000
  maxrows: 50

scrapper:
  proxy_scrapers_domain: 'http://workspace.dev:8080'

memcached:
  api: 127.0.0.1:11211
  microsites: 127.0.0.1:11211
  engine: 127.0.0.1:11211

email:
    host: ''
    port: ''
    user: ''
    password: ''
    tls: True

queues:
  request_queue: 'test_requests_queue'

social:
  twitter_profile_url: ''
  facebook_profile_url: ''

mail_list:
  list_company: ''
  list_description: ''
  list_unsubscribe: ''
  list_update_profile: ''
  welcome_template_es: ''
  welcome_template_en: ''
  mailchimp:
    uri: 'https://us2.api.mailchimp.com/2.0/'
    api_key: ''
    lists:
      workspace_users_list:
        es_id: ''
        en_id: ''
  mandrill:
    api_key: ''