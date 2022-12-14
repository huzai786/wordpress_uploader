from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    wp_id = Column(Integer, nullable=False, unique=True, index=True)
    name = Column(String)

    child_categories = relationship(
        "Keyword",
        back_populates="parent_category",
        cascade="all, delete-orphan")

    def __repr__(self):
        return f"<wp id: {self.wp_id}, category name: {self.name}>"


class Keyword(Base):
    __tablename__ = "keyword"

    id = Column(Integer, primary_key=True)
    wp_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    excerpt = Column(String, nullable=True)
    questions = relationship(
        "Question", back_populates="keyword", cascade="all, delete-orphan")
    is_processed = Column(Boolean, nullable=True, default=False)
    is_posted = Column(Boolean, nullable=True, default=False)
    post_id = Column(String, nullable=True)

    category_id = Column(String, ForeignKey('category.id'), nullable=True)
    parent_category = relationship(
        "Category", back_populates="child_categories")

    def __repr__(self):
        return f"<id: {self.wp_id}, keyword name: {self.name}>"


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    question_string = Column(String)
    image_url = Column(String)
    image_wp_id = Column(String)
    link = Column(String, nullable=True)
    keyword_id = Column(Integer, ForeignKey('keyword.id'), nullable=False)
    keyword = relationship("Keyword", back_populates='questions')

    def __repr__(self):
        return f"<question: {self.question}>"
