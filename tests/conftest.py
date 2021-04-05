from _pytest.fixtures import fixture


@fixture
def emojis():
    return ['1️⃣', '2️⃣', '3️⃣']


@fixture
def word_length():
    return 6
