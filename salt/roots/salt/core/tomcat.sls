include:
  - core.java

tomcat7:
  pkg.installed:
    - pkgs:
      - tomcat7
      - tomcat7-admin

tomcat_users:
  file.managed:
    - name: /var/lib/tomcat7/conf/tomcat-users.xml
    - source: salt://core/tomcat-users.xml
    - template: jinja

tomcat_env:
  file.managed:
    - name: /usr/share/tomcat7/bin/setenv.sh
    - source: salt://core/tomcat-env.sh
    - template: jinja
