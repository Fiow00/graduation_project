from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import AboutpageView

# Create your tests here.
class AboutpageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("about")
        self.response = self.client.get(url)

    def test_aboutpage_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "about.html")
        self.assertContains(self.response, "About Page")
        self.assertNotContains(self.response, "I should not be here!")

        view = resolve("/about/")
        self.assertEqual(
            view.func.__name__,
            AboutpageView.as_view().__name__
        )
