include:
  - core.tomcat

download_v8:
  cmd.run:
    - names:
      - wget -c -N https://s3.amazonaws.com/salt.files/Wars/prod/AgileOfficeServer.war
      - wget -c -N https://s3.amazonaws.com/salt.files/Wars/prod/AgileOfficeScraperServices.war
    - cwd: /root
  file.managed:
    - user: tomcat7
    - group: tomcat7
    - names:
      - /root/AgileOfficeServer.war
      - /root/AgileOfficeScraperServices.war
    - recurse:
      - user
      - group

v8_apps_directory:
  file.directory:
    - names:
      - /var/lib/tomcat7/webapps/microsites/AgileOfficeServer/
      - /var/lib/tomcat7/webapps/workspace/AgileOfficeServer/
      - /var/lib/tomcat7/webapps/workspace/AgileOfficeScraperServices/
    - makedirs: True
    - user: tomcat7
    - group: tomcat7

extract_microsites_v8_war:
  cmd.run:
    - cwd: /var/lib/tomcat7/webapps/microsites/AgileOfficeServer/
    - name: unzip -o /root/AgileOfficeServer.war -d /var/lib/tomcat7/webapps/microsites/AgileOfficeServer/

extract_workspace_v8_war:
  cmd.run:
    - cwd: /var/lib/tomcat7/webapps/workspace/AgileOfficeServer/
    - name: unzip -o /root/AgileOfficeServer.war -d /var/lib/tomcat7/webapps/workspace/AgileOfficeServer/

extract_scraper_v8_war:
  cmd.run:
    - cwd: /var/lib/tomcat7/webapps/workspace/AgileOfficeScraperServices/
    - name: unzip -o /root/AgileOfficeScraperServices.war -d /var/lib/tomcat7/webapps/workspace/AgileOfficeScraperServices/

v8_change_ownership:
  file.directory:
    - user: tomcat7
    - group: tomcat7
    - names:
      - /var/lib/tomcat7/webapps/workspace/AgileOfficeScraperServices/
      - /var/lib/tomcat7/webapps/workspace/AgileOfficeServer/
      - /var/lib/tomcat7/webapps/microsites/AgileOfficeServer/
    - recurse:
      - user
      - group
    - watch:
      - cmd: extract_microsites_v8_war
      - cmd: extract_workspace_v8_war
      - cmd: extract_scraper_v8_war

microsites_config:
  file.managed:
    - name: /var/lib/tomcat7/webapps/microsites/AgileOfficeServer/WEB-INF/conf/config.properties
    - source: salt://apps/v8/microsites_config.properties
    - template: jinja

microsites_queries:
  file.managed:
    - name: /var/lib/tomcat7/webapps/microsites/AgileOfficeServer/WEB-INF/conf/queries.properties
    - source: salt://apps/v8/microsites_queries.properties
    - template: jinja

workspace_config:
  file.managed:
    - name: /var/lib/tomcat7/webapps/workspace/AgileOfficeServer/WEB-INF/conf/config.properties
    - source: salt://apps/v8/workspace_config.properties
    - template: jinja

workspace_queries:
  file.managed:
    - name: /var/lib/tomcat7/webapps/workspace/AgileOfficeServer/WEB-INF/conf/queries.properties
    - source: salt://apps/v8/workspace_queries.properties
    - template: jinja

workspace_commons_xml:
  file.managed:
    - name: /var/lib/tomcat7/webapps/workspace/AgileOfficeServer/WEB-INF/conf/commons.xml
    - source: salt://apps/v8/commons.xml
    - template: jinja

microsites_commons_xml:
  file.managed:
    - name: /var/lib/tomcat7/webapps/microsites/AgileOfficeServer/WEB-INF/conf/commons.xml
    - source: salt://apps/v8/commons.xml
    - template: jinja

tomcat_conf:
  file.managed:
    - name: /var/lib/tomcat7/conf/server.xml
    - source: salt://apps/v8/server.xml
    - template: jinja

tomcat_default_conf:
  file.managed:
    - name: /etc/default/tomcat7
    - source: salt://apps/v8/tomcat7.default
    - template: jinja

tomcat-service:
  service.running:
    - name: tomcat7
    - enable: True
    - watch:
      - file: /var/lib/tomcat7/webapps/microsites/AgileOfficeServer/WEB-INF/conf/config.properties
      - file: /var/lib/tomcat7/webapps/microsites/AgileOfficeServer/WEB-INF/conf/queries.properties
      - file: /var/lib/tomcat7/webapps/workspace/AgileOfficeServer/WEB-INF/conf/config.properties
      - file: /var/lib/tomcat7/webapps/workspace/AgileOfficeServer/WEB-INF/conf/queries.properties
      - file: /var/lib/tomcat7/webapps/workspace/AgileOfficeServer/WEB-INF/conf/commons.xml
      - file: /var/lib/tomcat7/webapps/microsites/AgileOfficeServer/WEB-INF/conf/commons.xml
      - file: /var/lib/tomcat7/conf/server.xml
      - file: /usr/share/tomcat7/bin/setenv.sh
