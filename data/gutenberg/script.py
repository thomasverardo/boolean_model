def replace_newline_with_space(text):
    paragraphs = text.split('\n\n')  # Split text into paragraphs

    # Replace newline characters with spaces for each paragraph
    replaced_paragraphs = []
    for paragraph in paragraphs:
        replaced_paragraphs.append(paragraph.replace('\n', ' '))

    # Join the paragraphs with double newline characters
    replaced_text = '\n\n'.join(replaced_paragraphs)

    return replaced_text


# Example usage
with open("data/gutenberg/A room with a view", "r") as f:
    file = replace_newline_with_space(f.read())
f.close()

with open("data/gutenberg/a_room_with_a_view_edited", "w") as f:
    f.write(file)
f.close()
