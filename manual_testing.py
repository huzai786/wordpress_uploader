from paascrape.parsing import get_answers_from_source
from paascrape.browser import get_page_source

q = 'Confit Tomato'

html = get_page_source(q)
if html:
    qna = get_answers_from_source(html)
    for qa in qna:
        print(qa)
        print('===============================')









