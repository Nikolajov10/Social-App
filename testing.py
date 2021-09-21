import random
import unittest
from selenium import webdriver
import selenium
from selenium.webdriver.common.action_chains import ActionChains
import time
import names

PATH = "C:\chromedriver.exe"
class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Chrome(PATH)
        self.driver.get("http://127.0.0.1:5000/ ")

    def test_sign_up(self):
        for _ in range(50):
            togler = self.driver.find_element_by_class_name("navbar-toggler")
            togler.click()

            self.driver.implicitly_wait(3)
            sign_up = self.driver.find_element_by_id("sign-up")
            sign_up.click()
            self.driver.implicitly_wait(3)

            name = names.get_first_name() + str(random.randint(1,10))
            email = name + names.get_last_name()[:4] + "@gmail.com"
            password = "123123"

            name_input = self.driver.find_element_by_id("username")
            email_input = self.driver.find_element_by_id("email")
            password1_input = self.driver.find_element_by_id("password1")
            password2_input = self.driver.find_element_by_id("password2")
            button = self.driver.find_element_by_class_name("btn-success")

            name_input.send_keys(name)
            email_input.send_keys(email)
            password1_input.send_keys(password)
            password2_input.send_keys(password)
            button.click()

            self.driver.implicitly_wait(5)
            assert self.driver.title =="Feed" or "Username or email already taken" in self.driver.page_source
            if "Username or email already taken" in self.driver.page_source:
                continue
            togler = self.driver.find_element_by_class_name("navbar-toggler")
            togler.click()
            create_post = self.driver.find_element_by_id("create_post")
            create_post.click()

            self.driver.implicitly_wait(2)
            post_input = self.driver.find_element_by_id("post")
            post_input.send_keys(name+"s firts post.")
            post_button = self.driver.find_element_by_class_name("btn-primary")
            post_button.click()

            self.driver.implicitly_wait(2)
            togler = self.driver.find_element_by_class_name("navbar-toggler")
            togler.click()
            logout = self.driver.find_element_by_id("logout")
            logout.click()

    def tearDown(self) -> None:
        
        time.sleep(3)
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()