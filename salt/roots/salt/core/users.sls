# User and Group settings
create_group:
  group.present:
    - name: {{ pillar['system']['group'] }}

create_user:
  user.present:
    - name: {{ pillar['system']['user'] }}
    - fullname: {{ pillar['system']['user'] }}
    - shell: /bin/bash
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

#alias para facilitar el debug
bash_aliases:
   file.managed:
     - source: salt://core/scripts/bash_aliases
     - name: {{ pillar['system']['home'] }}/.bash_aliases
     - mode: 644
     - user: {{ pillar['system']['user'] }}
     - group: {{ pillar['system']['group'] }}
     - template: jinja
