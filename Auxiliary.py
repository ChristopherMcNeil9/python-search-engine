import os
import re
import string


def main():
    paths = create_rml_list()
    mapper(paths)


# creates a file that contains a path to every RML file within the site from the source of python file
def create_rml_list():
    path = '../blogs_source'
    directories = os.listdir(path)

    content = ''

    for directory in directories:
        path = '../blogs_source/' + directory
        files = os.listdir(path)
        # goes through every subdirectory finding all RML files
        for file in files:
            if file.endswith('.rml'):
                content += path + '/' + file + '\n'
    content = content.rstrip()

    path = '../Aux/rml_paths.txt'
    file_out = open(path, 'w+')
    file_out.write(content)
    file_out.close()

    return content


def mapper(paths):
    paths = paths.split('\n')
    global_dict = dict()
    dictionaries = []
    # gets the number of occurrences of each word within each blog
    for path in paths:
        data = open(path).read()
        local_dict = dict()
        _, title, recipe_title, _ = re.findall("<head>\n(.*?)\n</head>", data, flags=re.DOTALL)[0].split('\n')
        # strips all html tags, newlines, digits, and punctuation while making everything lower case and splitting into a list
        data = re.sub(r'<.*?>|[0-9]|[^\w\s]', '', data).replace('\n', ' ').lower()
        # removes all empty entries from the list
        data = list(filter(None, data.split(' ')))

        for word in data:
            if len(word) > 2 and 'null' != word:
                if word in local_dict:
                    local_dict[word] += 1
                    global_dict[word] += 1
                else:
                    local_dict[word] = 1
                # separate instantiation for global, if its in local its in global, but not vice versa
                if word not in global_dict:
                    global_dict[word] = 1
        dictionaries.append(local_dict)

    content = ''
    for word in sorted(global_dict):
        content += word + ':: '
        weights = [0] * len(dictionaries)
        counter = 0
        for dictionary in dictionaries:
            if word in dictionary:
                weights[counter] = dictionary[word]
            counter += 1

        while weights.index((max(weights))) > 0:
            index = weights.index(max(weights))
            content += paths[index] + ': ' + str(weights[index]) + ', '
            weights[index] = 0
        content = content.rsplit(',', 1)[0] + '\n'
    path = '../Aux/map.txt'
    file_out = open(path, 'w+')
    file_out.write(content)
    file_out.close()


if __name__ == "__main__":
    main()
