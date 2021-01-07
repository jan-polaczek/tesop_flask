from behave import *

use_step_matcher("re")


@given("The user navigates to the login page")
def step_impl(context):
    context.browser.get('http://127.0.0.1:5000/login')


@step("The user enters valid username and password")
def step_impl(context):
    context.browser.find_element_by_name('username').send_keys('user1')
    context.browser.find_element_by_name('password').send_keys('password1')


@then("The user is logged in successfully")
def step_impl(context):
    assert context.browser.current_url == 'http://127.0.0.1:5000/'
    assert 'Witaj, ' in context.browser.page_source


@step("The user enters invalid username and password")
def step_impl(context):
    context.browser.find_element_by_name('username').send_keys('baduser')
    context.browser.find_element_by_name('password').send_keys('badpassword')


@then("The user is not logged in")
def step_impl(context):
    assert context.browser.current_url == 'http://127.0.0.1:5000/login'
    assert 'Niewłaściwa nazwa użytkownika i/lub hasło' in context.browser.page_source
