from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from sni.database import Base

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
cache = Cache()
