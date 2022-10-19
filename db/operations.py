"""crud operations"""
import os
from typing import List, Tuple
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session

from db.model import Category, Keyword, Question, Base

e = create_engine(f'sqlite:///{os.getcwd()}\\database.db')

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


def add_keyword_to_db(parent_id: int, keyword_name: str):
    """
    add keyword to database with category as parent_id
    """

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

def get_category_keywords_details(wp_category_id):
    global e
    with Session(e) as session:

        # category = session.execute(select(Category).where(Category.wp_id == wp_category_id)).first()
        keyword_details = session.execute(select(Keyword).where(Keyword.parent_category.wp_id == wp_category_id)).all()
        details_table = [[], [], [], []]
        if keyword_details:
            details_table = [[i.name, i.is_processed, i.is_posted, len(i.questions)] for i in keyword_details]

        return details_table


if __name__ == '__main__':
    Base.metadata.create_all(bind=e)


