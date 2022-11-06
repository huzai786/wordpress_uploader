import os
import webbrowser
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.action_chains import ActionChains
from jinja2 import Environment, FileSystemLoader
from selenium.webdriver.common.by import By
from db.crud import get_keywords_non_posted
from paascrape.browser import get_driver
import requests


def get_screen_shots():
    path = os.path.join(os.getcwd(), 'output.html')
    driver = get_driver()
    driver.get(f'file://{path}')
    driver.maximize_window()
    articles = driver.find_elements(By.TAG_NAME, 'article')
    action = ActionChains(driver)

    screen_shots = []
    for i, article in enumerate(articles):
        action.move_to_element(article).perform()
        name = article.get_attribute('class')
        name = '_'.join([i for i in name.split()])

        data = driver.get_screenshot_as_png()
        location = article.location
        size = article.size
        left, top, right, bottom = location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height']

        im = Image.open(BytesIO(data))
        im.crop((left, top, right, bottom))
        img_byte_arr = BytesIO()
        im.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        img = Image.open(BytesIO(img_byte_arr))
        img.show(name)
        screen_shots.append((name, img_byte_arr))

    driver.quit()
    return screen_shots


def update_html():
    kws = get_keywords_non_posted()[0][2]
    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template('template.html')
    content = template.render(questions=kws)
    with open('output.html', 'w') as f:
        f.write(content)
    webbrowser.open('output.html')




# get_screen_shots()
# update_html()


