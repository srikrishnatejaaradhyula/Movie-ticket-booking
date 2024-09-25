from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from celery import Celery
import redis
from flask_caching import Cache
from .worker import celery_init_app
# from .celery import celey, ContextTask


app = Flask(__name__, template_folder='template')

app.config['SECRET_KEY'] = 'THIS_IS_A_SECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


config = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "task_api",
    "CACHE_REDIS_URL": "redis://127.0.0.1:6379/0"
}
app.config.from_mapping(config)
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://127.0.0.1:6379/1",
        result_backend="redis://127.0.0.1:6379/2",
        task_ignore_result=True,
    ),
)

cache = Cache(app)
db = SQLAlchemy(app)

celery = celery_init_app(app)

CORS(app)

app.app_context().push()


from app.api import auth,venue,show,booking
# from app.other import pdf
from . import tasks


