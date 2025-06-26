import re

def truncate_text_by_words(text, word_limit):
    words = text.split()
    print(len(words))
    word_limit-=1
    if len(words) <= word_limit:
        return text #if text is alreay in light than return it

    truncated_words = words[:word_limit]

    #serach for the next sentese
    remaining_text = " ".join(words[word_limit:])
    sentence_end = re.search(r"[.!?]", remaining_text)

    if sentence_end:
        end_index = sentence_end.end()  #include the full sentense 
        truncated_text = " ".join(truncated_words) + " " + remaining_text[:end_index]
    else:
        truncated_text = " ".join(truncated_words)  #if no sentese end.

    return truncated_text.strip()
