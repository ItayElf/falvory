import io

from flask import Flask, send_file
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_graphql_auth import GraphQLAuth
from graphene import Schema

from hidden import JWT_KEY
from pyvory.orm.recipes import get_recipe_picture
from pyvory.orm.users import get_profile_pic, get_profile_pic_by_name
from web.mutation import Mutation
from web.query import Query

app = Flask("flavory")
app.config["JWT_SECRET_KEY"] = JWT_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 10  # 10 minutes
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 30  # 30 days
CORS(app)
auth = GraphQLAuth(app)

schema = Schema(query=Query, mutation=Mutation)

app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", graphiql=True, schema=schema))


@app.route("/images/users/<int:idx>")
def images_user_profile(idx):
    try:
        image = get_profile_pic(idx)
        return send_file(io.BytesIO(image), mimetype="image/webp")
    except FileNotFoundError as e:
        return str(e), 404


@app.route("/images/users/<name>")
def images_user_profile_name(name):
    try:
        image = get_profile_pic_by_name(name)
        return send_file(io.BytesIO(image), mimetype="image/webp")
    except FileNotFoundError as e:
        return str(e), 404


@app.route("/images/recipes/<int:idx>")
def images_recipe_image(idx):
    try:
        image = get_recipe_picture(idx)
        return send_file(io.BytesIO(image), mimetype="image/webp")
    except FileNotFoundError:
        # return f"No image for recipe with id {idx}", 404
        return send_file(io.BytesIO(b""), mimetype="image/webp")
