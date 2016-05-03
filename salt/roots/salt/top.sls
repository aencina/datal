base:
  '*':
    - core.system
    - core.users
    - core.redis
    - core.memcached
    - core.mysql
    - apps.v8.init
    - core.elasticsearch.init
    - apps.datastore.core
    - apps.datal.init
