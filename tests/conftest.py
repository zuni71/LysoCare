import pytest

from libra.models import Book, Member, Loan, Genre


@pytest.fixture
def books() -> list[Book]:
    a = Book.objects.create(
        title="Annihilation",
        author="Jeff Vandermeer",
        genre="science fiction",
    )
    b = Book.objects.create(
        title="The Tainted Cup",
        author="Robert Jackson Bennett",
        genre="fantasy",
    )
    c = Book.objects.create(
        title="The Achilles Trap",
        author="Steve Coll",
        genre="nonfiction",
    )
    return [a, b, c]


@pytest.fixture
def members() -> list[Member]:
    a = Member.objects.create(
        name="Alan Turing",
        branch="London",
    )
    b = Member.objects.create(
        name="Guido van Rossum",
        branch="Den Haag",
    )
    c = Member.objects.create(
        name="Grace Hopper",
        branch="New York City",
    )
    return [a, b, c]

