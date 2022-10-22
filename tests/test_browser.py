import os

from paascrape.browser import get_page_source

def get_keywords(fn):
    fn = f'test_sample/{fn}'
    if os.path.exists(fn):
        with open(fn, 'r') as file:
            keywords = file.readlines()
            for k in keywords:
                k = k.replace('\n', '')
                yield k

def test_get_page_source_sample_set_1():
    keywords = get_keywords('sample_set1.txt')
    for k in keywords:
        print(k)
        assert type(get_page_source(k)) == str

