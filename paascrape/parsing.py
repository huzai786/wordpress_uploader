import re
import traceback
from typing import Optional, List, Any, Tuple

from bs4 import Tag, BeautifulSoup


def check_youtube(div: Tag) -> Optional[str]:
    link = div.find('a', href=re.compile(r'https://www.youtube.com/watch'))
    if link:
        return link['href']


def extract_answer(answer_block: Tag) -> Tuple:
    """
    Takes a html blob of single question and returns its relevant answer.

    :param answer_block: Bs4 Tag element containing the relevant data
    """
    question = None
    answer = []

    div_under_related_question_pair = answer_block.find('div', class_=re.compile(
        r'related-question-pair')).find('div', recursive=False)

    items = [i for i in list(div_under_related_question_pair.children) if len(str(i)) > 10]

    if len(items) == 2:
        question_tag, answer_tag = items

        question = question_tag.find('span').text
        first_two_tag_under_answer_tag = answer_tag.find_all('div', recursive=False)

        if len(first_two_tag_under_answer_tag) == 2:

            answer_tag = first_two_tag_under_answer_tag[0].find('div')
            divs_with_only_id = answer_tag.find_all('div', recursive=False)

            for div in divs_with_only_id[:-1]:
                youtube_video_url = check_youtube(div)
                if youtube_video_url:
                    answer.append(youtube_video_url)
                    break

                ans = div.text.replace('\n', '')

                if ans:
                    more_rows_check = re.findall(r"more rows$", ans)
                    more_item_check = re.findall(r"More items\.\.\.$", ans)
                    if more_item_check or more_rows_check:
                        break
                    date_check = re.findall(r"([0-9]{2}-(Jun|Feb|Jan|Mar|Apr|May|Jul|Aug|Sept|Oct|Nov|Dec)-[0-9]{4})$", ans)
                    if date_check:
                        ans = ans.removesuffix(date_check[0][0])

                    answer.append(ans)

    return question, answer


def _get_questions(html: str,
                   ) -> Optional[List]:
    """returns all questions"""

    bs = BeautifulSoup(html, 'lxml')
    try:
        main_block = bs.find(
            'div', {
                "id": "rso", "data-async-context": re.compile(r'query:')})

        questions = main_block.select(
            'div[data-sgrd="true"] > div')

        return questions

    except AttributeError:
        return None


def get_answers_from_source(html: str) -> list[tuple[Any, Any]]:
    """
    parse question and their answers from a page.

    :param html: html content with questions_html
    """

    questions_and_answers = []

    questions_html = _get_questions(html)
    print(len(questions_html))
    if questions_html:
        if len(questions_html) > 20:
            for question in questions_html:
                qna = extract_answer(question)
                if qna[1]:
                    questions_and_answers.append((qna[0], qna[1]))

    return questions_and_answers
