from http import HTTPStatus
from time import sleep
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from requests import Session as BaseSession
from requests.models import Response
from mistletoe import Document
from mistletoe.block_token import CodeFence

from .graphql_queries import QUERY_SOLUTIONS
from .graphql_queries import QUERY_SOLUTION
from .article_metadata_response import ArticleMetadataResponse
from .article_response import ArticleResponse

class SubmissionResult(BaseModel):
    status: str = Field(alias='state')
    output: str = Field(alias='std_output')
    submission_id: int
    testcase_number: int = Field(alias='total_testcases')
    correct_number: int = Field(alias='total_correct')

class SubmissionRequest(BaseModel):
    submission_id: int

class Solution(BaseModel):
    language: str
    code: str

class Session(BaseSession):
    def __init__(self, username: str, password: str, endpoint: str = 'leetcode.cn'):
        super().__init__()

        self.username = username
        self.password = password
        self.endpoint = endpoint

        self.login()

    def login(self):
        login_url = f'https://{self.endpoint}/accounts/login'
        self.get(login_url, verify=False)
        self.post(
            url=login_url,
            data={'login': self.username, 'password': self.password},
            headers={'Referer': login_url}
        )

    def request(self, *args, **kwargs) -> Response:
        response = super().request(*args, **kwargs)

        if not response.status_code == HTTPStatus.OK:
            raise ValueError(f'response status is {response.status_code}: {response.text}')

        return response

    def submit(self, question_id, question_slug, code, language) -> int:
        response = self.post(
            url=f'https://{self.endpoint}/problems/{question_slug}/submit/',
            json={
                "question_id": question_id,
                "lang": language,
                "typed_code": code,
                "test_mode": False,
                "test_judger": "",
                "questionSlug": question_slug
            },
            headers={
                'Referer': f'https://{self.endpoint}/problems/{question_slug}/submissions/',
            }
        )
        return SubmissionRequest.parse_raw(response.text)

    def get_result(self, submission_id, timeout: int = 10, interval: int = 1) -> SubmissionResult:
        for _ in range(timeout):
            sleep(interval)
            response = self.get(url=f'https://{self.endpoint}/submissions/detail/{submission_id}/check/')

            if not response.json().get('state') == 'STARTED':
                break

        return SubmissionResult.parse_raw(response.text)

    def get_article_metadata_array(self, question_slug: str, only_official: bool = True):
        url = f'https://{self.endpoint}/graphql/'
        response = self.post(
            url=url,
            json={
                "operationName": "questionSolutionVideoArticles",
                "variables": {
                    "questionSlug": question_slug,
                    "userInput": "",
                    "tagSlugs": [],
                },
                'query': QUERY_SOLUTIONS
            }
        )

        for metadata in ArticleMetadataResponse.parse_raw(response.text).article_metadata_array:
            if only_official and not metadata.is_official:
                continue
            yield metadata

    def get_articles(self, question_slug: str, only_official: bool = True):
        url = f'https://{self.endpoint}/graphql/'
        for metadata in self.get_article_metadata_array(question_slug, only_official):
            response = self.post(
                url=url,
                json={
                    "operationName": "solutionDetailArticle",
                    "variables": {
                        "slug": metadata.slug,
                        "orderBy": "DEFAULT"
                    },
                    'query': QUERY_SOLUTION
                }
            )
            article_response = ArticleResponse.parse_raw(response.text)
            yield Document(article_response.content)

    def get_solutions(self, question_slug: str, language: Optional[str] = None, only_official: bool = True):
        for markdown in self.get_articles(question_slug, only_official):
            for child in markdown.children:
                if not isinstance(child, CodeFence):
                    continue

                if language and not child.language == language:
                    continue

                if not child.children:
                    continue

                element, *_ = child.children
                yield Solution(language=child.language, code=element.content)
