import os
from typing import Tuple, List

from db.crud import (
    get_keywords_unprocessed,
    dump_keyword_questions_in_db,
    get_cat_kw_details,
    add_keyword_to_db,
    get_keywords_non_posted,
    update_keyword_status_processed,
    delete_keyword_from_db,
    get_keyword_post_id
)
from gui.helper import (
    _generate_paragraph,
    _generate_table,
    _generate_list,
    _generate_youtube
)
from wp_api.operation import (
    add_keyword_to_wp,
    create_post,
    delete_keyword_from_wp, delete_post_from_wp
)
from paascrape.container import Answer, AnswerType
from paascrape.parsing import get_answers
from wp_api.container import PostData


def get_keywords_from_file(filepath):
    keyword_list = []

    if not os.path.exists(filepath):
        return keyword_list

    with open(filepath, 'r') as f:
        keywords = f.readlines()
        for k in keywords:
            k = k.replace('\n', '')
            if k:
                keyword_list.append(k)

    return keyword_list


def process_keywords():
    """get all non-processed keywords and scrape questions from each keyword then finally dump them in the database"""

    ids = get_keywords_unprocessed()
    print("get_keywords_unprocessed", ids)
    if ids:  # DB ID, KEYWORD
        for db_id, keyword in ids:
            print(keyword)
            answers = get_answers(keyword)
            if answers:
                # Saves the answers as html formatted
                # Opens them with selenium
                # Gets the screenshot binary data and question string
                # Saves them in the database
                dump_keyword_questions_in_db(answers, db_id)


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


def post_keywords_data():
    # get all keywords that has is_processed=True and is_posted=False
    kws = get_keywords_non_posted()
    if kws:
        for kw in kws:
            keyword_name, keyword_id, keyword_questions = kw

            # create a post content from the keywords questions
            post_data = get_post_data(keyword_name, keyword_questions)

            # post the content
            post_id = create_post(keyword_id, post_data)
            if post_id:
                update_keyword_status_processed(keyword_id, post_id)


def delete_keyword(keywords: List[Tuple[int, str]], cat_id: int) -> bool:
    for kw in keywords:
        keyword_id = kw[0]
        post_id = get_keyword_post_id(keyword_id)
        if post_id:
            post_deleted = delete_post_from_wp(post_id)
            if post_deleted:
                kw_deleted = delete_keyword_from_wp(keyword_id)
                if kw_deleted:
                    delete_keyword_from_db(cat_id, keyword_id)
                else:
                    return False
            else:
                return False
        else:
            kw_deleted = delete_keyword_from_wp(keyword_id)
            if kw_deleted:
                delete_keyword_from_db(cat_id, keyword_id)
            else:
                return False

    return True


def get_post_data(keyword_name: str, qnas: list[Answer]) -> PostData:
    p = PostData()
    p.title = keyword_name
    p.slug = keyword_name
    p.content = generate_content(qnas)
    return p


def generate_content(qnas: list[Answer]):
    html = ''
    for qna in qnas:
        if qna.answer_type == AnswerType.Paragraph:
            html += _generate_paragraph(qna)
        elif qna.answer_type == AnswerType.Table:
            html += _generate_table(qna)
        elif qna.answer_type == AnswerType.List:
            html += _generate_list(qna)
        elif qna.answer_type == AnswerType.Youtube:
            html += _generate_youtube(qna)

    return html
