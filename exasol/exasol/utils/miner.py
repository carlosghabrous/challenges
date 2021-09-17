import hashlib
import logging
import multiprocessing as mp

logger = logging.getLogger('exasol.' + __name__)

# Avoid: 
# tab: 9
# new line: 10
# carriage return: 13
# space: 32 
AVOID = [b'\t', b'\n', b'\r', b' ']
LEN_BYTES = 8
MAX_PROCESSES = 4


# def worker(authdata: str, difficulty: int, goal: str, block_size: int, sweep_q: Queue, res_q: Queue, stop_event: Event) -> None:
#     hash_list = list([authdata.encode(), b''])

#     # AVOID SOME DOTS
#     join_str = b''.join
#     hash_op = hashlib.sha1

#     nonce = sweep_q.get()
#     upper_limit = nonce + block_size 

#     logger.info(f'-> CONSUMER: starting sweeping from {nonce} to {upper_limit}...')
#     while not stop_event.is_set():

#         if nonce >= upper_limit:
#             nonce = sweep_q.get()
#             upper_limit = nonce + block_size

#         hash_list[1] = int(nonce).to_bytes(LEN_BYTES, 'big')
#         hash_value = hash_op(join_str(hash_list)).hexdigest()

#         if hash_value[:difficulty] != goal:
#             nonce += 1
#             continue 

#         if any([c in hash_list[1] for c in AVOID]):
#             logger.info(f'-> CONSUMER: Nonce {nonce} forbidden char in string {hash_list[1]}')
#             nonce += 1
#             continue 
    
#         logger.info(f'-> CONSUMER: Found nonce {nonce}, hash {hash_value}, suffix {hash_list[1]}')
#         if res_q.empty():
#             res_q.put((nonce, hash_value, hash_list[1]))

#         stop_event.set()

#     logger.info(f'-> CONSUMER: Done')

# def mine(authdata: str, difficulty: int) -> bytes:
    # '''The miner

    # It uses four processes to find nonce values in different number ranges. 

    # Args:
    #     authdata ([type]): Authorization string coming from the server
    #     difficulty (int): Number of leading nibbles the hash value must have

    # Returns:
    #     [type]: [description]
    # '''
#     goal = '0' * difficulty
#     block_size = 2**(4*difficulty)
    
#     stop_event = mp.Event()
#     q = mp.Queue()
#     _ = [q.put(i*block_size) for i in range(MAX_PROCESSES)]
#     result = mp.Queue()

#     consumers = [mp.Process(target=worker, args=(authdata, difficulty, goal, block_size, q, result, stop_event), 
#                             name='p-' + str(i)) for i in range(MAX_PROCESSES)]

#     for p in consumers:
#         p.start()

#     for p in consumers:
#         p.join()

#     _, _, suffix = result.get()
#     return suffix
    

def mine(authdata, difficulty) -> bytes:
    '''The miner

    With high difficulties, i.e., 9, the probability of finding a nonce is (1/2)**(4*difficulty).
    This number translates to ~ 1 out of 68 billion numbers satisfy the proof of work condition. 
    I did not check whether the forbidden characters are included in this nonce because the probability is very low, 
    and it would be further diminished by the number of unicode characters, 143,859. 

    Args:
        authdata (str): Authorization string coming from the server
        difficulty (int): Number of leading nibbles the hash value must have

    Returns:
        [type]: The nonce in a byte string form
    '''
    goal = '0' * difficulty
    hash_value = ''
    hash_list = list([authdata.encode(), b''])

    # AVOID SOME DOTS
    join_str = b''.join
    SHA1 = hashlib.sha1
    nonce = 0

    while True:
        hash_list[1] = nonce.to_bytes(LEN_BYTES, 'big')
        hash_value = SHA1(join_str(hash_list)).hexdigest()

        if hash_value[:difficulty] != goal:
            nonce += 1
            continue 

        break

    return hash_list[1]
