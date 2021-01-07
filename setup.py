from setuptools import setup

setup(
    name='odas',
    packages=['odas'],
    include_package_data=True,
    install_requires=[
        'flask', 'python-dotenv', 'bcrypt', 'flask_sqlalchemy', 'pymysql', 'sqlalchemy',
        'email-validator', 'behave', 'selenium'
    ],
)
