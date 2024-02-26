import json

# The original dictionary is downloaded from https://kaikki.org/dictionary/German/index.html
# This file has a size of 800MB. This file creates a smaller version (44MB) of the dictionary
# by removing complex fields.

my_german_dict = {}


def combine_lists(list_of_lists):
    combined_list = []
    for sublist in list_of_lists:
        combined_list.extend(sublist)
    return combined_list


def clean_strings(txt):
    txt = txt.replace('#German', '')
    txt = txt.replace('#English', '')
    txt = txt.replace('##', '')
    return txt


with open("dictionary/kaikki.org-dictionary-German.json", 'r', encoding="utf-8") as filename:
    for i, line in enumerate(filename):
        # if i >= 10:
        #     break  # Stop after 10 lines
        data = json.loads(line)
        list_of_meanings = []
        if 'links' in data['senses'][0].keys():
            # data['senses'][0]['links'] is a list of lists. So combine the lists
            new_list = combine_lists(data['senses'][0]['links'])
            for i, word in enumerate(new_list):
                new_list[i] = clean_strings(word)
            if '' in new_list:
                new_list.remove('')
            list_of_meanings += new_list

        if 'glosses' in data['senses'][0].keys():
            # extend the meaning list with those from 'glosses'
            new_list = data['senses'][0]['glosses']
            for i, word in enumerate(new_list):
                new_list[i] = clean_strings(word)
            if '' in new_list:
                new_list.remove('')
            list_of_meanings += new_list

        # create a dictionary of part of speach (pos) and a list meanings.
        # The list of meanings have repetition. Use set() to find the unique values.
        meaning = [data['pos']+'| '] + list(set(list_of_meanings))
        my_german_dict[data['word']] = meaning





# Serializing json
data = json.dumps(my_german_dict, ensure_ascii=False)

with open("dictionary/kaikki_formatted.json", 'w', encoding='utf8') as outfile:
    outfile.write(data)

print('Done!! The dictionary has %d unique words' % len(my_german_dict.keys()))

# # load and test the formatted dictionary
# import json
# with open("kaikki_formatted.json", 'r', encoding='utf8') as file:
#     my_dict = json.load(file)

