# ********** DataBase module *****************
from mod.db import create_session
from mod.api import Post
# ******** End DataBase module ***************

# ************** Standart module *********************
from datetime import datetime
import random
from mod.utils import email
# ************** Standart module end *****************

# Authorization
class Posts():
    def _create_post(data):
        session = create_session()
        post = Post(
            title=data.title,
            author=data.author,
            time=datetime.now(),
            image=data.image,
            description=data.description,
            text=data.text
        )
        session.add(post)
        session.commit()

    def _get_post(id):
        session = create_session()
        post = session.query(Post).\
    				filter(Post.id == id).\
    				one()

        result = Post(
            id=post.id,
            title=post.title,
            author=post.author,
            time=post.time,
            image=post.image,
            description=post.description,
            text=post.text
        )
        return result

    def _get_last_posts():
        session = create_session()
        posts = session.query(Post).all()

        res = []
        a = 0

        for post in posts:
            if a < 10:
                res.append({
                    "id": post.id,
                    "title": post.title,
                    "author": post.author,
                    "time": post.time,
                    "image": post.image,
                    "description": post.description,
                    "text": post.text
                })
                a += 1
            else:
                break
        return res
