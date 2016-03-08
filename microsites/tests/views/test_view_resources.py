from django.test import SimpleTestCase
from django.test import Client
from django.core.management import call_command
from core import models

#coverage run --source=microsites manage.py test --settings="microsites.settings"  --nologcapture --where=microsites/
#coverage report --skip-covered -m

class HomeViewTestCase(SimpleTestCase):
    fixtures = [
        '../core/fixtures/accountlevel.json',
        '../core/fixtures/account.json',
        '../core/fixtures/preference.json',
        '../core/fixtures/user.json',
        '../core/fixtures/role.json',
        '../core/fixtures/privilege.json',
        '../core/fixtures/grant.json',
        '../core/fixtures/application.json',
        '../core/fixtures/category.json',
        '../core/fixtures/categoryi18n.json',
        '../core/fixtures/dataset.json',
        '../core/fixtures/dataseti18n.json',
        '../core/fixtures/datasetrevision.json',
        '../core/fixtures/datastream.json',
        '../core/fixtures/datastreami18n.json',
        '../core/fixtures/datastreamrevision.json',
        '../core/fixtures/tag.json',
        '../core/fixtures/visualization.json',
        '../core/fixtures/visualizationi18n.json',
        '../core/fixtures/visualizationrevision.json',
    ]

    def setUp(self):
        call_command('loaddata', *self.fixtures)
        
    def test_chart_coverage(self):
        # Basic path
        resp = self.client.get('/visualizations/1736/-', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # not found
        resp = self.client.get('/visualizations/1742/-', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 404)

        # mapchart
        resp = self.client.get('/visualizations/1742/-', follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 200)
    
    def test_embed_coverage(self):
        # Basic path
        resp = self.client.get('/visualizations/embed/NOMIN-DE-INICI-DE-INVER/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # not found 404
        resp = self.client.get('/visualizations/embed/MAP-OF-TRAFF-ACCID/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # mapchart
        #resp = self.client.get('/visualizations/embed/MAP-OF-TRAFF-ACCID/-', follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        #self.assertEqual(resp.status_code, 200) 