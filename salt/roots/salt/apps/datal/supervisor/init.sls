supervisor_conf:
  file.managed:
    - name: /etc/supervisor/supervisord.conf
    - source: salt://apps/datal/supervisor/supervisord.conf
    - template: jinja

uwsgi_conf:
  file.managed:
    - name: /etc/supervisor/conf.d/uwsgi.conf
    - source: salt://apps/datal/supervisor/uwsgi.conf
    - template: jinja

supervisor:
  pkg:
    - installed
