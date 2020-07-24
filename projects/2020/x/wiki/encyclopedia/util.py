import re
import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def random_entry():
    list = list_entries()
    return list[random.randrange(len(list))]

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

# Delete entry created to remove if renamed
def delete_entry(title):
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def markdownToHTML(input):
    output = input

    # Boldface
    output = re.sub('\*\*(.+?)\*\*', r'<strong>\1</strong>', output, flags=re.MULTILINE)
    output = re.sub('\_\_(.+?)\_\_', r'<strong>\1</strong>', output, flags=re.MULTILINE)

    # Windows new line conversion
    output = re.sub(r'\r\n', r'\n', output)

    # h6 to h1
    output = re.sub(r'\#\#\#\#\#\#\s(.+)', r'<h6>\1</h6>', output, flags=re.MULTILINE)
    output = re.sub(r'\#\#\#\#\#\s(.+)', r'<h5>\1</h5>', output, flags=re.MULTILINE)
    output = re.sub(r'\#\#\#\#\s(.+)', r'<h4>\1</h4>', output, flags=re.MULTILINE)
    output = re.sub(r'\#\#\#\s(.+)', r'<h3>\1</h3>', output, flags=re.MULTILINE)
    output = re.sub(r'\#\#\s(.+)', r'<h2>\1</h2>', output, flags=re.MULTILINE)
    output = re.sub(r'\#\s(.+)', r'<h1>\1</h1>', output, flags=re.MULTILINE)
    
    # Unordered List
    output = re.sub(r'[\*\-]\s(.+)', r'<li>\1</li>', output, flags=re.MULTILINE)
    output = re.sub(r'((?:\<li\>)[\s\S]+(?:\<\/li\>))', r'<ul>\1</ul>', output, flags=re.MULTILINE)

    output = re.sub(r'^([^<].+[^>])$', r'<p>\1</p>', output, flags=re.MULTILINE)
    
    # Links
    output = re.sub('\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', output, flags=re.MULTILINE)
    
    return output