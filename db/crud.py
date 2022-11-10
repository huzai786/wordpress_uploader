"""crud operations"""
import os
from collections import namedtuple
from typing import List, Tuple, Optional

from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session

from db.models import Category, Keyword, Question

# initiate a engine
e = create_engine(f'sqlite:///{os.getcwd()}\\database.db')

keyword_detail = namedtuple('Keyword_data', ['keyword_name', 'keyword_id', "excerpt", "render_data"])


def add_category_to_db(category_id: int,
                       category_name: str) -> None:
    """
    add category to local database, will be done after creating category in word press
    :param category_id: word press category id
    :param category_name: word press category id
    """
    global e

    with Session(e) as session:
        category = Category(wp_id=category_id, name=category_name)
        session.add(category)
        session.commit()


def delete_category_from_db(wp_id: int) -> None:
    """
    delete category to local database, will be done after delete category in word press
    """
    global e

    with Session(e) as session:
        session.execute(delete(Category).where(Category.wp_id == wp_id))
        session.commit()


def get_categories_from_db() -> List[Tuple]:
    """
    get a list of all categories along with their word press ids.
    :return: list tuples of categories names and id
    """
    global e

    with Session(e) as session:
        results = session.query(Category).all()
        categories = [(i.wp_id, i.name) for i in results]

        return categories


def add_keyword_to_db(
        parent_id: int,
        keyword_wp_id,
        keyword_name: str) -> None:
    """
    add keyword to database with category as parent_id
    :param keyword_wp_id: keyword.wp_id
    :param parent_id: category.wp_id that it will belong to
    :param keyword_name: name of the keyword
    """

    global e
    with Session(e) as session:
        cat = session.execute(select(Category).where(
            Category.wp_id == parent_id)).all()[0]
        keyword = Keyword(name=keyword_name, wp_id=keyword_wp_id)
        cat[0].child_categories.append(keyword)
        session.add(keyword)
        session.commit()


def delete_keyword_from_db(parent_id: int,
                           keyword_wp_id: int) -> None:
    """
    remove keyword from category.
    :param parent_id: category.wp_id
    :param keyword_wp_id: keyword.wp_id
    """
    global e

    with Session(e) as session:
        category = session.execute(select(Category).where(
            Category.wp_id == parent_id)).first()[0]
        keyword = session.execute(select(Keyword).where(
            Keyword.wp_id == keyword_wp_id)).first()[0]
        category.child_categories.remove(keyword)
        session.commit()


def get_cat_kw_details(wp_category_id):
    global e

    rows = []
    with Session(e) as session:
        stmt = select(Keyword).where(
            Keyword.parent_category.has(Category.wp_id == wp_category_id))
        keyword_details = session.execute(stmt).all()
        if not keyword_details:
            return rows

        for keyword in keyword_details:
            k = keyword[0]
            rows.append([k.wp_id, k.name, k.is_posted,
                         k.is_processed, len(k.questions)])

    return rows


def add_keyword_questions_to_db(keyword_id: int, excerpt: str, question_data_list: List[dict]) -> None:
    """
    Associate the questions data to a keyword.

    :param excerpt:
    :param question_data_list: list of dicts of keyword data
    :param keyword_id: keyword id to associate to
    """
    global e

    with Session(e) as session:
        keyword = session.execute(select(Keyword).where(Keyword.wp_id == keyword_id)).first()[0]
        for question_data in question_data_list:
            q = Question(question_string=question_data.get('question'), image_url=question_data.get('url'),
                         image_wp_id=question_data.get('image_id'), link=question_data.get('link'))

            keyword.questions.append(q)
            session.add(q)
        keyword.is_processed = True
        keyword.excerpt = excerpt
        session.commit()


def get_keywords_unprocessed():
    """get all non-processed keyword wp_ids and keyword names."""
    global e

    with Session(e) as session:
        kws = session.execute(select(Keyword).where(Keyword.is_processed == False)).all()
        return [(i[0].wp_id, i[0].name) for i in kws if kws]


def get_keywords_non_posted() -> list[keyword_detail]:
    """get all processed and not posted keywords"""
    global e
    keywords_data = []

    with Session(e) as session:
        kws = session.execute(select(Keyword).where(Keyword.is_processed == True, Keyword.is_posted == False)).all()
        for kw in kws:
            kw = kw[0]
            kw_name = kw.name
            kw_id = kw.wp_id
            excerpt = kw.excerpt
            images_url_and_link = [(i.image_url, i.link, i.question_string) for i in kw.questions]

            k = keyword_detail(keyword_name=kw_name, keyword_id=kw_id, excerpt=excerpt, render_data=images_url_and_link)

            keywords_data.append(k)

    return keywords_data


def update_keyword_status_processed(keyword_id: str,
                                    post_id: int) -> None:
    """
    add post_id to a keyword instance.

    :param keyword_id: Word press sub category id
    :param post_id: Word press post id
    """
    global e
    with Session(e) as session:
        kw = session.execute(select(Keyword).where(
            Keyword.wp_id == keyword_id)).first()[0]
        kw.post_id = post_id
        kw.is_posted = True
        session.commit()


def get_keyword_post_id(keyword_id: int):
    global e
    with Session(e) as session:
        kw = session.execute(select(Keyword).where(
            Keyword.wp_id == keyword_id)).first()[0]
        if kw.post_id:
            return kw.post_id
        else:
            return None

def get_keyword_media_ids(keyword_id: int) -> Optional[List]:
    global e
    with Session(e) as session:
        kw = session.execute(select(Keyword).where(
            Keyword.wp_id == keyword_id)).first()[0]
        if len(kw.questions) > 0:
            return [i.image_wp_id for i in kw.questions]

        return None

