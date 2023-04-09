import os


def pytest_scope_func() -> str:
    env = os.getenv('PYTEST_CURRENT_TEST')
    if not env:
        raise RuntimeError('PYTEST_CURRENT_TEST not found')

    return env.split(' ')[0]
