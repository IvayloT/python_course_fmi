import markdown


def determine_file_type(file):
    readed_file = file.read()
    if file.name.endswith('.md'):
        read_file = decode_text_to_utf8(readed_file)
        # https://python-markdown.github.io/extensions/nl2br/
        return markdown.markdown(read_file, extensions=['nl2br'])
    else:
        return decode_text_to_utf8(readed_file).replace('\n', '')


def decode_text_to_utf8(text):
    return text.decode('UTF-8')
