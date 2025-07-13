import pytest


def longest_word(sentence):
    if not isinstance(sentence, str):
        raise TypeError("sentence must be str")

    longest: str = ""
    words: list[str] = sentence.split()

    for word in words:
        if len(word) >= len(longest):
            longest = word

    return longest


def test_single_word():
    assert longest_word("hello") == "hello"


def test_ascending_word_length():
    assert longest_word("a ab abc abcd abcde") == "abcde"


def test_tiebreak():
    assert longest_word("hello world") == "world"


def test_descending_word_length():
    assert longest_word("abcde abcd abc ab a") == "abcde"


def test_empty_string():
    assert longest_word("") == ""


def test_type_error():
    with pytest.raises(TypeError):
        longest_word(24)


def test_multiple_ties():
    # Multiple words of same length - should return the last one
    assert longest_word("cat dog bat") == "bat"
    assert longest_word("hi me go it") == "it"


def test_punctuation_handling():
    # Words with punctuation - interviews often test this
    assert longest_word("hello, world!") == "world!"
    assert (
        longest_word("don't can't won't") == "won't"
    )  # or any, they're all same length


def test_whitespace_variations():
    # Multiple spaces, leading/trailing spaces
    assert longest_word("  hello   world  ") == "world"
    assert longest_word("a    b") == "b"


def test_case_sensitivity():
    # Just to verify case doesn't affect length calculation
    assert longest_word("Hello WORLD") == "WORLD"


def test_numbers_and_special_chars():
    # Mixed content
    assert longest_word("abc 123 a1b2c3") == "a1b2c3"
