from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# nota: esse arquivo serve para reduzir a possibilidade
# de imports circulares