from typing import List
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class Tag(BaseModel):
    name: str
    slug: str
    type: str = Field(alias='tagType')

class Article(BaseModel):
    type_name: str = Field(alias='__typename')
    is_official: bool = Field(alias='byLeetcode')
    content: str
    create_time: datetime = Field(alias='createdAt')
    slug: str
    tags: List[Tag]
    title: str

class Data(BaseModel):
    article: Article = Field(alias='solutionArticle')

class ArticleResponse(BaseModel):
    data: Data

    @property
    def content(self):
        return self.data.article.content
