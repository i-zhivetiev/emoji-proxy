from bs4 import BeautifulSoup
from pytest import fixture

from emoji_proxy.page_content_filter import PageContentFilter


@fixture
def html_template():
    return """\
<!doctype html>
<html lang="ru-RU">
<head>
    <meta charset="utf-8">
    <title>Заголовок страницы</title>
</head>
<body>
<section>
    <main>
        <h1>Заголовок статьи</h1>
        {article}
    </main>
</section>
</body>
</html>
"""


@fixture
def input_article():
    return """\
<article>
    <h2>Подзаголовок</h2>
    <p>Параграф один: 1234 123456 1234 12 123456</p>
    <p>Параграф два: 1 12 1234 123456 1 1234 123456 12</p>
    <p>Параграф с 123456: <a href="http://localhost:9000">123456</a></p>
    <h2>aaaaaa</h2>
</article>
"""


@fixture
def output_article():
    return """\
<article>
    <h2>Подзаголовок</h2>
    <p>Параграф один: 1234 1234561️⃣ 1234 12 1234562️⃣</p>
    <p>Параграф два: 1 12 1234 1234563️⃣ 1 1234 1234561️⃣ 12</p>
    <p>Параграф с 1234562️⃣: <a href="http://localhost:9000">1234563️⃣</a></p>
    <h2>aaaaaa1️⃣</h2>
</article>
"""


@fixture
def input_html(html_template, input_article):
    content = BeautifulSoup(
        html_template.format(article=input_article),
        'html.parser',
    )
    return str(content)


@fixture
def no_article(html_template):
    content = BeautifulSoup(
        html_template.format(article=''),
        'html.parser',
    )
    return str(content)


@fixture
def expected(html_template, output_article):
    content = BeautifulSoup(
        html_template.format(article=output_article),
        'html.parser',
    )
    return str(content)


@fixture
def content_filter(emojis, word_length):
    return PageContentFilter(emojis=emojis, word_length=word_length)


def test_add_emojis_to_article(input_html, expected, content_filter):
    assert content_filter.add_emojis_to_article(input_html) == expected


def test_no_article(no_article, content_filter, html_template):
    expected = BeautifulSoup(html_template.format(article=''), 'html.parser')
    assert content_filter.add_emojis_to_article(no_article) == str(expected)
