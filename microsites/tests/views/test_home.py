from django.test import SimpleTestCase
from django.test import Client
from django.core.management import call_command
from core import models

#coverage run --source=microsites manage.py test --settings="microsites.settings"  --nologcapture --where=microsites/
#coverage report --skip-covered -m

class HomeViewTestCase(SimpleTestCase):
    fixtures = ['accountlevel.json', 'account.json']

    def setUp(self):
        call_command('loaddata', '../core/fixtures/accountlevel.json', verbosity=0)
        call_command('loaddata', '../core/fixtures/account.json', verbosity=0)
        call_command('loaddata', '../core/fixtures/preference.json', verbosity=0)
        call_command('loaddata', '../core/fixtures/category.json', verbosity=0)
        call_command('loaddata', '../core/fixtures/categoryi18n.json', verbosity=0)

    def test_home_coverage(self):
        # Basic path
        resp = self.client.get('/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # No home, redirect
        cabierta = models.Account.objects.get(id=1)
        home = models.Preference.objects.get(account=cabierta, key='account.home')
        
        home_value = home.value
        home.value = ''
        home.save()
        
        resp = self.client.get('/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.redirect_chain[-1][0], 'http://microsites.dev:8080/search/')
        
        home.value = home_value
        home.save()

    def test_update_list_coverage(self):
        resp = self.client.post('/home/update_list', follow=True, SERVER_NAME="microsites.dev:8080",
            data={ 'order': 0, 'category_filters': '', 'entity_filters': '2', 'type_filters':'vz'} )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/home/update_list', data={ 'order': 1, 'category_filters': 'Finanzas'}, follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # No federated account
        resp = self.client.post('/home/update_list', data={ 'order': 1, 'category_filters': 'Finanzas'}, follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 200)

        # Validation fail
        resp = self.client.post('/home/update_list', data={ 'type': '23$%*43'}, follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 200)


    def test_update_categories_coverage(self):
        resp = self.client.get('/home/update_categories', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/home/update_categories?account_id=2', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        
    def test_sitemap_coverage(self):
        resp = self.client.get('/sitemap', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)