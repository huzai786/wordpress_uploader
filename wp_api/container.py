from dataclasses import dataclass


@dataclass
class PostData:
    title: str = None
    content: str = None
    excerpt: str = None
    slug: str = None
    status: str = 'publish'
