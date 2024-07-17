from datetime import datetime
from ..extensions import db

class KeywordData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200), nullable=False)
    added = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    json = db.Column(db.JSON, nullable=False)
    filters = db.Column(db.JSON, nullable=True)

class KeywordCluster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship('Profile', backref=db.backref('keyword_clusters', lazy=True))
    keywords = db.relationship('Keyword', secondary='keyword_cluster_keywords', lazy='subquery',
                               backref=db.backref('keyword_clusters', lazy=True))

class Keyword(db.Model):
    name = db.Column(db.String(200), primary_key=True)

class APIUsed(db.Model):
    name = db.Column(db.String(200), primary_key=True)

class APICostRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    api_used_name = db.Column(db.String(200), db.ForeignKey('api_used.name'), nullable=False)
    api_used = db.relationship('APIUsed', backref=db.backref('cost_records', lazy=True))

# Association table for the many-to-many relationship between KeywordCluster and Keyword
keyword_cluster_keywords = db.Table('keyword_cluster_keywords',
    db.Column('keyword_cluster_id', db.Integer, db.ForeignKey('keyword_cluster.id'), primary_key=True),
    db.Column('keyword_name', db.String(200), db.ForeignKey('keyword.name'), primary_key=True)
)