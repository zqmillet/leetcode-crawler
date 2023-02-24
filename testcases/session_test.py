from textwrap import dedent

from pytest import fixture

from crawler.session import Session

@fixture(name='session', scope='session')
def _session(username, password):
    return Session(username=username, password=password)

def test_submit(session):
    submission_request = session.submit(
        question_id='1',
        question_slug='two-sum',
        language='python3',
        code=dedent(
            '''
            from zlib import compress
            from base64 import b64encode
            from json import dumps

            def encode(text: str) -> str:
                compressed_bytes = compress(text.encode('utf8'))
                return b64encode(compressed_bytes).decode('utf8')

            class Recorder:
                def __init__(self, total):
                    self.total = total
                    self.index = 0
                    self.inputs = []

                def __call__(self, function):
                    def wrapper(_, *args):
                        self.index += 1
                        self.inputs.append(list(args))

                        if self.index == self.total:
                            print(encode(dumps(self.inputs)))
                            raise Exception('bingo')
                        else:
                            return function(_, *args)
                    return wrapper

            class Solution:
                @Recorder(total=57)
                def twoSum(self, nums: List[int], target: int) -> List[int]:
                    hashtable = dict()
                    for i, num in enumerate(nums):
                        if target - num in hashtable:
                            return [hashtable[target - num], i]
                        hashtable[nums[i]] = i
                    return []
            '''
        ).strip()
    )

    submission_result = session.get_result(submission_request.submission_id)
    assert submission_result.testcase_number > 0

def test_get_solutions(session):
    solutions = list(session.get_solutions('two-sum', language='Python'))
    assert len(solutions) == 2
