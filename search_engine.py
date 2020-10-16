import re
from os import getcwd as cwd


def main():
    searcher('chicken')


def searcher(phrase):
    # takes user phrase, removes any tags, digits, and punctuation and splits it into separate words
    terms = re.sub(r'<.*?>|[0-9]|[^\w\s]', '', phrase.replace('+', ' ')).lower().split(' ')
    data = open(cwd() + '/Aux/map.txt').readlines()
    lines = ''
    for term in terms:
        lines += recursive_binary_search(term, data)

    entries = re.sub(r'.*?:: ', '', lines).replace('\n', ', ').split(', ')[:-1]
    dictionary = dict()
    # finds the number of times each phrase of the search appears in the binary search output
    for entry in entries:
        name, number = entry.split(': ')
        if name in dictionary:
            dictionary[name] += (dictionary[name] + int(number))*2
        else:
            dictionary[name] = int(number)

    # sends the built html file back to server
    return build_html(dictionary)


def recursive_binary_search(term, file):
    if len(file) == 1:
        return 'not_found'
    if term == file[int(len(file)/2)].split('::')[0]:
        return file[int(len(file)/2)]
    elif term < file[int(len(file)/2)].split('::')[0]:
        return recursive_binary_search(term, file[0:int(len(file)/2)])
    else:
        return recursive_binary_search(term, file[int(len(file)/2):])


def build_html(dictionary):
    search_page = open(cwd() + '/Aux/starters/search_header.txt').read()
    for entry in sorted(dictionary.items(), key=lambda x: x[1], reverse=True):
        data = open(cwd() + entry[0].replace('..', '')).read()
        # gets information from RML file using regex
        date, blog_name, recipe_title, _ = re.findall("<head>\n(.*?)\n</head>", data, flags=re.DOTALL)[0].split('\n')
        article = re.sub(r'<.*?>|[0-9]|[^\w\s]|\n', '', re.findall("<article>\n(.*?)\n</article>", data, flags=re.DOTALL)[0]).strip().split(' ')
        # adds all need information into html format
        search_page += '        <div class="search_result">\n          <a href="' + entry[0].replace('.rml', '.html') + '">\n'
        if 'null' in recipe_title:
            search_page += '            <h2>' + blog_name.strip() + '</h2>\n          </a>'
        else:
            search_page += '            <h2>' + recipe_title.strip() + '</h2>\n          </a>'
        search_page += '          <h5>' + date.strip() + '</h5>\n          <img src="' + entry[0].rsplit('/', 1)[0].replace('../', '') + '/image1.jpg">\n'
        if len(article) > 100:
            search_page += '          <p>' + ' '.join(article[0:99]) + '...</p>\n        </div>\n'
        else:
            search_page += '          <p>' + ' '.join(article[0:]) + '</p>\n        </div>\n'

    search_page += open(cwd() + '/Aux/enders/search_footer.txt').read()
    return search_page


if __name__ == "__main__":
    main()
