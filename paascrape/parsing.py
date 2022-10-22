import re
import traceback
from typing import Optional, Tuple, List, Any
from urllib.parse import quote

from bs4 import Tag, BeautifulSoup


def _tag_len_2(answer_content):
    publication_date = None

    # getting source url
    source_url = answer_content[-1].find('div', class_="g").find('a')
    url = source_url.attrs['href'] if source_url else None

    # getting answer description
    desc_type_answer = answer_content[0]
    answer = (desc_type_answer.get_text()).replace(
        "\n", "") if desc_type_answer else 'Answer Not Found!'
    ans = re.sub(r'\s+', ' ', answer)
    ans = re.sub(r'More items\.\.\.', '', ans)

    date = re.findall(
        r"([0-9]{2}-(Jun|Feb|Jan|Mar|Apr|May|Jul|Aug|Sept|Oct|Nov|Dec)-[0-9]{4})",
        ans)

    if date:
        ans = ans.removesuffix(date[0][0])
        publication_date = date[0][0]

    return ans, url, publication_date


def _tag_len_3(answer_content):
    publication_date = None

    # getting source url
    source_url = answer_content[-1].find('div', class_="g").find('a')
    url = source_url.attrs['href'] if source_url else None

    # getting answer heading
    answer_heading_tag = answer_content[0].find('div', {"role": "heading"})
    answer_heading = answer_heading_tag.get_text() if answer_heading_tag else ''

    # getting answer body
    answer_body = answer_content[1].get_text()
    answer = answer_heading.replace(
        "\n", "") + '\n' + answer_body.replace("\n", "")
    ans = re.sub(r'\s+', ' ', answer)
    ans = re.sub(r'More items\.\.\.', '', ans)

    date = re.findall(
        r"([0-9]{2}-(Jun|Feb|Jan|Mar|Apr|May|Jul|Aug|Sept|Oct|Nov|Dec)-[0-9]{4})",
        ans)
    if date:
        ans = ans.removesuffix(date[0][0])
        publication_date = date[0][0]

    return ans, url, publication_date


def extract_answer(answer_block: Tag):
    """
    Takes a html blob of single question and returns its relevant answer.

    :rtype: Questions
    :param answer_block: Bs4 Tag element containing the relevant data
    :return: NamedTuple containing the questions or None
    """

    div_under_related_question_pair = answer_block.find('div', class_=re.compile(
        r'related-question-pair')).find('div', recursive=False)

    items = [i for i in list(div_under_related_question_pair.children) if len(str(i)) > 10]

    if len(items) == 2:

        question = ''
        answer = ''

        question_tag, answer_tag = items
        question = question_tag.find('span').text

        first_two_tag_under_answer_tag = answer_tag.find_all('div', recursive=False)

        if len(first_two_tag_under_answer_tag) == 2:

            answer_tag = first_two_tag_under_answer_tag[0].find('div')
            answer_content = answer_tag.find_all('div', recursive=False)
            return answer_content.text

            # if len(answer_content) == 2:
            #     answer, source_url, publication_date = _tag_len_2(
            #         answer_content)
            #
            # if len(answer_content) == 3:
            #     answer, source_url, publication_date = _tag_len_3(
            #         answer_content)

    else:
        return None

def _get_questions(bs: BeautifulSoup, keyword: str) -> List:
    main_block = bs.find(
        'div', {
               "id": "rso", "data-async-context": f"query:{quote(keyword)}"})
    questions_block = main_block.find(
        'div', {"data-initq": f"{keyword.lower()}", "data-it": "rq"})
    questions = questions_block.select('div[data-sgrd="true"] > div')

    return questions

def parse_answers(html: str,
          keyword: str) -> list[tuple[Any, Any]]:
    """
    parse question and their answers from a page
    :param html: html content with questions_html
    :param keyword: keyword to search
    """

    questions_and_answers = []

    bs = BeautifulSoup(html, 'lxml')
    questions_html = _get_questions(bs, keyword)

    if questions_html:
        for question in questions_html:
            try:
                extract_answer(question)
                ques, ans = extract_answer(question)
                if ans:
                    questions_and_answers.append((ques, ans))

            except (AttributeError, IndexError):
                traceback.print_exc()
                pass

    return questions_and_answers
