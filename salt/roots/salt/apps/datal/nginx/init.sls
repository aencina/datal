{% set environment = salt['pillar.get']('environment', None) %}
include:
  - core.nginx.init
  - apps.datal.nginx.admin
  - apps.datal.nginx.api
  - apps.datal.nginx.microsites
  - apps.datal.nginx.workspace

# Delete default host
default_site_removed_webserver:
  file.absent:
    - names: 
        - /etc/nginx/sites-available/default
        - /etc/nginx/sites-enabled/default

restart_nginx:
  service.running:
    - name: nginx
    - require:
      - pkg: nginx
    - watch:
      - file: /etc/nginx/sites-available/admin
      - file: /etc/nginx/sites-available/api
      - file: /etc/nginx/sites-available/microsites
      - file: /etc/nginx/sites-available/workspace
      - file: /etc/nginx/nginx.conf
