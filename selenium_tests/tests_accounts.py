from django.test import tag, TestCase, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.core.management import call_command
from userena.models import UserenaSignup
from selenium.webdriver.firefox.webdriver import WebDriver

class AccountsSeleniumTests(StaticLiveServerTestCase):
    user1_info = {'username': 'amelia',
                  'password': 'test123',
                  'email': 'amelia@localhost'}
    
    @classmethod
    def setUpClass(cls):
        super(AccountsSeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        # stworzenie uzytkownika i jego aktywacja
        call_command('check_permissions')
        cls.user = UserenaSignup.objects.create_user(**cls.user1_info)
        UserenaSignup.objects.activate_user(cls.user.userena_signup.activation_key)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(AccountsSeleniumTests, cls).tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, reverse('userena_signin')))
        username_input = self.selenium.find_element_by_id("id_identification")
        username_input.send_keys(self.user1_info['username'])
        password_input = self.selenium.find_element_by_id("id_password")
        password_input.send_keys(self.user1_info['password'])

        # klikniecie przycisku "sign in":
        self.selenium.find_element_by_xpath('//*[@id="content-box"]/div/form/input[2]').click()
        self.assertEquals(self.selenium.title, self.user1_info['username']+"'s profile.")
