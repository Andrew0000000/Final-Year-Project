def test_tokenize_text():
    # Test case 1: Empty text
    text = ""
    assert dp.tokenize_text(text) == []

    # Test case 2: Text with only punctuation
    text = "!!! ??? ..."
    assert dp.tokenize_text(text) == []

    # Test case 3: Text with numbers
    text = "The price is $10.99."
    assert dp.tokenize_text(text) == [('The', 'DT'), ('price', 'NN'), ('is', 'VBZ'), ('$10.99', 'CD'), ('.', '.')]

    # Test case 4: Text with special characters
    text = "This is @GitHub_Copilot!"
    assert dp.tokenize_text(text) == [('This', 'DT'), ('is', 'VBZ'), ('@GitHub_Copilot', 'NN'), ('!', '.')]

    # Test case 5: Text with multiple sentences
    text = "Hello. How are you? I'm fine, thank you."
    assert dp.tokenize_text(text) == [('Hello', 'NNP'), ('.', '.'), ('How', 'WRB'), ('are', 'VBP'), ('you', 'PRP'),
                                      ('?', '.'), ('I', 'PRP'), ("'m", 'VBP'), ('fine', 'JJ'), (',', ','), ('thank', 'NN'),
                                      ('you', 'PRP'), ('.', '.')]

    # Test case 6: Text with contractions
    text = "I don't like it."
    assert dp.tokenize_text(text) == [('I', 'PRP'), ('do', 'VBP'), ("n't", 'RB'), ('like', 'VB'), ('it', 'PRP'), ('.', '.')]

    # Test case 7: Text with multiple spaces
    text = "   This    is   a   test.   "
    assert dp.tokenize_text(text) == [('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('test', 'NN'), ('.', '.')]

    # Test case 8: Text with different capitalization
    text = "This is a TEST."
    assert dp.tokenize_text(text) == [('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('TEST', 'NN'), ('.', '.')]

    # Test case 9: Text with non-ASCII characters
    text = "Café au lait"
    assert dp.tokenize_text(text) == [('Café', 'NN'), ('au', 'NN'), ('lait', 'NN')]

    # Test case 10: Text with multiple occurrences of the same word
    text = "The cat cat cat sat on the mat."
    assert dp.tokenize_text(text) == [('The', 'DT'), ('cat', 'NN'), ('cat', 'NN'), ('cat', 'NN'), ('sat', 'VBD'),
                                      ('on', 'IN'), ('the', 'DT'), ('mat', 'NN'), ('.', '.')]

    # Test case 11: Text with different types of apostrophes
    text = "It's John's book."
    assert dp.tokenize_text(text) == [('It', 'PRP'), ("'s", 'VBZ'), ('John', 'NNP'), ("'s", 'POS'), ('book', 'NN'), ('.', '.')]

    # Test case 12: Text with hyphenated words
    text = "The long-term goal is to succeed."
    assert dp.tokenize_text(text) == [('The', 'DT'), ('long-term', 'JJ'), ('goal', 'NN'), ('is', 'VBZ'), ('to', 'TO'),
                                      ('succeed', 'VB'), ('.', '.')]

    # Test case 13: Text with multiple types of punctuation
    text = "This is a test! How about that?"
    assert dp.tokenize_text(text) == [('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('test', 'NN'), ('!', '.'), ('How', 'WRB'),
                                      ('about', 'IN'), ('that', 'DT'), ('?', '.')]

    # Test case 14: Text with multiple types of whitespace characters
    text = "This\tis\na\rtest."
    assert dp.tokenize_text(text) == [('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('test', 'NN'), ('.', '.')]

    # Test case 15: Text with leading and trailing whitespace
    text = "   This is a test.   "
    assert dp.tokenize_text(text) == [('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('test', 'NN'), ('.', '.')]

    # Test case 16: Text with mixed case words
    text = "This is a TeSt."
    assert dp.tokenize_text(text) == [('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('TeSt', 'NN'), ('.', '.')]

    # Test case 17: Text with multiple types of quotes
    text = 'He said, "Hello!"'
    assert dp.tokenize_text(text) == [('He', 'PRP'), ('said', 'VBD'), (',', ','), ('"', '``'), ('Hello', 'UH'), ('!', '.'), ('"', "''")]

    # Test case 18: Text with URLs
    text = "Check out this link: https://www.example.com"
    assert dp.tokenize_text(text) == [('Check', 'VB'), ('out', 'RP'), ('this', 'DT'), ('link', 'NN'), (':', ':'),
                                      ('https://www.example.com', 'URL')]

    # Test case 19: Text with email addresses
    text = "Contact me at john@example.com"
    assert dp.tokenize_text(text) == [('Contact', 'NN'), ('me', 'PRP'), ('at', 'IN'), ('john@example.com', 'EMAIL')]

    # Test case 20: Text with emojis
    text = "I love ❤️ GitHub Copilot! 😃"
    assert dp.tokenize_text(text) == [('I', 'PRP'), ('love', 'VBP'), ('❤️', 'EMOJI'), ('GitHub', 'NNP'), ('Copilot', 'NNP'),
                                      ('!', '.'), ('😃', 'EMOJI')]

    print("All test cases passed!")

test_tokenize_text()