from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func, desc
from sqlalchemy.orm.attributes import set_attribute, flag_modified

db = SQLAlchemy()
