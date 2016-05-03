include:
  - core.nginx.init

api_site:
  file.managed:
    - name: /etc/nginx/sites-available/api
    - source: salt://apps/datal/nginx/api
    - template: jinja

api_site_enabled:
  file.symlink:
    - target: /etc/nginx/sites-available/api
    - name: /etc/nginx/sites-enabled/api
