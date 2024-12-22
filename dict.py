import re
import inflect
import string

# Script to pre-process the dictionary path
def remove_punctuation(text):
    # Define the punctuation to remove
    punctuation_to_remove = r'[.,:!]'

    # Remove punctuation
    text_without_punctuation = re.sub(punctuation_to_remove, '', text)

    return text_without_punctuation

def split_text_into_words(text):
    # Split the text into words
    words = text.split()

    return words


# This is necessary as it aids in force alignment
def clean_text(text):
    # Use regular expression to keep only letters, numbers, and spaces
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    return cleaned_text

# SECTION 1
# converting the scraped text into individual lettering + split lines
def process_text(input_filename, output_filename):
    try:
        # Read the input text from the file
        with open(input_filename, 'r') as input_file:
            text = input_file.read()

        # Remove punctuation
        text_without_punctuation = remove_punctuation(text)

        # Split the text into words
        words = split_text_into_words(text_without_punctuation)

        # Write each word to the output file
        with open(output_filename, 'w') as output_file:
            for word in words:
                word = clean_text(word)
                output_file.write(word.upper() + '\n')

        print(f"Output written to {output_filename} successfully.")

    except FileNotFoundError:
        print(f"Error: The file {input_filename} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# SECTION 2
# Removes punctuation and ensures that the words are converted into ordinals
def process_text_section2(input_file_path, output_file_path):
    p = inflect.engine()
    
    # Ensure that the encoding here is kept at iso-8859-1 so that it can take in broader range of characters
    with open(input_file_path, 'r', encoding='iso-8859-1') as file:
        text = file.read()

    # Split text into words
    words = text.split()

    def convert_number(word):
        # Store original for returning if not a match
        original_word = word

        # Convert word to lowercase for matching ordinals
        lw = word.lower()

        if lw.isdigit() or re.match(r'^\d+(st|nd|rd|th)$', lw):
            # Convert ordinal numbers (e.g. "7th", "11th")
            return convert_ordinal_to_words(lw)
        return original_word

    def convert_ordinal_to_words(ordinal):
        """Converts an ordinal number (e.g., 7th) to its cardinal form (e.g., 7).

        Args:
            ordinal: The ordinal number as a string.

        Returns:
            The cardinal form of the number as a string.
        """
        try:
            # Remove the ordinal suffix (st, nd, rd, th)
            cardinal = re.sub(r'(st|nd|rd|th)$', '', ordinal.lower())
            word = p.number_to_words(cardinal)
            text = p.ordinal(word).upper()
            text = text.translate(str.maketrans('', '', string.punctuation.replace('-', '')))
            text = text.replace('-', ' ')
            return text
        except ValueError:
            return "Invalid input"

    # Convert numbers and ordinals to words
    words = [convert_number(word) for word in words]

    # Convert to uppercase and split the resulting phrase into sub-words
    processed_words = []
    for word in words:
        for sub_word in word.split():
            processed_words.append(sub_word.upper())


    

    # Let us see if this would actually properly work
    # Write each word on a new space (for the transcription to be done later)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for word in processed_words:
            v = ''
            for letter in word:
                if letter.isnumeric() or letter.isalpha():
                    v += letter
            file.write(v+ ' ')