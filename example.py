def map_words_to_title_description(text_list):
    """
    Maps each word in the text (from 'Title:' and 'Description:' lines)
    to the entire corresponding line.

    Args:
        text_list (list): A list of strings, where each string is expected
                           to start with 'Title:' or 'Description:'.

    Returns:
        list: A 2D array (list of lists) where each inner list contains a word
              and its corresponding 'Title:' or 'Description:' line.
    """
    mapping_array = []
    for line in text_list:
        if line.startswith("Title:"):
            title_line = line
            words = title_line[len("Title:"):].strip().split()
            for word in words:
                mapping_array.append([word, title_line])
        elif line.startswith("Description:"):
            description_line = line
            words = description_line[len("Description:"):].strip().split()
            for word in words:
                mapping_array.append([word, description_line])
    return mapping_array

# Your text in the specified format
text_data = [
    "Title: I am exploiting my employer and I have never been happier",
    "Description: [deleted]"
]

# Get the mapping as a 2D array
word_line_mapping = map_words_to_title_description(text_data)
print(word_line_mapping)