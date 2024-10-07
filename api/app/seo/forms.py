from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, SubmitField
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

class ContentIdeasForm(FlaskForm):
    topic = StringField('topic', validators=[DataRequired()])
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


class UpdateKeywordClusterNameForm(FlaskForm):
    keyword_cluster_id = IntegerField('keyword_cluster_id', validators=[DataRequired()])
    keyword_cluster_name = StringField('keyword_cluster_name', validators=[DataRequired()])


class ContentIdeaCreationForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    topic_variation = StringField('topic_variation', validators=[DataRequired()])
    topic_category = StringField('topic_category', validators=[DataRequired()])


class ContentIdeaDeletionForm(FlaskForm):
    id = IntegerField('keyword_cluster_id', validators=[DataRequired()])


class GenerateContentOutlineForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    target_audience = StringField('target_audience', validators=[Optional()])
    wrote_as = StringField('wrote_as', validators=[Optional()])
    additional_info = StringField('additional_info', validators=[Optional()])
    content_idea_id = IntegerField('content_idea_id', validators=[DataRequired()])
    delete_content_idea = BooleanField('delete_content_idea', validators=[Optional()])



class EditContentOutlineForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    page_title = StringField('Page Title', validators=[DataRequired()])
    page_description = StringField('Page Description', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])  # Assuming content is a string
    submit = SubmitField('Update Content Outline')