import os
from db.crud import get_cat_kw_details, add_keyword_to_db
from wp_api.operation import add_keyword_to_wp


def get_keywords_from_file(filepath):
    keyword_list = []

    if not os.path.exists(filepath):
        return keyword_list

    with open(filepath, 'r', encoding='utf-8') as f:
        keywords = f.readlines()
        for k in keywords:
            k = k.replace('\n', '')
            if k:
                keyword_list.append(k)

    return keyword_list

def update_keywords_table(window, i_d=None, name=None):
    if i_d:
        updated_tw = get_cat_kw_details(i_d)
        if not updated_tw:
            updated_tw = [['--', '---', '---', '---', '---']]
    else:
        updated_tw = [['--', '---', '---', '---', '---']]
        name = '---'
    window['-KEYWORD_COL_CAT-'].update(name)
    window['-KEYWORDS_TABLE-'].update(updated_tw)


def get_keywords_in_category(category_id):
    return [i[1].lower() for i in get_cat_kw_details(category_id)]


def add_keywords_from_file(kws, c_id):
    current_keywords = get_keywords_in_category(c_id)
    for keyword_name in kws:
        if keyword_name.lower() not in current_keywords:
            keyword_id = add_keyword_to_wp(c_id, keyword_name)
            if not keyword_id:
                print('wordpress error: could not create category!')
                break

            add_keyword_to_db(c_id, keyword_id, keyword_name)


