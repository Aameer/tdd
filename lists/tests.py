from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.test import TestCase
from lists.views import home_page

from lists.models import Item
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

    def test_home_page_can_save_post_request_to_database(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text']= 'A new item'

        response = home_page(request)

        item_from_db = Item.objects.all()[0]
        self.assertEqual(item_from_db.text, 'A new item')
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/lists/the-only-list-in-the-world/')

class ListViewTest(TestCase):
    def test_list_page_shows_items_in_database(self):
        Item.objects.create(text= 'item 1')
        Item.objects.create(text= 'item 2')
        
        response =self.client.get('/lists/the-only-list-in-the-world/')

        self.assertIn('item 1',response.content.decode())
        self.assertContains(response, 'item 2')

class ListModelTest(TestCase):
    def test_saving_and_retrieving_items_to_the_database(self):
        first_item = Item()
        first_item.text= 'Item the first'
        first_item.save()

        second_item = Item()
        second_item.text= 'second item'
        second_item.save()
      
        first_item_from_db = Item.objects.all()[0]
        self.assertEqual(first_item_from_db.text, 'Item the first')

        second_item_from_db = Item.objects.all()[1]
        self.assertEqual(second_item_from_db.text, 'second item')
