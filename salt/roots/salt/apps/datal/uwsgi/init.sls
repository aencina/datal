uwsgiinstall:
  pkg:
    - name: uwsgi
    - installed

admin_uwsgi_conf:
  file.managed:
    - name: /etc/uwsgi/admin.ini
    - source: salt://apps/datal/uwsgi/admin.ini
    - template: jinja

api_uwsgi_conf:
  file.managed:
    - name: /etc/uwsgi/api.ini
    - source: salt://apps/datal/uwsgi/api.ini
    - template: jinja

microsite_uwsgi_conf:
  file.managed:
    - name: /etc/uwsgi/microsite.ini
    - source: salt://apps/datal/uwsgi/microsite.ini
    - template: jinja

workspace_uwsgi_conf:
  file.managed:
    - name: /etc/uwsgi/workspace.ini
    - source: salt://apps/datal/uwsgi/workspace.ini
    - template: jinja

# Set directory owner
uwsgi_log_dir_structure:
  file.directory:
    - name: /var/log/uwsgi
    - mode: 777
