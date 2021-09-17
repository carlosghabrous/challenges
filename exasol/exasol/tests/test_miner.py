import pytest

import time

from exasol.utils.miner import mine

UPPER_LIMIT_S = 2 * 60 * 60

@pytest.mark.parametrize('authdata', ['UZyTPgfwUqevkbyqTZmhXzBPqAfQiPBWOKaXFqLxQWawsJnWLNVGZezDJKgffDvZ'])
@pytest.mark.parametrize('difficulty', [i for i in range(1, 10)])
def test_miner(authdata, difficulty):
    start = time.time()
    print(f'Difficulty {difficulty}, started @{time.strftime("%H:%M:%S", time.localtime(start))}')

    while 1: 
        try: 
            suffix = mine(authdata, difficulty)

        except UnicodeError as e:
            print(f'{e}')

        else:
            break 

    stop = time.time()
    print(f'Suffix: {suffix}, took {stop - start}')
    assert (stop - start) < UPPER_LIMIT_S