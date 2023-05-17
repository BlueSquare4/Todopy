from flask_sqlalchemy import SQLAlchemy
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from datetime import datetime


db = SQLAlchemy(db)


class TodoModel(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    done = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"<Todo {self.id}>"

    
class TodoObject(SQLAlchemyObjectType):
    class Meta:
        model = TodoModel
        interfaces = (graphene.relay.Node, )

    def fetch_todos_from_database():
      todos = TodoModel.query.all()
           return [Todo(
                id=todo.id,
                title=todo.title,
                completed=todo.completed
               ) for todo in todos]
  

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_todos = SQLAlchemyConnectionField(TodoObject.connection)


class CreateTodoMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        done = graphene.Boolean(required=True)

    todo = graphene.Field(lambda: TodoObject)

    def mutate(self, info, title, description, done):
        todo = TodoModel(title=title, description=description, done=done)
        db.session.add(todo)
        db.session.commit()
        return CreateTodoMutation(todo=todo)
      

class Mutation(graphene.ObjectType):
    create_todo = CreateTodoMutation.Field()

def get_todos():
    todos = TodoModel.query.all()
    return todos



