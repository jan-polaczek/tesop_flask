import os
import click
from flask import Flask, send_from_directory
from tesop.web import web as web
from tesop import models

app = Flask(__name__)

app.config.update(
    SECRET_KEY=os.environ.get('FLASK_SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DB_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

models.db.init_app(app)
app.register_blueprint(web, url_prefix='/')


@app.cli.command()
def reset_db():
    click.echo('Resetting database...')
    models.db.drop_all()
    models.db.create_all()
    load_data('data.json')
    click.echo('Database reset.')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def load_data(path):
    pass


if __name__ == '__main__':
    app.run()


