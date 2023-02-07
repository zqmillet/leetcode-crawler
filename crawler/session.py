from http import HTTPStatus
from requests import Session as BaseSession
from requests.models import Response
from urllib.parse import unquote
from json import loads
from base64 import b64decode
from time import sleep
from pydantic import BaseModel
from pydantic import Field
from typing import Optional
from typing import List
from typing import Any
from zlib import decompress
from base64 import b64decode
from json import loads

def assert_status_code(response: Response) -> None:
    if not response.status_code == HTTPStatus.OK:
        raise ValueError(f'response status is {response.status_code}')

class SubmissionResult(BaseModel):
    status: str = Field(alias='state')
    output: str = Field(alias='std_output')
    submission_id: int
    testcase_number: int = Field(alias='total_testcases')
    correct_number: int = Field(alias='total_correct')

    @property
    def testcases(self) -> List[List[Any]]:
        return loads(decompress(b64decode(self.output)))

class Session(BaseSession):
    def __init__(self, username: str, password: str, endpoint: str = 'leetcode.cn'):
        self.username = username
        self.password = password

        self.login_url = f'https://{endpoint}/accounts/login'
        self.endpoint = endpoint
        super().__init__()

        response = self.get(self.login_url, verify=False)
        assert_status_code(response)

        response = self.post(
            url=self.login_url,
            data={'login': username, 'password': password},
            headers={'Referer': self.login_url}
        )
        assert_status_code(response)

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
        assert_status_code(response)
        return response.json()['submission_id']

    def check(self, submission_id, timeout: int = 10, interval: int = 1) -> SubmissionResult:
        for _ in range(timeout):
            sleep(1)

            response = self.get(
                url=f'https://{self.endpoint}/submissions/detail/{submission_id}/check/'
            )
            assert_status_code(response)
            status = response.json()

            if status == 'SUCCESS':
                break

        return SubmissionResult.parse_raw(response.text)
