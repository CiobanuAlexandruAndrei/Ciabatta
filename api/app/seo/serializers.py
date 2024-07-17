from flask_marshmallow import Marshmallow
from .models import Keyword, KeywordCluster, APICostRecord

ma = Marshmallow()

class KeywordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Keyword
        load_instance = True
        include_fk = True

class KeywordClusterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = KeywordCluster
        load_instance = True
        include_fk = True

class APICostRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = APICostRecord
        load_instance = True
        include_fk = True
        fields = ['id', 'cost', 'timestamp']