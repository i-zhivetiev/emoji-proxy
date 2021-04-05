from _pytest.fixtures import fixture
from pytest import mark

from emoji_proxy.page_content_filter import EmojiAdder


def test_init(emoji_adder, word_length):
    assert emoji_adder._word_length == word_length


def test_get_default_emojis(emoji_adder):
    assert emoji_adder._emoji == '1️⃣'
    assert emoji_adder._emoji == '2️⃣'
    assert emoji_adder._emoji == '3️⃣'
    assert emoji_adder._emoji == '1️⃣'


@mark.parametrize('text,expected', [
    ('123456', '1234561️⃣'),
    ('123456 ', '1234561️⃣ '),
    (' 123456', ' 1234561️⃣'),
    (' 123456 ', ' 1234561️⃣ '),
    ('aa 123456 bb', 'aa 1234561️⃣ bb'),
    ('aa 123456, bb', 'aa 1234561️⃣, bb'),
    ('aa 123456. bb', 'aa 1234561️⃣. bb'),
    ('aa 123456.bb', 'aa 1234561️⃣.bb'),
    ('aa 123456 bb 1234567', 'aa 1234561️⃣ bb 1234567'),
    ('1234 123456 1234567', '1234 1234561️⃣ 1234567'),
    ('1234 123456 1234 123456', '1234 1234561️⃣ 1234 1234562️⃣'),
    ('12 123456 12 123456 123456 12 123456',
     '12 1234561️⃣ 12 1234562️⃣ 1234563️⃣ 12 1234561️⃣'),
])
def test_replacer(text, expected, emoji_adder):
    assert emoji_adder.add_emoji(text) == expected


@fixture
def emoji_adder(emojis, word_length):
    return EmojiAdder(emojis=emojis, word_length=word_length)
