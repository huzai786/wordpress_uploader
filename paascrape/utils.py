import re
from typing import Optional

from bs4 import ResultSet

from paascrape.container import AnswerType, Answer


def _youtube_check(divs: ResultSet,
                   answer_class: Answer) -> Optional[Answer]:
    for div in divs:
        link = div.find('a', {"ping": re.compile(r'/url?')}, href=re.compile(r'https://www.youtube.com/watch'))
        if link:
            answer_class.answer_type = AnswerType.Youtube
            answer_class.answer = link['href']
            return answer_class

    return None


def _get_table(table):
    table_data = []
    trs = table.find_all('tr')
    for tr in trs:
        table_headers = tr.find_all('th')
        table_rows = tr.find_all('td')
        if table_headers:
            table_data.append([i.text for i in table_headers])
        if table_rows:
            table_data.append([i.text for i in table_rows])

    return table_data


def _table_check(divs: ResultSet,
                 answer_class: Answer):
    for div in divs:
        table = div.find('table')
        if table:
            table_heading = div.find('div', {"role": "heading"})
            truncated_info_link = div.find('div', class_="webanswers-webanswers_table__webanswers-table")
            if truncated_info_link:
                links = truncated_info_link.find_all('a')
                if links:
                    for a in links:
                        if 'more' in a.text:
                            answer_class.Truncated_info_link = a['href']
                            break

            if table_heading:
                answer_class.answer_heading = table_heading.text

            answer_class.answer = _get_table(table)
            answer_class.answer_type = AnswerType.Table

            return answer_class

    return None


def _get_list(ol_ul):
    ans_list = []
    for li in ol_ul.find_all('li'):
        ans_list.append(li.text)
    return ans_list


def _list_check(divs: ResultSet,
                answer_class: Answer):
    for div in divs:
        ul_or_ol = div.find(['ul', 'ol'])
        if ul_or_ol:
            answer_class.answer = _get_list(ul_or_ol)
            heading = div.find('div', {"role": "heading"})
            if heading:
                answer_class.answer_heading = heading.text

            more_item_link = div.find('a', class_="truncation-information")
            if more_item_link:
                answer_class.Truncated_info_link = more_item_link['href']
            answer_class.answer_type = AnswerType.List
            return answer_class

    return None


def _get_paragraph_answer(divs: ResultSet,
                          answer_class: Answer):
    answer_class.answer_type = AnswerType.Paragraph
    for div in divs:
        para = div.find('div', {"role": "heading", "data-attrid": "wa:/description"})
        if para:
            answer_para = para.text
            date_check = re.findall(r"([0-9]{2}-(Jun|Feb|Jan|Mar|Apr|May|Jul|Aug|Sept|Oct|Nov|Dec)-[0-9]{4})$",
                                    answer_para)
            if date_check:
                answer_para = answer_para.removesuffix(date_check[0][0])

            answer_class.answer = answer_para
            break
        else:
            heading = div.find('div', {"role": "heading"})
            if heading:
                answer_class.answer_heading = heading.text
            else:
                ans = div.text.replace('\n', '')
                if ans:
                    answer_class.answer = ans

    if answer_class.answer and 'YouTubeYouTubeStart' not in answer_class.answer:
        return answer_class
    else:
        return None



