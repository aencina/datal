from django.test import SimpleTestCase
from django.test import Client
from django.core.management import call_command
from core import models

#coverage run --source=microsites manage.py test --settings="microsites.settings"  --nologcapture --where=microsites/
#coverage report --skip-covered -m

class HomeViewTestCase(SimpleTestCase):

    def setUp(self):
        call_command('loaddata', '../core/fixtures/accountlevel.json', verbosity=0)
        call_command('loaddata', '../core/fixtures/account.json', verbosity=0)
        call_command('loaddata', '../core/fixtures/preference.json', verbosity=0)
        call_command('loaddata', '../core/fixtures/category.json', verbosity=0)
        call_command('loaddata', '../core/fixtures/categoryi18n.json', verbosity=0)

    def test_browse_coverage(self):
        # Basic path
        resp = self.client.get('/datastreams/category/finanzas/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

    def test_search_coverage(self):
        # Basic path
        resp = self.client.get('/search/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # sin dataset       
        resp = self.client.get('/search', follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 200)

        # sin dataset       
        resp = self.client.get('/search/?resource=dt', follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 404)

        # empty result       
        resp = self.client.get('/search/?page=4', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # caracteres raors
        resp = self.client.get('/search/?q=-?', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # invlid form       
        resp = self.client.get('/search/?tag=--', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 404)