import os
import webbrowser
from jinja2 import Environment, FileSystemLoader
from selenium.webdriver.common.by import By
from db.crud import get_keywords_non_posted
from paascrape.browser import get_driver
from selenium.webdriver.common.action_chains import ActionChains

path = os.path.join(os.getcwd(), 'output.html')


driver = get_driver(headless=False)
action = ActionChains(driver=driver)
driver.get(f'file://{path}')
articles = driver.find_elements(By.CLASS_NAME, 'article')


for i, article in enumerate(articles):
    action.move_to_element(article)
    driver.get_screenshot_as_file(f'media/{i}.png')
driver.quit()


# kws = get_keywords_non_posted()[0][2]
# env = Environment(loader=FileSystemLoader('templates/'))
# template = env.get_template('template.html')
# content = template.render(questions=kws)
# with open('output.html', 'w') as f:
#     f.write(content)
# webbrowser.open('output.html')




