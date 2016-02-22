# Para zafar por un problema particular con ChileCompra
import json
account = 5476
guids = []

f = open('/tmp/{}/dataset.json'.format(account), 'r')
fixtures = json.load(f)
f.close()
new_fixtures = []
for fixture in fixtures:
    if fixture['fields']['guid'] not in guids:
        guids.append(fixture['fields']['guid'])
    else:
        print "VIEJO GUID: {}".format(fixture['fields']['guid'])
        partes = fixture['fields']['guid'].split('-')
        partes[4] = str(int(partes[4]) + 1)
        new_guid = '-'.join(partes)
        print "NUEVO GUID: {}".format(new_guid)
        guids.append(new_guid)
        fixture['fields']['guid'] = new_guid
    new_fixtures.append(fixture)
f = open('/tmp/{}/dataset.json'.format(account), 'w')
json.dump(new_fixtures, f)
f.close()
