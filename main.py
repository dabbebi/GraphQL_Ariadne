import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database Configs [Check it base on other Database Configuration]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return 'Hello!'

def run():
    from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
    from ariadne.constants import PLAYGROUND_HTML
    from flask import request, jsonify
    from schemas.postQuery import resolve_posts, resolve_post
    from schemas.postMutation import resolve_create_post, resolve_update_post, resolve_delete_post
    # Query
    query = ObjectType("Query")

    query.set_field("posts", resolve_posts)
    query.set_field("post", resolve_post)
    type_defs = load_schema_from_path("schema.graphql")

    #Mutation
    mutation = ObjectType("Mutation")

    mutation.set_field("createPost", resolve_create_post)
    mutation.set_field("updatePost", resolve_update_post)
    mutation.set_field("deletePost", resolve_delete_post)

    schema = make_executable_schema(
        type_defs, query, mutation, snake_case_fallback_resolvers
    )

    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return PLAYGROUND_HTML, 200


    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()

        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )

        status_code = 200 if success else 400
        return jsonify(result), status_code



if __name__ == '__main__':
    run()
    app.run()