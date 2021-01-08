from behave import *

use_step_matcher("re")


@given("The user navigates to the registration page")
def step_impl(context):
    context.browser.get('http://127.0.0.1:5000/sign-up')


@step("The user enters valid username, email and password")
def step_impl(context):
    context.browser.find_element_by_name('username').send_keys('testuser')
    context.browser.find_element_by_name('email').send_keys('test@example.com')
    context.browser.find_element_by_name('password').send_keys('testpassword')


@when("The user presses the submit button")
def step_impl(context):
    context.browser.find_element_by_xpath(f"//input[@type='submit']").click()


@then("The user is successfully registered")
def step_impl(context):
    assert 'http://127.0.0.1:5000/login' in context.browser.current_url
    assert 'Rejestracja udana' in context.browser.page_source


@step("The user enters invalid username, email and/or password")
def step_impl(context):
    context.browser.find_element_by_name('username').send_keys('testuser')
    context.browser.find_element_by_name('email').send_keys('bad_email')
    context.browser.find_element_by_name('password').send_keys('testpassword')


@then("The user is not registered")
def step_impl(context):
    assert context.browser.current_url == 'http://127.0.0.1:5000/register'
    assert 'Nieprawidowy adres e-mail' in context.browser.page_source
