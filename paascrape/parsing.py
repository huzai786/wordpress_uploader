import re
import csv
import traceback
from typing import Union
from urllib.parse import quote

from bs4 import Tag, BeautifulSoup

from .question import Questions


def tag_len_2(answer_content):
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


def tag_len_3(answer_content):
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


def extract_data(html: Tag) -> Union[Questions, None]:
    qs_data = html.find('div', class_=re.compile(
        r'related-question-pair')).find('div', recursive=False)
    items = [i for i in list(qs_data.children) if len(str(i)) > 10]

    if len(items) == 2:

        question = None
        answer = None
        source_url = None
        publication_date = None
        question_tag = items[0].find('span')
        if question_tag:
            question = question_tag.text

        main_content = items[1].find_all('div', recursive=False)

        if len(main_content) == 2:
            # div that contains 2 or more divs with only id attribute
            answer_tag = main_content[0].find('div')
            answer_content = answer_tag.find_all('div', recursive=False)

            if len(answer_content) == 2:
                answer, source_url, publication_date = tag_len_2(
                    answer_content)

            if len(answer_content) == 3:
                answer, source_url, publication_date = tag_len_3(
                    answer_content)
        question_object = Questions(
            question=question,
            answer=answer,
            source_url=source_url,
            publication_date=publication_date)
        return question_object

    else:
        return None


def parse(html, query):
    """parse question and their answers from a page"""
    bs = BeautifulSoup(html, 'lxml')
    try:
        main_block = bs.find(
            'div', {
                "id": "rso", "data-async-context": f"query:{quote(query)}"})

        parent = main_block.find(
            'div', {"data-initq": f"{query.lower()}", "data-it": "rq"})

        questions = parent.select('div[data-sgrd="true"] > div')
        with open(f'output/{query}_questions.csv', 'w', newline='', encoding='utf-8') as csv_file:
            question_writer = csv.writer(
                csv_file, delimiter='|', quoting=csv.QUOTE_MINIMAL)
            question_writer.writerow(
                ['question', 'answer', 'source url', 'publication date'])
            for question in questions:
                question_details = extract_data(question)
                if question_details:
                    question_writer.writerow(
                        [question_details.question, question_details.answer,
                         question_details.source_url, question_details.publication_date]
                    )

    except (AttributeError, IndexError):
        traceback.print_exc()
