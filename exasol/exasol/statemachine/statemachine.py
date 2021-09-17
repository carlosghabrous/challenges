import enum
import functools 
import logging
from hashlib import sha1 as SHA
from time import time, localtime, strftime

from exasol.utils.miner import mine

NEW_LINE_ENC = '\n'.encode()

authdata = ''

class State:
    def __init__(self):
        self.name = type(self).__name__
        self.transitions = None
        self.logger = logging.getLogger('exasol.' + __name__ + self.name)

    def next(self, state_input):
        try: 
            return self.transitions[state_input]

        except KeyError:
            return self.transitions['ERROR']

class FiniteStateMachine:
    def __init__(self, initial_state, conn):
        self.initial_state = initial_state
        self.current_state = initial_state
        self.conn = conn
        self.current_state.run()

    def run(self, args):
        try: 
            self.current_state = self.current_state.next(args[0])

        except KeyError:
            return 

        else: 
            self.current_state.run(conn=self.conn, data=args[1:])

    def reset(self):
        self.current_state = self.initial_state
        self.current_state.run()


# Own transitions    
class Message(enum.Enum):
    helo = 'HELO'
    pow = 'POW'
    end = 'END'
    error = 'ERROR'
    name = 'NAME'
    mailnum = 'MAILNUM'
    mail1 = 'MAIL1'
    mail2 = 'MAIL2'
    skype = 'SKYPE'
    birthdate = 'BIRTHDATE'
    country = 'COUNTRY'
    addrnum = 'ADDRNUM'
    addrline1 = 'ADDRLINE1'
    addrline2 = 'ADDRLINE2'


# Own states
class Waiting(State):
    def next(self, received):
        if not self.transitions:
            self.transitions = {Message.helo.value: ExasolFsm.helo}

        return super().next(received)

    def run(self, conn=None, data=None):
        self.logger.info(f'In state {self.name}; data {data}')


class Hello(State):
    def next(self, received):
        if not self.transitions:
            self.transitions = {
                Message.pow.value: ExasolFsm.pow,
                Message.error.value: ExasolFsm.error,
}

        return super().next(received)

    def run(self, conn=None, data=None):
        self.logger.info(f'In state {self.name}; data {data}')
        conn.send('EHLO\n'.encode())
        self.logger.info('Received HELO, replied EHLO')

class Pow(State):
    def next(self, received):
        if not self.transitions:
            self.transitions = {
                Message.error.value: ExasolFsm.error,
                Message.name.value: ExasolFsm.send_name,
                Message.mailnum.value: ExasolFsm.send_mailnum,
                Message.mail1.value: ExasolFsm.send_mail1,
                Message.mail2.value: ExasolFsm.send_mail2,
                Message.skype.value: ExasolFsm.send_skype,
                Message.birthdate.value: ExasolFsm.send_birthdate,
                Message.country.value: ExasolFsm.send_country,
                Message.addrnum.value: ExasolFsm.send_addrnum,
                Message.addrline1.value: ExasolFsm.send_addrline1,
                Message.addrline2.value: ExasolFsm.send_addrline2
            }

        return super().next(received)

    def run(self, conn=None, data=None):
        self.logger.info(f'In state {self.name}; data {data}')
        global authdata
        authdata, difficulty = data[0], int(data[1])
        start = time()
        self.logger.info(f'started mining @{strftime("%H:%M:%S", localtime(start))}')

        nonce, suffix = mine(authdata, difficulty)
        self.logger.info(f'Found nonce {nonce}, suffix {suffix}, took {time() - start}')
        conn.send(suffix + NEW_LINE_ENC)


class End(State):
    def next(self, received):
        if not self.transitions:
            self.transitions = {Message.end.value: ExasolFsm.waiting}

        return super().next(received)

    def run(self, conn=None, data=None):
        self.logger.info(f'In state {self.name}; data {data}')
        # if you get this command, then your data was submitted
        conn.send('OK\n'.encode())


class Error(State):
    def next(self, received):
        if not self.transitions:
            self.transitions = {Message.error.value: ExasolFsm.waiting}

        return super().next(received)

    def run(self, conn=None, data=None):
        self.logger.info(f'In state {self.name}; data {data}')

class SendData(State):
    def __init__(self, command):
        self.command = command
        self.data = {
            'name': b'Carlos Ghabrous Larrea',
            'mailnum': b'1',  
            'mail1': b'carlos.ghabrous@gmail.com',
            'mail2': b'',
            'skype': b'carlosghabrous',
            'birthdate': b'04.02.1980',
            'country': b'Switzerland',
            'addrnum': b'2',
            'addrline1': b'Rue du Beulet,8',
            'addrline2': b'1203 Geneva'           
        }

        super().__init__()

    def next(self, received):
        if not self.transitions:
            self.transitions = {
                Message.name.value: ExasolFsm.send_name,
                Message.mailnum.value: ExasolFsm.send_mailnum,
                Message.mail1.value: ExasolFsm.send_mail1,
                Message.mail2.value: ExasolFsm.send_mail2,
                Message.skype.value: ExasolFsm.send_skype,
                Message.birthdate.value: ExasolFsm.send_birthdate,
                Message.country.value: ExasolFsm.send_country,
                Message.addrnum.value: ExasolFsm.send_addrnum,
                Message.addrline1.value: ExasolFsm.send_addrline1,
                Message.addrline2.value: ExasolFsm.send_addrline2,
                Message.error.value: ExasolFsm.error,
                Message.end.value: ExasolFsm.end
                }

        return super().next(received)

    def run(self, conn=None, data=None):
        self.logger.info(f'In state {self.name}; data {data}')
        payload = SHA(authdata + data[0]).digest()
        conn.send(payload)



# Own FSM
class ExasolFsm(FiniteStateMachine):
    def __init__(self, conn, authdata):
        super().__init__(ExasolFsm.waiting, conn)
        self.authdata = ''
        self.logger = logging.getLogger('exasol.statemachine' + __name__ + type(self).__name__)


ExasolFsm.waiting = Waiting()
ExasolFsm.helo = Hello()
ExasolFsm.pow  = Pow()
ExasolFsm.error = Error()
ExasolFsm.end = End()
ExasolFsm.send_name = SendData('name')
ExasolFsm.send_mailnum = SendData('mailnum')
ExasolFsm.send_mail1 = SendData('mail1')
ExasolFsm.send_mail2 = SendData('mail2')
ExasolFsm.send_skype = SendData('skype')
ExasolFsm.send_birthdate = SendData('birthdate')
ExasolFsm.send_country = SendData('country')
ExasolFsm.send_addrnum = SendData('addrnum')
ExasolFsm.send_addrline1 = SendData('addrline1')
ExasolFsm.send_addrline2 = SendData('addrline2')
