from pytest import fixture

def pytest_addoption(parser):
    parser.addoption(
        '--username',
        type=str,
        action='store',
        help='the username of leetcode'
    )

    parser.addoption(
        '--password',
        type=str,
        action='store',
        help='the password of leetcode'
    )

@fixture(name='username', scope='session')
def _username(request):
    return request.config.getoption('username')

@fixture(name='password', scope='session')
def _password(request):
    return request.config.getoption('password')
