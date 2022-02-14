from ariadne import convert_kwargs_to_snake_case

from main import db
from models.postModel import Post


@convert_kwargs_to_snake_case
def resolve_create_post(obj, info, title, body):
    try:
        post = Post(
            title=title, body=body
        )
        db.session.add(post)
        db.session.commit()
        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except ValueError:
        payload = {
            "success": False,
            "errors": ["Erreur !"]
        }

    return payload