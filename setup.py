from setuptools import setup

setup(
    name='tesop',
    packages=['tesop'],
    include_package_data=True,
    install_requires=[
        'flask', 'python-dotenv', 'click', 'bcrypt', 'flask_sqlalchemy', 'pymysql', 'sqlalchemy',
        'email-validator', 'behave', 'selenium', 'webdriver-manager', 'pyOpenSSL'
    ],
)
