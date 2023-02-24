from typing import List

from pydantic import BaseModel
from pydantic import Field

class Node(BaseModel):
    is_official: bool = Field(alias='byLeetcode')
    slug: str
    title: str
    hit_count: int = Field(alias='hitCount')

class Edge(BaseModel):
    type_name: str = Field(alias='__typename')
    node: Node

class Articles(BaseModel):
    edges: List[Edge]

class Data(BaseModel):
    articles: Articles = Field(alias='questionSolutionVideoArticles')

class ArticleMetadataResponse(BaseModel):
    data: Data

    @property
    def article_metadata_array(self):
        return [edge.node for edge in self.data.articles.edges]
