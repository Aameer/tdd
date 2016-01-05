from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.test import TestCase
from lists.views import home_page

from lists.models import Item,List
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

class NewListViewTest(TestCase):
    def test_can_save_post_request_to_database(self):
        self.client.post('/lists/new/',{'item_text':'A new item'})
        item_from_db = Item.objects.all()[0]
        self.assertEqual(item_from_db.text, 'A new item')
        
    def test_redirects_to_url(self):
        response =self.client.post('/lists/new/',{'item_text':'A new item'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

class ListViewTest(TestCase):
    def test_list_page_shows_items_in_database(self):
        list_ = List.objects.create()
        Item.objects.create(text= 'item 1', list = list_)
        Item.objects.create(text= 'item 2', list = list_)
        
        response =self.client.get('/lists/the-only-list-in-the-world/')

        self.assertIn('item 1',response.content.decode())
        self.assertContains(response, 'item 2')

    def test_uses_lists_template(self):
        response =self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response,'list.html')
        

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items_to_the_database(self):
        first_list = List()
        first_item = Item()
        first_list.save()
        first_item.text= 'Item the first'
        first_item.list = first_list
        first_item.save()

        second_item = Item()
        second_item.text= 'second item'
        second_item.list = first_list
        second_item.save()
      
        first_item_from_db = Item.objects.all()[0]
        self.assertEqual(first_item_from_db.text, 'Item the first')
        self.assertEqual(first_item_from_db.list, first_list)

        second_item_from_db = Item.objects.all()[1]
        self.assertEqual(second_item_from_db.text, 'second item')
        self.assertEqual(second_item_from_db.list, first_list)
