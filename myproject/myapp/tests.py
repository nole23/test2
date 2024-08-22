# myapp/tests/test_selenium.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from django.test import LiveServerTestCase

class SeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Pokreće Chrome u headless režimu
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.selenium = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_text_presence(self):
        self.selenium.get(f'{self.live_server_url}/')
        body = self.selenium.find_element(By.TAG_NAME, 'body')
        self.assertIn('Hello, world!', body.text)
