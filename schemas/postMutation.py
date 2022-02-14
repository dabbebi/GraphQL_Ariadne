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

@convert_kwargs_to_snake_case
def resolve_update_post(obj, info, post_id, title, body):
    try:
        post = Post.query.get(post_id)
        post.title = title
        post.body = body
        db.session.add(post)
        db.session.commit()
        payload = {
            "success": True,
            "post": post.to_dict()
        }
    except AttributeError:  # post not found
        payload = {
            "success": False,
            "errors":  [f"Post matching id {post_id} was not found"]
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_delete_post(obj, info, post_id):
    try:
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
        payload = {"success": True}

    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Post matching id {post_id} not found"]
        }

    return payload