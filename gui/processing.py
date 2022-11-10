import os
from typing import Tuple, List

from jinja2 import Environment, FileSystemLoader
from requests import RequestException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from db.crud import (
    get_keywords_unprocessed,
    add_keyword_questions_to_db,
    get_keywords_non_posted,
    update_keyword_status_processed,
    delete_keyword_from_db,
    get_keyword_post_id,
    get_keyword_media_ids
)
from paascrape.browser import get_driver
from paascrape.parsing import get_answers
from wp_api.operation import (
    create_post,
    delete_keyword_from_wp,
    delete_post_from_wp,
    upload_image, delete_media_from_wp
)


def process_keywords():
    """get all non-processed keywords and scrape questions from each keyword then finally dump them in the database"""

    keywords = get_keywords_unprocessed()
    if not keywords:
        return

    for keyword_id, keyword_string in keywords:
        print()
        answers = get_answers(keyword_string)
        if not answers:
            print(f'keyword: "{keyword_string}"  -FAILED! NO PAA')
            continue

        content = render_html(answers)
        path = os.path.join(os.getcwd(), 'templates', keyword_string.split()[0] + '.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        screen_shots = cropped_questions(path)
        if not screen_shots:
            print(f'keyword: "{keyword_string}"  -FAILED! NO SCREENSHOTS')
            os.unlink(path)
            break

        keyword_data = []
        for ss in screen_shots:
            question_data: dict = ss[0]  # {"name": name, "link": qs_link}
            image_in_byte: bytes = ss[1]  # ByteArray
            wp_image = upload_image(question_data['name'], image_in_byte)
            if not wp_image:
                os.unlink(path)
                break

            image_id, image_url = wp_image
            question_string = ' '.join([i for i in question_data['name'].split('_')])
            data = {"question": question_string, "url": image_url, "image_id": image_id, 'link': question_data['link']}
            keyword_data.append(data)
            print(f'keyword: "{keyword_string}"  -FAILED!')

        excerpt = next([i.question, i.answer] for i in answers if i.answer_type.value == 'paragraph')
        excerpt = excerpt[0] + "\n" + excerpt[1]
        add_keyword_questions_to_db(keyword_id, excerpt, keyword_data)
        os.unlink(path)


def post_keywords_data() -> None:
    """
    get all keywords that has is_processed=True and is_posted=False
    :return: None
    """
    keywords_data = get_keywords_non_posted()  # namedtuple('Keyword_data', ['keyword_name', 'keyword_id', 'excerpt'
    # "render_data"])
    if not keywords_data:
        return

    for keyword_data in keywords_data:
        # create a post content from the keywords questions
        html_content = __generate_content(keyword_data.render_data)

        # post the content
        post_id = create_post(keyword_data.keyword_id, keyword_data.keyword_name, keyword_data.excerpt, html_content)
        if post_id:
            update_keyword_status_processed(keyword_data.keyword_id, post_id)


def delete_keyword(keywords: set,
                   cat_id: int) -> bool:
    for keyword_id in keywords:

        post_id, media_ids = get_keyword_post_id(keyword_id), get_keyword_media_ids(keyword_id)
        if post_id:
            try:
                delete_post_from_wp(post_id)
            except RequestException:
                return False

        if media_ids:
            try:
                for i in media_ids:
                    delete_media_from_wp(i)

            except RequestException:
                return False

        kw_deleted = delete_keyword_from_wp(keyword_id)
        if kw_deleted:
            delete_keyword_from_db(cat_id, keyword_id)
        else:
            return False

    return True


def __generate_content(render_data: List[Tuple[str, str, str]]):
    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template('render_images.html')
    content = template.render(urls=render_data)

    return content


def render_html(keywords):
    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template('template.html')
    content = template.render(questions=keywords)
    return content


def cropped_questions(path):
    driver = get_driver()
    driver.get(f'file://{path}')
    driver.implicitly_wait(10)
    action = ActionChains(driver)
    articles = driver.find_elements(By.TAG_NAME, 'article')

    screen_shots = []
    for i, article in enumerate(articles):

        driver.implicitly_wait(10)
        article.location_once_scrolled_into_view
        action.move_to_element(article).perform()
        name = article.get_attribute('class')
        qs_link = article.get_attribute('link')
        name = '_'.join([r for r in name.split()]).replace('?', '').replace('.', '')
        img_data = article.screenshot_as_png
        screen_shots.append(({"name": name, "link": qs_link}, img_data))

    driver.quit()
    return screen_shots
