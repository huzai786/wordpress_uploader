from paascrape.parsing import parse_answers, extract_answer
from bs4 import BeautifulSoup

with open('questions.html', 'r', encoding='utf-8') as f:
    data = f.read()


for q in data:
    ques = BeautifulSoup(q, 'lxml')
    question, answer = extract_answer(ques)








