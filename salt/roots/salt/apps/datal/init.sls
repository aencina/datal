{% set environment = salt['pillar.get']('environment', None) %}
{% set install_dir = salt['pillar.get']('application:install_dir', None) %}
{% set user = pillar['system']['user'] %}
{% set group = pillar['system']['group'] %}

include:
  - core.users
  - core.python
  - core.uwsgi
  - core.memcached
  - core.git
  {% if environment == 'demo' or environment == 'staging' or environment == 'test' or environment == 'prod' %}
  - core.github_bot
  {% endif %}
  - core.bower
  - apps.datal.uwsgi.init
  - apps.datal.supervisor.init
  - apps.datal.nginx.init

raven:
  pip.installed

mysql_datal_deps:
  pkg.installed:
    - refresh: True
    - pkgs:
      - libmysqlclient-dev
      - python-mysqldb

pillow_datal_deps:
  pkg.installed:
    - refresh: True
    - pkgs:
      - libjpeg-dev

{% if environment == 'demo' or environment == 'staging' or environment == 'test' %}
clean_caches:
  cmd.run:
    - names:
      - echo 'flush_all' | nc localhost 11211
      - redis-cli FLUSHALL
{% endif %}

# Set directory environment owner
directory_structure:
  file.directory:
    - name: {{install_dir}}{{ pillar['virtualenv']['path'] }}
    - user: {{ user }}
    - group: {{ group }}
    - follow_symlinks: False
    - recurse:
      - user

{% if environment == 'dev' %}
local_hosts:
  host.present:
    - ip: 127.0.0.1
    - names:
      - workspace.dev
      - microsites.dev
      - api.dev
      - admin.dev
      - datastore.dev
{% endif %}

# Bien feo esto, mejoralo!
{% if environment == 'prod' %}
local_hosts:
  host.present:
    - ip: 127.0.0.1
    - names:
      - workspace.local
      - microsites.local
{% endif %}

{% if environment == 'demo' or environment == 'staging' or environment == 'test' or environment == 'prod' %}
app_directory_structure:
  file.directory:
     - name: {{install_dir}}{{ pillar['application']['path'] }}
     - user: {{user}}
     - group: {{group}}
     - makedirs: True

datal_code:
  git.latest:
    - name: {{ pillar['application']['git']['datal_repo'] }}
    - rev: {{ pillar['application']['git']['branch'] }}
    - target: {{install_dir}}{{ pillar['application']['path'] }}
    - force_checkout: True
    - force: True
    - force_reset: True
    - user: {{user}}
    - require:
       - user: {{user}}
       - group: {{group }}
       - ssh_known_hosts: github.com
       - file: {{ pillar['system']['home'] }}/.ssh/id_rsa.pub
       - file: {{ pillar['system']['home'] }}/.ssh/id_rsa

junar_code:
  git.latest:
    - name: {{ pillar['application']['git']['junar_repo'] }}
    - rev: {{ pillar['application']['git']['branch'] }}
    - target: {{install_dir}}{{ pillar['application']['path'] }}/plugins
    - force_checkout: True
    - force: True
    - force_reset: True
    - user: {{user}}
    - require:
       - user: {{user}}
       - group: {{group }}
       - ssh_known_hosts: github.com
       - file: {{ pillar['system']['home'] }}/.ssh/id_rsa.pub
       - file: {{ pillar['system']['home'] }}/.ssh/id_rsa
{% endif %}

# Create static files directory
{{install_dir}}{{ pillar['application']['statics_dir'] }}:
  file.directory:
    - user: {{ user }}
    - group: {{ group }}
    - mode: 755
    - makedirs: True

# Create data store resources directory
{{ pillar['system']['home'] }}/{{ pillar['datastore']['sftp']['remote_base_folder'] }}:
  file.directory:
    - user: {{ user }}
    - group: {{ group }}
    - mode: 755
    - makedirs: True

# Create data store temporary directory
{{ pillar['system']['home'] }}/{{ pillar['datastore']['sftp']['local_tmp_folder'] }}:
  file.directory:
    - user: {{ user }}
    - group: {{ group }}
    - mode: 755
    - makedirs: True

# Create virtual environment
create_env:
  virtualenv.managed:
    - name: {{install_dir}}{{ pillar['virtualenv']['path'] }}
    - system_site_packages: False
    - requirements: {{install_dir}}{{ pillar['virtualenv']['requirements'] }}
    - user: {{ user }}

# Activate virtualenv on login
/home/{{ user }}/.bashrc:
  file.append:
    - text:
      - "source {{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/activate"
      - "cd {{install_dir}}{{ pillar['application']['path'] }}"

local_settings:
  file.managed:
    - name: {{install_dir}}{{ pillar['application']['path'] }}/core/local_settings.py
    - source: salt://apps/datal/local_settings_base.py
    - template: jinja
    - user: {{ pillar['system']['user'] }}
    - group: {{ pillar['system']['group'] }}

local_settings_workspace:
  file.managed:
    - name: {{install_dir}}{{ pillar['application']['path'] }}/workspace/local_settings.py
    - source: salt://apps/datal/local_settings_workspace.py
    - template: jinja
    - user: {{ pillar['system']['user'] }}
    - group: {{ pillar['system']['group'] }}

local_settings_api:
  file.managed:
    - name: {{install_dir}}{{ pillar['application']['path'] }}/api/local_settings.py
    - source: salt://apps/datal/local_settings_api.py
    - template: jinja
    - user: {{ pillar['system']['user'] }}
    - group: {{ pillar['system']['group'] }}

local_settings_microsites:
  file.managed:
    - name: {{install_dir}}{{ pillar['application']['path'] }}/microsites/local_settings.py
    - source: salt://apps/datal/local_settings_microsites.py
    - template: jinja
    - user: {{ pillar['system']['user'] }}
    - group: {{ pillar['system']['group'] }}

bower_install:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; CI=true bower install

sync_db:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py syncdb --noinput --settings=core.settings
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py syncdb --noinput --settings=admin.settings
      # - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py syncdb --noinput --settings=api.settings
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py syncdb --noinput --settings=microsites.settings
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py syncdb --noinput --settings=workspace.settings

migrate_db:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py migrate --settings=core.settings
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py migrate --settings=admin.settings

{% if environment != 'prod' %}
fixtures:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py loaddata  core/fixtures/* --settings=core.settings
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py loaddata  admin/fixtures/* --settings=admin.settings
{% endif %}

{% if environment == 'demo' or environment == 'staging' or environment == 'test' %}
environment_fixtures:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py loaddata  plugins/fixtures/{{ environment }}/* --settings=core.settings
{% endif %}

{% if environment != 'prod' %}
plugins_fixtures:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py loaddata  plugins/dashboards/fixtures/* --settings=core.settings
{% endif %}

cleanpython:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - find -iname "*.py[co]" -exec rm -f {} \;

sync_plugins:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py syncplugins --settings=core.settings

language:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py compilemessages --settings=workspace.settings
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py compilemessages --settings=microsites.settings

core_statics:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py collectstatic --settings=core.settings --noinput

microsites_statics:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py collectstatic --settings=microsites.settings --noinput

workspace_statics:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py collectstatic --settings=workspace.settings --noinput

{% if environment != 'dev' and environment != 'staging' %}
core_sass:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py compilescss --settings=core.settings 

microsites_sass:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py compilescss --settings=microsites.settings 

workspace_sass:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py compilescss --settings=workspace.settings 
{% endif %}

/tmp/datal.log:
  file.managed:
    - user: {{ user }}
    - group: {{ group }}
    - mode: 777

{% if environment != 'prod' %}
reindex:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py index --settings=workspace.settings --all --flush --debug

log_activity:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{install_dir}}{{ pillar['application']['path'] }}
    - names:
      - PATH="{{install_dir}}{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py log_activity --settings=workspace.settings

{% endif %}

uwsgi:
  service.running:
    - require:
      - pkg: uwsgi
    - watch:
      - file: /etc/uwsgi/admin.ini
      - file: /etc/uwsgi/api.ini
      - file: /etc/uwsgi/microsite.ini
      - file: /etc/uwsgi/workspace.ini

supervisord_service:
  service.running:
    - name: supervisor
    - require:
      - pkg: supervisor
    - watch:
      - file: /etc/supervisor/supervisord.conf
      - file: /etc/supervisor/conf.d/uwsgi.conf
      - file: /etc/uwsgi/admin.ini
      - file: /etc/uwsgi/api.ini
      - file: /etc/uwsgi/microsite.ini
      - file: /etc/uwsgi/workspace.ini
      - file: /tmp/datal.log

uwsgi_service:
  supervisord.running:
    - name: uwsgi
    - restart: True
