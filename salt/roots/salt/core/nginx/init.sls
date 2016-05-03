install_nginx:
  pkg.installed:
    - names:
      - nginx

nginx_main_conf:
  file.managed:
    - name: /etc/nginx/nginx.conf
    - source: salt://core/nginx/nginx.conf
    - template: jinja

nginx_certs_directory:
  file.directory:
    - name: /etc/nginx/certs
    - makedirs: True
