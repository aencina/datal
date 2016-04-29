include:
  - core.nginx.init

workspace_site:
  file.managed:
    - name: /etc/nginx/sites-available/workspace
    - source: salt://apps/datal/nginx/workspace
    - template: jinja

workspace_site_enabled:
  file.symlink:
    - target: /etc/nginx/sites-available/workspace
    - name: /etc/nginx/sites-enabled/workspace


workspace_pass:
  file.managed:
    - name: /etc/nginx/workspace.pass
    - source: salt://apps/datal/nginx/workspace.pass

