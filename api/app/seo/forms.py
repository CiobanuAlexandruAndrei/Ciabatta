from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Optional


class KeywordForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

class KeywordSearchForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])
    limit = IntegerField('limit', validators=[Optional()])

class KeywordGenerationForm(FlaskForm):
    topic = StringField('topic', validators=[DataRequired()])
    intent = StringField('intent', validators=[DataRequired()])
    additional_instructions = StringField('additional_instructions', validators=[Optional()])

class AddKeywordToClusterForm(FlaskForm):
    keyword_name = StringField('keyword_name', validators=[DataRequired()])
    cluster_id = IntegerField('cluster_id', validators=[DataRequired()])

class KeywordClusterForm(FlaskForm):
    keyword_cluster_name = StringField('keyword_cluster_name', validators=[DataRequired()])

class KeywordClusterDeleteForm(FlaskForm):
    cluster_id = IntegerField('cluster_id', validators=[DataRequired()])

class PeriodForm(FlaskForm):
    period = StringField('period', validators=[DataRequired()])