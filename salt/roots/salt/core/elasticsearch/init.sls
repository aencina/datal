{% set user = pillar['system']['user'] %}
{% set group = pillar['system']['group'] %}

include:
  - core.users
  - core.java
  - core.git

elastic_deps:
  pkg.installed:
    - pkgs:
      - python-git
      - python-dev

elasticsearch-ubuntu:
  pkgrepo.managed:
    - humanname: ElasticSearch PPA
    - name: deb http://packages.elastic.co/elasticsearch/1.6/debian stable main
    - dist: stable
    - file: /etc/apt/sources.list.d/elasticsearch.list
    - key_url: https://packages.elastic.co/GPG-KEY-elasticsearch
    - require_in:
      - pkg: elasticsearch

  pkg.latest:
    - name: elasticsearch
    - refresh: True

#Instala elasticsearch, crea los init.d y lo mete en todos los rc
elasticsearch:
  pkg:
    - installed
  cmd.run:
    - cwd: /
    - name: update-rc.d elasticsearch defaults 95 10 ; update-rc.d elasticsearch enable

# no sé por qué no puede crear este directorio
# aunque... al reiniciar se pierde
/run/elasticsearch/:
  file.directory:
    - user: elasticsearch
    - group: elasticsearch
    - mode: 755
    - makedirs: True

/etc/elasticsearch/elasticsearch.yml:
 file.append:
    - text:
        - "script.inline: on"
        - "script.indexed: on"

elasticsearch-service:
  service.running:
    - name: elasticsearch
    - enable: True
