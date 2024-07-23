from flask_marshmallow import Marshmallow
from .models import Keyword, KeywordCluster, APICostRecord, ContentIdea

ma = Marshmallow()

class KeywordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Keyword
        load_instance = True

class KeywordClusterSchema(ma.SQLAlchemyAutoSchema):
    keywords = ma.Nested('KeywordSchema', many=True)

    class Meta:
        model = KeywordCluster
        load_instance = True

class APICostRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = APICostRecord
        load_instance = True
        include_fk = True
        fields = ['id', 'cost', 'timestamp']

class ContentIdeaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ContentIdea
        load_instance = True
