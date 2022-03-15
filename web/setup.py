from flask import Flask
from flask_graphql import GraphQLView
from flask_graphql_auth import GraphQLAuth
from graphene import Schema

from hidden import JWT_KEY
from web.mutation import Mutation
from web.query import Query

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 10  # 10 minutes
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 30  # 30 days
auth = GraphQLAuth(app)

schema = Schema(query=Query, mutation=Mutation)

app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", graphiql=True, schema=schema))
