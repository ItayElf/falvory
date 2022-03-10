from flask import Flask
from flask_graphql import GraphQLView
from graphene import Schema

from web.query import Query

app = Flask(__name__)

schema = Schema(query=Query)

app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", graphiql=True, schema=schema))
