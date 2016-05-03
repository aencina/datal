{% set user = pillar['system']['user'] %}
{% set group = pillar['system']['group'] %}

include:
  - core.nginx.init

datastore_site:
  file.managed:
    - name: /etc/nginx/sites-available/datastore
    - source: salt://apps/datastore/datastore
    - template: jinja

datastore_site_enabled:
  file.symlink:
    - target: /etc/nginx/sites-available/datastore
    - name: /etc/nginx/sites-enabled/datastore

# Create data store resources directory
datastore_resources_dir:
  file.directory:
    - name: {{ salt['user.info'](user).home }}/{{ pillar['datastore']['sftp']['remote_base_folder'] }}
    - user: {{ user }}
    - group: {{ group }}
    - mode: 755
    - makedirs: True

datastore_resources_temp_dir:
  file.directory:
    - name: {{ salt['user.info'](user).home }}/{{ pillar['datastore']['sftp']['remote_base_folder'] }}/{{ pillar['datastore']['temporary_bucket'] }}
    - user: {{ user }}
    - group: {{ group }}
    - mode: 755
    - makedirs: True

datastore_resources_base_dir:
  file.directory:
    - name: {{ salt['user.info'](user).home }}/{{ pillar['datastore']['sftp']['remote_base_folder'] }}/{{ pillar['datastore']['bucket'] }}
    - user: {{ user }}
    - group: {{ group }}
    - mode: 755
    - makedirs: True

root_bucket:
  file.symlink:
    - name: /{{ pillar['datastore']['bucket'] }}
    - target: {{ salt['user.info'](user).home }}/{{ pillar['datastore']['sftp']['remote_base_folder'] }}/{{ pillar['datastore']['bucket'] }}

temp_root_bucket:
  file.symlink:
    - name: /{{ pillar['datastore']['temporary_bucket'] }}
    - target: {{ salt['user.info'](user).home }}/{{ pillar['datastore']['sftp']['remote_base_folder'] }}/{{ pillar['datastore']['temporary_bucket'] }}

# For fixed uploaded file for theme
{{ pillar['system']['home'] }}/{{ pillar['datastore']['sftp']['remote_base_folder'] }}/{{ pillar['datastore']['cdn_bucket'] }}/1:
  file.directory:
    - user: {{ user }}
    - group: {{ group }}
    - mode: 755
    - makedirs: True

fixed_image:
  file.managed:
    - name: {{ pillar['system']['home'] }}/{{ pillar['datastore']['sftp']['remote_base_folder'] }}/{{ pillar['datastore']['cdn_bucket'] }}/1/datal-portada.jpg
    - source: salt://apps/datastore/datal-portada.jpg
    - user: {{ user }}
    - group: {{ group }}
