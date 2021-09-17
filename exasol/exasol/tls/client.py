import hashlib
import logging
import signal
import socket 
import ssl
import sys

from time import localtime, time, strftime
from typing import List

from statemachine import statemachine as sm 
from utils.miner import mine

logger = logging.getLogger('exasol.' + __name__)

class TlsClientError(Exception):
    '''[summary]

    Args:
        Exception (Exception): Exception raised by the TLS client
    '''

    def __init__(self, signum, frame):
        self.logger = logging.getLogger('exasol')
        self.logger.error(f'Signal {signum} received')


def _shutdown(signum: int, frame: int):
    '''Raises an exception to stop the TLS client cleanly

    Args:
        signum (int): received signal
        frame (int): frame

    Raises:
        TlsClientError: Exception raised when this function is invoked
    '''
    raise TlsClientError(signum, frame)

def start(server: str, ports: List, certificate: str, pk: str) -> None:
    '''Starts the TLS client

    Args:
        server (str): Server to connect the client to
        ports (List): List of valid ports the server listens to
        certificate (str): Location of the server's certificate file
        pk (str): Location of the server's private key's file
    '''
    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)

    logger.info('Signal handlers configured')

    try:
        tec = TlsExasolClient(server, ports, certificate, pk)
        tec.run()

    except TlsClientError:
        if tec:
            tec.stop()

        logger.info('TlsExasolClient terminated. Exiting...')
        sys.exit(0)

class TlsExasolClient():
    '''TLS client to connect to Exasol's TLS server
    '''
    def __init__(self, server: str, ports: List, cert: str, key:str, timeout_s:int = 6):
        '''Constructor

        Initializes class members

        Args:
            server (str): Server to connect to
            ports (List): List of ports to connect to
            cert (str): Server's certificate file location
            key (str): Server's private key file location
            timeout_s (int, optional): Connection timeout. Defaults to 65.
        '''
        self.logger = logging.getLogger('exasol.' + __name__ + type(self).__name__)
        self.server = server
        self.ports = ports 
        self.cert = cert 
        self.key = key
        self.timeout_s = timeout_s

        self.sock = None
        self.conn = None
        self.context = None

    def run(self):
        '''Sets up a connection to the server and runs the communication protocol
        '''
        NEW_LINE_ENC = '\n'.encode()
        SHA = hashlib.sha1

        self.context = ssl.SSLContext()
        self.context.load_cert_chain(self.cert, keyfile=self.key)

        self.sock = socket.socket(socket.AF_INET)
        self.sock.settimeout(self.timeout_s)
        self.conn = self.context.wrap_socket(self.sock)

        for port in self.ports: 
            try: 
                self.conn.connect((self.server, port))

            except Exception as e:
                self.logger.warning(e)

            else:
                self.logger.info(f'Connected to server')
                break
        
        else:
            self.logger.error(f'Could not connect to server on any of the available ports')
            return


        fsm = sm.ExasolFsm(self.conn)
        while fsm.current_state != fsm.end and fsm.current_state != fsm.error:
            received = self.conn.read().decode().strip().split(' ')
            fsm.run(received)

        self.looger.info(f'Done with state: {fsm.current_state}')
        fsm.reset()

        self.conn.close()

        # authdata = ''
        # while True: 
        #     args = self.conn.read().decode().strip().split(' ')
        #     self.logger.info(f'Got {args}')

        #     if args[0] == 'HELO':
        #         self.conn.send('EHLO\n'.encode())
        #         self.logger.info('Received HELO, replied EHLO')
        #         continue 

        #     elif args[0] == 'ERROR':
        #         self.logger.error(f'In ERROR {" ".join(args[1:])}. Exiting...')
        #         break

        #     elif args[0] == 'POW':
        #         self.sock.settimeout(2 * 60 * 60)
        #         authdata, difficulty = args[1], int(args[2])
        #         start = time()
        #         self.logger.info(f'started mining @{strftime("%H:%M:%S", localtime(start))}')

        #         nonce, suffix = mine(authdata, difficulty)
        #         self.logger.info(f'Found nonce {nonce}, suffix {suffix}, took {time() - start}')
        #         self.conn.send(suffix + NEW_LINE_ENC)

        #     elif args[0] == 'END':
        #         self.logger.info('in END')
        #         # if you get this command, then your data was submitted
        #         self.conn.send('OK\n'.encode())
        #         break

        #     # the rest of the data server requests are required to identify you
        #     # and get basic contact information
        #     elif args[0] == 'NAME':
        #         self.logger.info('in NAME')
        #         name = [b'Carlos', b'Ghabrous', b'Larrea']
        #         payload = SHA(authdata + args[1]).digest() + b' ' + b' '.join(name) + b'\n'
    
        #         # as the response to the NAME request you should send your full name
        #         # including first and last name separated by single space
        #         self.conn.send(payload)
        #         continue

        #     elif args[0] == 'MAILNUM':
        #         self.logger.info('in MAILNUM')
        #         payload = SHA(authdata + args[1]).digest() + b' ' + b'1\n'
        #         # here you specify, how many email addresses you want to send
        #         # each email is asked separately up to the number specified in MAILNUM
        #         self.conn.send(payload)
        #         continue

        #     elif args[0] == 'MAIL1':
        #         self.logger.info('in MAIL1')
        #         payload = SHA(authdata + args[1]).digest() + b' ' + b'carlos.ghabrous@gmail.com\n'
        #         self.conn.send(payload)
        #         continue

        #     elif args[0] == 'MAIL2':
        #         self.logger.info('in MAIL2')
        #         payload = SHA(authdata + args[1]).digest() + b' ' + b'carlos.ghabrous@gmail.com\n'
        #         self.conn.send()
        #         continue

        #     elif args[0] == 'SKYPE':
        #         self.logger.info('in SKYPE')
        #         # here please specify your Skype account for the interview, or N/A
        #         # in case you have no Skype account
        #         payload = SHA(authdata + args[1]).digest() + b' ' + b'carlosghabrous\n'
        #         self.conn.send(payload)
        #         continue

        #     elif args[0] == 'BIRTHDATE':
        #         self.logger.info('in BIRTHDATE')
        #         # here please specify your birthdate in the format %d.%m.%Y
        #         payload = SHA(authdata + args[1]).digest() + b' ' + b'04.02.1980\n'
        #         self.conn.send(payload)
        #         continue

        #     elif args[0] == 'COUNTRY':
        #         self.logger.info('in COUNTRY')
        #         # country where you currently live and where the specified address is
        #         # please use only the names from this web site:
        #         # https://www.countries-ofthe-world.com/all-countries.html
                
        #         payload = SHA(authdata + args[1]).digest() + b' ' + b'Switzerland\n'
        #         self.conn.send(payload)
        #         continue

        #     elif args[0] == 'ADDRNUM':
        #         self.logger.info('in ADDRNUM')
        #         # specifies how many lines your address has, this address should
        #         # be in the specified country
        #         payload = SHA(authdata + args[1]).digest() + b' ' + b'2\n'
        #         self.conn.send(payload)
        #         continue

        #     elif args[0] == 'ADDRLINE1':
        #         self.logger.info('in ADDRLINE1')
        #         payload = SHA(authdata + args[1]).digest() + b' ' + b'Rue du Beulet,8\n'
        #         self.conn.send(payload)
        #         continue

        #     elif args[0] == 'ADDRLINE2':
        #         self.logger.info('in ADDRLINE2')
        #         payload = SHA(authdata + args[1]).digest() + b' ' + b'1203 Geneva\n'
        #         self.conn.send(payload)
        #         continue


    def stop(self):
        self.logger.info('Client stopped')

