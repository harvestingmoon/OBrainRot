def read_txt_to_array(filepath):
    """
    Reads a text file and returns its content as an array (list)
    where each line of the file is an element in the array.

    Args:
        filepath (str): The path to the text file.

    Returns:
        list: A list of strings, where each string is a line from the file.
              Returns an empty list if the file cannot be opened.
    """
    try:
        with open(filepath, 'r') as file:
            lines = [line.strip() for line in file]
        return lines
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
        return []
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

if __name__ == "__main__":
    input_filepath = "../texts/test.txt"  # Replace with the actual path to your .txt file
    data_array = read_txt_to_array(input_filepath)

    if data_array:
        print("Content of the text file as an array:")
        print(data_array)
        # You can now work with the 'data_array' list
        # For example, access the first element:
        # print(f"\nThe first line: '{data_array[0]}'")
    else:
        print("No data was read from the file.")