from flask import Blueprint

security = Blueprint('security', __name__)

# Import routes at the end to avoid circular import
from . import routes, models, forms, serializers