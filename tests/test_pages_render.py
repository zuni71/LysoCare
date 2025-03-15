import random

import pytest
from django.test import Client
from django.urls import reverse

from libra.models import Book, Member


@pytest.mark.django_db
def test_homepage_renders(
    client: Client, books: list[Book], members: list[Member]
) -> None:
    # Make sure the page loads
    url = reverse("homepage")
    response = client.get(url)
    assert response.status_code == 200
    content = str(response.content)

    # Check against the page contents
    for book in books:
        assert book.title in content

    for member in members:
        assert member.name in content


@pytest.mark.django_db
def test_books_index_renders(client: Client, books: list[Book]) -> None:
    # Make sure the page loads
    url = reverse("books_index")
    response = client.get(url)
    assert response.status_code == 200
    content = str(response.content)

    # Check against the page contents
    for book in books:
        assert book.title in content


@pytest.mark.django_db
def test_books_detail_renders(client: Client, books: list[Book]) -> None:
    # Make sure the page loads
    book = random.choice(books)
    url = reverse("books_detail", kwargs={"book_id": book.id})
    response = client.get(url)
    assert response.status_code == 200
    content = str(response.content)

    # Check against the page content
    assert book.title in content
    assert book.author in content
    assert book.genre in content


@pytest.mark.django_db
def test_genre_renders(client: Client, books: list[Book]) -> None:
    # Make sure the page loads
    book = random.choice(books)
    url = reverse("genre", kwargs={"genre_name": book.genre})
    response = client.get(url)
    assert response.status_code == 200
    content = str(response.content)

    # Check against the page content
    assert book.genre in content
    assert book.title in content


@pytest.mark.django_db
def test_members_index_renders(client: Client, members: list[Member]) -> None:
    # Make sure the page loads
    url = reverse("members_index")
    response = client.get(url)
    assert response.status_code == 200
    content = str(response.content)

    # Check against the page content
    for member in members:
        assert member.name in content


@pytest.mark.django_db
def test_members_detail_renders(client: Client, members: list[Member]) -> None:
    # Make sure the page loads
    member = random.choice(members)
    url = reverse("members_detail", kwargs={"member_id": member.id})
    response = client.get(url)
    assert response.status_code == 200
    content = str(response.content)

    # Check against the page content
    assert member.name in content
    assert member.branch in content
