import sqlalchemy as sa
from .db import SqlAlchemyBase

class Post(SqlAlchemyBase):
    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
    author = sa.Column(sa.String, nullable=True)
    time = sa.Column(sa.String, nullable=True)
    image = sa.Column(sa.String, nullable=True)
    description = sa.Column(sa.String, nullable=True)
    text = sa.Column(sa.String, nullable=True)