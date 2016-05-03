include:
  - core.nginx.init

admin_site:
  file.managed:
    - name: /etc/nginx/sites-available/admin
    - source: salt://apps/datal/nginx/admin
    - template: jinja

admin_site_enabled:
  file.symlink:
    - target: /etc/nginx/sites-available/admin
    - name: /etc/nginx/sites-enabled/admin
