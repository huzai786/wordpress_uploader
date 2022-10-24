from enum import Enum
from dataclasses import dataclass
from typing import Any


class AnswerType(Enum):
    Youtube = 'youtube'
    Table = 'table'
    List = 'list'
    Paragraph = 'paragraph'


@dataclass
class Answer:
    question: str = None
    answer_heading: str = None
    answer: Any = None
    answer_type: AnswerType = None
    Truncated_info_link: str = None
