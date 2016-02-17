base:
  '*':
    - base.system
    - base.nginx
    - apps.general
    - apps.v8
    - apps.datal
    {% if salt['file.file_exists']('/srv/salt/pillar/local.sls') %}
    - local
    {% endif %}