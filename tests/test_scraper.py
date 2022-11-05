import os
import pytest

from exception import PAADoesNotExist
from paascrape.browser import get_page_source
from paascrape.parsing import get_answers_from_source


def get_keywords(fn):
    filepath = os.path.join(os.getcwd(), 'browser_test_data', fn)
    with open(filepath, 'r', encoding='utf-8') as file:
        keywords = file.readlines()
        for k in keywords:
            k = k.replace('\n', '')
            yield k


keywords_sample1 = get_keywords('sample_set1.txt')

# keywords_sample2 = get_keywords('sample_set2.txt')
@pytest.mark.parametrize('keyword', keywords_sample1)
def test_get_page_source_sample_set_2(keyword):
    try:
        html = get_page_source(keyword)
        qnas = get_answers_from_source(html)
        print(qnas[0])
        assert qnas

    except PAADoesNotExist:
        pass

