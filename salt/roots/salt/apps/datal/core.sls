{% set user = pillar['system']['user'] %}
{% set group = pillar['system']['group'] %}

cleanpython:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{ pillar['application']['path'] }}
    - names:
      - find -iname "*.py[co]" -exec rm -f {} \;

{% if salt['grains.get']('os') == 'Debian' %}
install_ruby:
  pkg.installed:
    - names:
      - ruby
{% endif %}

sass_install:
  gem.installed:
    - name: sass

clean_caches:
  cmd.run:
    - names:
      - echo 'flush_all' | nc localhost 11211
      - redis-cli FLUSHALL

# Create static files directory
{{ pillar['application']['statics_dir'] }}:
  file.directory:
    - user: {{ user }}
    - group: {{ group }}
    - mode: 755
    - makedirs: True

# Create static components files directory
{{ pillar['application']['path'] }}/components/components:
  file.directory:
    - user: {{ user }}
    - group: {{ group }}
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

# Set directory owner
directory_structure:
  file.directory:
    - name: {{ pillar['virtualenv']['path'] }}
    - user: {{ user }}
    - group: {{ group }}
    - follow_symlinks: False
    - recurse:
      - user

# Create virtual environment
create_env:
  virtualenv.managed:
    - name: {{ pillar['virtualenv']['path'] }}
    - system_site_packages: False
    - requirements: {{ pillar['virtualenv']['requirements'] }}
    - user: {{ user }}

# Activate virtualenv on login
/home/{{ user }}/.bashrc:
  file.append:
    - text:
      - "source {{ pillar['virtualenv']['path'] }}/bin/activate"
      - "cd {{ pillar['application']['path'] }}"

local_settings:
  file.managed:
    - name: {{ pillar['application']['path'] }}/core/local_settings.py
    - source: salt://apps/datal/local_settings_base.py
    - template: jinja
    - user: {{ user }}
    - group: {{ group }}

sync_db:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{ pillar['application']['path'] }}
    - names:
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py syncdb --noinput --settings=core.settings
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py syncdb --noinput --settings=admin.settings
      # - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py syncdb --noinput --settings=api.settings
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py syncdb --noinput --settings=microsites.settings
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py syncdb --noinput --settings=workspace.settings

bower_install:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{ pillar['application']['path'] }}
    - names:
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; CI=true bower install

migrate_db:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{ pillar['application']['path'] }}
    - names:
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py migrate --settings=core.settings

fixtures:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{ pillar['application']['path'] }}
    - names:
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py loaddata  core/fixtures/* --settings=core.settings
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py loaddata  admin/fixtures/* --settings=admin.settings

language:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{ pillar['application']['path'] }}
    - names:
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py compilemessages --settings=workspace.settings
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py compilemessages --settings=microsites.settings

core_statics:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{ pillar['application']['path'] }}
    - names:
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py collectstatic --settings=core.settings --noinput

microsites_statics:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{ pillar['application']['path'] }}
    - names:
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py collectstatic --settings=microsites.settings --noinput

workspace_statics:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{ pillar['application']['path'] }}
    - names:
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py collectstatic --settings=workspace.settings --noinput

/tmp/datal.log:
  file.managed:
    - user: {{ user }}
    - group: {{ group }}
    - mode: 777

include:
  - apps.datal.uwsgi.init
  - apps.datal.supervisor.init

uwsgi_service:
  supervisord.running:
    - name: uwsgi
    - restart: True

reindex:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{ pillar['application']['path'] }}
    - names:
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py index --settings=workspace.settings --re-index

log_activity:
  cmd.run:
    - user: {{ user }}
    - group: {{ group }}
    - cwd: {{ pillar['application']['path'] }}
    - names:
      - PATH="{{ pillar['virtualenv']['path'] }}/bin/:$PATH"; python manage.py log_activity --settings=workspace.settings
