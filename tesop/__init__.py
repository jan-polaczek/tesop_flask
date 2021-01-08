import os
import click
import json
from flask import Flask, send_from_directory
from tesop.web import web as web
from tesop.models import db

app = Flask(__name__)

app.config.update(
    SECRET_KEY=os.getenv('FLASK_SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.getenv('DB_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(app)
app.register_blueprint(web, url_prefix='/')


@app.cli.command()
def init_db():
    click.echo('Resetting database...')
    reset_db()
    click.echo('Database reset.')


def reset_db(path=None):
    db.drop_all()
    db.create_all()
    if path:
        load_data(path)


def load_data(path):
    with open(path, 'r', encoding='utf-8') as file:
        data_string = file.read()
    data = json.loads(data_string)
    for user in data['users']:
        models.User.register(**user)


if __name__ == '__main__':
    app.run(ssl_context='adhoc')


