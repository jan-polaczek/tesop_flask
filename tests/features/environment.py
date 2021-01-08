from webdriver_manager.chrome import ChromeDriverManager
import threading
import os
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tesop import app, reset_db

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-proxy-server')
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")

CHROME_DRIVER = os.path.join(os.path.join(os.path.dirname(__file__), 'driver'), 'chromedriver.exe')


def before_all(context):
    app.config.update(
        SECRET_KEY='\x1fSU\xe5\xb2.F\x03\xacm\x9fy-\x04\xbb0\xa8\xf0\x96q\x94\xbb\xb0n',
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@127.0.0.1:3306/tesop_test',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    with app.app_context():
        reset_db(os.path.join(os.path.join(os.path.dirname(__file__), 'test_data.json')))
    context.server = simple_server.WSGIServer(("", 5000), WSGIRequestHandler)
    context.server.set_app(app)
    context.pa_app = threading.Thread(target=context.server.serve_forever)
    context.pa_app.start()
    context.browser = webdriver.Chrome(options=chrome_options, executable_path=CHROME_DRIVER)
    context.browser.set_page_load_timeout(time_to_wait=200)


def after_all(context):
    context.browser.quit()
    context.server.shutdown()
    context.pa_app.join()
