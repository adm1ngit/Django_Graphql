import graphene
from graphene_django.types import DjangoObjectType
from .models import Book

# GraphQL Book turi
class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "published_date")

# Query sinfi
class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.Int())

    def resolve_all_books(root, info):
        return Book.objects.all()

    def resolve_book(root, info, id):
        try:
            return Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return None

# Mutatsiya sinfi
class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        published_date = graphene.Date(required=True)

    book = graphene.Field(BookType)

    def mutate(root, info, title, author, published_date):
        book = Book(title=title, author=author, published_date=published_date)
        book.save()
        return CreateBook(book=book)

class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
