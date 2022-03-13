from flask import Flask
from flask_graphql import GraphQLView
from flask_graphql_auth import GraphQLAuth
from graphene import Schema

from hidden import JWT_KEY
from web.mutation import Mutation
from web.query import Query

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_KEY
auth = GraphQLAuth(app)

schema = Schema(query=Query, mutation=Mutation)

app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", graphiql=True, schema=schema))
