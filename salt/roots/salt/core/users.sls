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

