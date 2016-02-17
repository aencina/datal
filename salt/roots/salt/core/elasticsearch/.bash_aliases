# ejemplo:
#	es_search -d '{"django_id": 66891}'
#
alias es_search="curl -XGET 'localhost:9200/datal/'"
alias es_showall="curl -XGET 'localhost:9200/datal/_search?pretty'"
alias es_show_ds="curl -XGET 'localhost:9200/datal/_search?pretty&q=_type=ds'"
alias es_show_dt="curl -XGET 'localhost:9200/datal/_search?pretty&q=_type=dt'"
alias es_show_vz="curl -XGET 'localhost:9200/datal/_search?pretty&q=_type=vz'"
alias es_mapping="curl -XGET 'localhost:9200/datal/_mapping'"

alias microsites="python manage.py runserver 0.0.0.0:3017 --settings=microsites.settings"
alias microsites-shell="python manage.py shell --settings=microsites.settings"

alias workspace="python manage.py runserver 0.0.0.0:3015 --settings=workspace.settings"
alias workspace-shell="python manage.py shell --settings=workspace.settings"

alias admin="python manage.py runserver 0.0.0.0:3016 --settings=admin.settings"
alias api="python manage.py runserver 0.0.0.0:3018 --settings=api.settings"
alias core-shell="python manage.py shell --settings=core.settings"

alias reindex="python manage.py index --settings=workspace.settings --re-index"

alias compile-msg-core="/home/vagrant/env/bin/python /home/vagrant/app/manage.py compilemessages --settings='core.settings'"
alias compile-msg-workspace="/home/vagrant/env/bin/python /home/vagrant/app/manage.py compilemessages --settings='workspace.settings'"
alias compile-msg-microsites="/home/vagrant/env/bin/python /home/vagrant/app/manage.py compilemessages --settings='microsites.settings'"

alias collectstatic-core="echo yes | /home/vagrant/env/bin/python /home/vagrant/app/manage.py collectstatic --settings=core.settings"
alias collectstatic-workspace="echo yes | /home/vagrant/env/bin/python /home/vagrant/app/manage.py collectstatic --settings=workspace.settings"
alias collectstatic-microsites="echo yes | /home/vagrant/env/bin/python /home/vagrant/app/manage.py collectstatic --settings=microsites.settings"
alias collectstatic-all="echo yes | collectstatic-core -c; echo yes | collectstatic-workspace ; echo yes | collectstatic-microsites "

alias clear_pyco='find ~/app/ -iname "*.py[co]" -exec rm -f {} \;'

