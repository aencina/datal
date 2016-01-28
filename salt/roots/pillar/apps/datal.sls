application:
  path: /home/vagrant/app
  statics_dir: /home/vagrant/static
  cdn: 'datastore.dev:8888/resources/datal_cdn/'
  api_key: '576bba0dd5a27df9aaac12d1d7ec25c8411fe29e'
  public_key: '9d6508cced6919e1a132d47d9c85896132aaf516'

  settings:
    # Base Django Settings
    secret_key: '1'
    root_urlconf: 'workspace.urls'

    pagination_results_per_page: 10

    domains:
      microsites: 'microsites.dev:8080'
      workspace: 'workspace.dev:8080'
      api: 'api.dev:8080'
      datastore: 'datastore.dev:8888'

    domains_engine:
      microsites: 'microsites.dev:8080'
      workspace: 'workspace.dev:8080'
      api: 'api.dev:8080'
      

virtualenv:
  path: /home/vagrant/env
  requirements: /home/vagrant/app/requirements.txt

searchers:
  searchify:
    api_url: 'http://localhost:20220'
    index: 'idx'

email:
    host: ''
    port: ''
    user: ''
    password: ''
    tls: True

sentry_dns: ''

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