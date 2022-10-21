from paascrape.browser import question_page
from paascrape.parsing import parse

keyword = 'what+are+the+12+rules+of+life'
html = question_page(query_keyword=keyword)
if html:
    parse(html, keyword)
else:
    print('paa section doesnt exists')


