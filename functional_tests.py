import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        #self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Edith has heard about a cool new online to-do app. She goes 
        #to check out its homepage
        self.browser.get('http://localhost:8000/')

        #She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)


        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('To-Do',header.text)

        #she is invited to enter a to-do item straight awy
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')

        #she types "Buy peacock feathers" into text box (Edith's hobby
        #is fly-fishing lures)
        inputbox.send_keys("Buy peacock feathers")
        
        #when she hits enter, the page updates, and now  the page lists
        #"1: Buy peacock feathers" as an item in to-do list
        inputbox.send_keys(Keys.ENTER)

        table=self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
                "1: Buy peacock feathers",
                [row.text for row in rows]
        )

        #There is still  a text box inviting her to add another item. She 
        #enters "Use peacock feathers to make a fly" (Edith  is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)

        table=self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
                "2: Use peacock feathers to make a fly",
                [row.text for row in rows]
        )

        self.assertIn(
                "1: Buy peacock feathers",
                [row.text for row in rows]
        )
        self.fail('Finish the test!')
        #The page Updates again, and now shows both items on her list
        
        #Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        
        # She visits that URL - her to-do list is still there.
        
        # Satisfied, she goes back to sleep

if __name__ == "__main__":
    unittest.main()

