include:
  - core.nginx.init

microsites_site:
  file.managed:
    - name: /etc/nginx/sites-available/microsites
    - source: salt://apps/datal/nginx/microsites
    - template: jinja

microsites_site_enabled:
  file.symlink:
    - target: /etc/nginx/sites-available/microsites
    - name: /etc/nginx/sites-enabled/microsites
