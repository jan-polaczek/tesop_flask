from behave import *

use_step_matcher("re")


@given("The user is logged in")
def step_impl(context):
    context.browser.get('http://127.0.0.1:5000/login')
    context.browser.find_element_by_name('email').send_keys('user1@example.com')
    context.browser.find_element_by_name('password').send_keys('password1')
    context.browser.find_element_by_xpath(f"//input[@type='submit']").click()


@step("The user navigates to the new blog post page")
def step_impl(context):
    context.browser.get('http://127.0.0.1:5000/posts/new')


@step("The user enters valid blog post data")
def step_impl(context):
    context.browser.find_element_by_name('title').send_keys('Post testowy')
    context.browser.find_element_by_name('content').send_keys('Treść testowego posta.')


@then("A new blog post is created")
def step_impl(context):
    assert 'http://127.0.0.1:5000/posts/' in context.browser.current_url
    assert 'Post testowy' in context.browser.page_source
