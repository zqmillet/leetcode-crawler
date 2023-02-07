from crawler.session import Session
from textwrap import dedent

from zlib import decompress
from base64 import b64decode
from json import loads


def test_submit(username, password):
    session = Session(username=username, password=password)

    submission_id = session.submit(
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

    submission_result = session.check(submission_id)
    assert len(submission_result.testcases) == 57
