# import os
# import shutil
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from django.test import LiveServerTestCase
# import time
# import subprocess
# import signal
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# class UserTests(LiveServerTestCase):

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()  # Osiguraj da se osnovne postavke izvrše

#         chrome_options = Options()
#         chrome_options.add_argument("--headless")  # Pokreće Chrome u headless režimu
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

#         cls.driver.implicitly_wait(10)  # Sačekaj 10 sekundi za elemente

#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
#         super().tearDownClass()

#     def test_1_setuser(self):
#         print("Start 1. test...")
#         self.driver.get(f'{self.live_server_url}/index')

#         print("End 1. test...")

#     def test_2_login(self):
#         print("Start 2. test...")
#         # Pokreni test za logovanje
#         self.driver.get(f'{self.live_server_url}/')
#         print("Start 2. 1")

#         username = self.driver.find_element(By.ID, 'username')
#         print("Start 2. 2")

#         password = self.driver.find_element(By.ID, 'password')
#         print("Start 2. 3")

#         username.send_keys('test')
#         print("Start 2. 4")
#         password.send_keys('test')
#         print("Start 2. 5")

#         # Nađite elemente (npr. dugme)
#         button = self.driver.find_element(By.CLASS_NAME, 'btn-primary')
#         print("Start 2. 6")
#         button.click()
#         print("Start 2. 7")

#         WebDriverWait(self.driver, 1).until(
#             EC.presence_of_element_located((By.ID, 'profile-img-user'))  # Zamijenite s ID-om elementa na početnoj stranici
#         )

#         print("End 2. test...")

#     # def test_3_add_new_repository(self):
#     #     print("Start 3. test...")
#     #     self.driver.get(f'{self.live_server_url}/')

#     #     button = self.driver.find_element(By.ID, 'user-all-repo')
#     #     button.click()

#     #     WebDriverWait(self.driver, 1).until(
#     #         EC.presence_of_element_located((By.ID, 'repository-new-repository'))
#     #     )

#     #     button1 = self.driver.find_element(By.ID, 'repository-new-repository')
#     #     button1.click()

#     #     newRepository = self.driver.find_element(By.ID, 'nameRepository')
#     #     description = self.driver.find_element(By.ID, 'descriptionRepository')

#     #     newRepository.send_keys('TestSelenium')
#     #     description.send_keys('TestSelenium description')

#     #     selectLanguage = self.driver.find_element(By.ID, 'new-repository-select-language')
#     #     selectLanguage.click()

#     #     selectPythonLangage = self.driver.find_element(By.ID, 'new-repository-language-Python')
#     #     selectPythonLangage.click()

#     #     selectLicene = self.driver.find_element(By.ID, 'new-repository-select-license')
#     #     selectLicene.click()

#     #     selectIMTLicence = self.driver.find_element(By.ID, 'new-repository-license-MIT')
#     #     selectIMTLicence.click()

#     #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     #     createRepositpry = self.driver.find_element(By.ID, 'new-repository-create-btn')
#     #     createRepositpry.click()

#     #     print("End 3. test...")

#     # def test_4_check_exist_new_repositor(self):
#     #     print("Start 4. test...")
#     #     element = self.driver.find_element(By.ID, 'repository-open-TestSelenium')
#     #     self.assertIsNotNone(element, "Element not found")

#     #     button = self.driver.find_element(By.ID, 'user-all-repo')
#     #     button.click()

#     #     element = self.driver.find_element(By.ID, 'one-repository-TestSelenium')
#     #     self.assertIsNotNone(element, "Element not found")

#     #     print("End 4. test...")

#     # def test_5_open_repository(self):
#     #     print("Start 5. test...")
#     #     button = self.driver.find_element(By.ID, 'user-overview')
#     #     button.click()

#     #     button = self.driver.find_element(By.ID, 'repository-open-TestSelenium')
#     #     button.click()

#     #     element = self.driver.find_element(By.ID, 'repository-tree')
#     #     self.assertEqual(element.text, "Code", f"Expected text 'Code', but got '{element.text}'")

#     #     print("End 5. test...")

#     # def test_6_open_all_tab(self):
#     #     print("Start 6. test...")
#     #     button = self.driver.find_element(By.ID, 'repository-issues')
#     #     button.click()

#     #     element = self.driver.find_element(By.ID, 'issues-add-new-issue')
#     #     self.assertEqual(element.text, "New issue", f"Expected text 'Code', but got '{element.text}'")

#     #     button = self.driver.find_element(By.ID, 'repository-pull')
#     #     button.click()

#     #     button = self.driver.find_element(By.ID, 'repository-statistic')
#     #     button.click()

#     #     button = self.driver.find_element(By.ID, 'repository-settings')
#     #     button.click()

#     #     element = self.driver.find_element(By.ID, 'nameRepository')

#     #     button = self.driver.find_element(By.ID, 'repository-tree')
#     #     button.click()

#     #     print("End 6. test...")

#     # # def test_7_add_new_file(self):
#     # #     print("Start 7. test...")
#     # #     button = self.driver.find_element(By.ID, 'typeRepository')
#     # #     button.click()

#     # #     button = self.driver.find_element(By.ID, 'code-add-new-file')
#     # #     button.click()

#     # #     fileName = self.driver.find_element(By.ID, 'add-files-add-name-file')
#     # #     descriptionFile = self.driver.find_element(By.ID, 'add-files-insert-text')

#     # #     fileName.send_keys('test_file.txt')
#     # #     descriptionFile.send_keys('Neki tekst da unese ')

#     # #     # Skrolujte u manjim delovima dok ne dostignete element
#     # #     scroll_pause_time = 2  # Pauza između skrolovanja
#     # #     last_height = self.driver.execute_script("return document.body.scrollHeight")

#     # #     while True:
#     # #         # Skrolujte prema dolje
#     # #         self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
#     # #         # Sačekajte da se stranica učita
#     # #         time.sleep(scroll_pause_time)
            
#     # #         # Izmerite novu visinu stranice
#     # #         new_height = self.driver.execute_script("return document.body.scrollHeight")
            
#     # #         # Proverite da li se visina promenila
#     # #         if new_height == last_height:
#     # #             break
            
#     # #         last_height = new_height


#     # #     button1 = self.driver.find_element(By.ID, 'add-files-commit-new-file')
#     # #     button1.click()

#     # #     time.sleep(10)

#     # #     if self.driver.find_elements(By.ID, 'code-open-file-test_file.txt'):
#     # #         print("Element sa ID-jem 'code-open-file-test_file.txt' postoji. Test se nastavlja.")
#     # #     # Nastavite sa daljim testiranjem
#     # #     else:
#     # #         raise Exception("Element sa ID-jem 'code-open-file-test_file.txt' ne postoji. Test nije uspeo.")
        
#     # #     print("End 7. test...")

#     # # def test_8_open_new_file(self):
#     # #     print("Start 8. test...")
#     # #     button = self.driver.find_element(By.ID, 'code-open-file-test_file.txt')
#     # #     button.click()

#     # #     editFile = self.driver.find_element(By.ID, 'code-edit-file-test_file.txt')
#     # #     editFile.send_keys('promjeniti tekst kako treba da radi')

#     # #     button = self.driver.find_element(By.ID, 'code-edit-open-file')
#     # #     button.click()

#     # #     element = self.driver.find_element(By.ID, 'code-edit-file-test_file.txt')
#     # #     self.assertEqual(element.text, "Neki tekst da unese promjeniti tekst kako treba da radi", f"Expected text 'Code', but got '{element.text}'")

#     # #     button = self.driver.find_element(By.ID, 'code-remove-open-file')
#     # #     button.click()

#     # #     print("End 8. test...")

#     # # def test_9_open_issues(self):
#     # #     print("Start 9. test...")
#     # #     button = self.driver.find_element(By.ID, 'repository-issues')
#     # #     button.click()

#     # #     button = self.driver.find_element(By.ID, 'issues-add-new-issue')
#     # #     button.click()

#     # #     titleIssues = self.driver.find_element(By.ID, 'name-issues')
#     # #     descriptionIssues = self.driver.find_element(By.ID, 'description-issues')

#     # #     titleIssues.send_keys('Issues 1')
#     # #     descriptionIssues.send_keys('Issue tekst')

#     # #     button = self.driver.find_element(By.ID, 'add-new-issue')
#     # #     button.click()

#     # #     print("End 9. test...")