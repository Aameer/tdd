from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.test import TestCase
from lists.views import home_page
# Create your tests here.

from lists.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found= resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_content = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_content)

    def test_home_page_can_remember_post_requests(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text']= 'A new item'

        response = home_page(request)

        self.assertIn('A new item',response.content.decode())

        expected_content = render_to_string('home.html',{'new_item_text':'A new item'})
        self.assertEqual(response.content.decode(), expected_content)
