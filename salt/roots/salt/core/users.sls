{% set environment = salt['pillar.get']('environment', None) %}

# User and Group settings
create_group:
  group.present:
    - name: {{ pillar['system']['group'] }}

create_user:
  user.present:
    - name: {{ pillar['system']['user'] }}
    - fullname: {{ pillar['system']['user'] }}
    - shell: /bin/bash
    {% if environment == 'dev' %}
    - enforce_password: True
    - password: {{ pillar['system']['user_password_hash'] }}
    {% endif %}
    - home: {{ pillar['system']['home'] }}
    - groups:
      - {{ pillar['system']['group'] }}

# bashrc monono
bash_rc:
   file.managed:
     - source: salt://core/scripts/bashrc
     - name: {{ pillar['system']['home'] }}/.bashrc
     - mode: 644
     - user: {{ pillar['system']['user'] }}
     - group: {{ pillar['system']['group'] }}


