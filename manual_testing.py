from paascrape.parsing import get_answers_from_source
from paascrape.browser import get_page_source

q = 'Crema Catalana'

html = get_page_source(q)
if html:
    qna = get_answers_from_source(html)
    print(*qna, sep='\n=========================\n')
    print(len(qna))







