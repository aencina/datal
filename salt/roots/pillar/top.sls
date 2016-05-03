base:
  '*':
    - general
    {% if salt['file.file_exists']('/srv/salt/pillar/local.sls') %}
    - local
    {% endif %}