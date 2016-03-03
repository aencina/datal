from django.test import SimpleTestCase
from django.test import Client
from django.core.management import call_command

#coverage run --source=microsites manage.py test --settings="microsites.settings"  --nologcapture --where=microsites/
#coverage report --skip-covered -m

class HomeViewTestCase(SimpleTestCase):
    fixtures = ['accountlevel.json', 'account.json']

    def setUp(self):
        call_command('loaddata', '../core/fixtures/accountlevel.json', verbosity=0)
        call_command('loaddata', '../core/fixtures/account.json', verbosity=0)

    def test_ok(self):
        resp = self.client.get('/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)
