#!/usr/bin/python3

'''Exasol challenge

Entry point to Exasol's challenge assingment. 
After configuring the parser to deal with the command line arguemtns, 
parses and validates a YAML configuration file, sets up logger objects and starts the TLS client. 
''' 

import argparse
import logging
import yaml

from logging import handlers
from pathlib import Path

import tls.client as client
from utils import config


def _read_config_file(config_file: str) -> dict:
    '''Reads a yaml config file

    Args:
        config_file (string): a YAML config file
    '''

    # Let it fail purposely in case there is no config file or it is malformed
    with open(config_file) as cfh: 
        config_params = yaml.load(cfh, Loader=yaml.FullLoader)
        return config_params


def _configure_logger(verbosity: int, log_file_path: str) -> None:
    '''Configures two logger handlers, file and stream, according to input parameteres

    Args:
        verbosity (integer): verbosity level
        log_file_path (string): Path to log file storage
    '''

    LOG_FILES_NUMBER = 20
    default_severity = (verbosity == True) and logging.DEBUG or logging.INFO

    logger = logging.getLogger("exasol")
    logger.setLevel(default_severity)

    LOG_FORMAT = "[%(asctime)s] [%(levelname)7s](%(module)11s): %(message)s"
    formatter = logging.Formatter(LOG_FORMAT)
    
    fh = handlers.RotatingFileHandler(log_file_path, maxBytes=1000000, backupCount=LOG_FILES_NUMBER)
    fh.setLevel(default_severity)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(default_severity)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    logger.info('Loggers correctly configured')

def _setup(c: str, verbosity: int):
    valid_config = config.validate(_read_config_file(c))
    _configure_logger(verbosity, valid_config['log_file_path'])
    client.start(valid_config['server'], valid_config['ports'], valid_config['certificate'], valid_config['private_key'])


def _cli() -> None:
    '''Configures the CLI parser; dispatches the arguments to the function _setup


    Returns:
        dict: argparse dictionary with command line input
    '''

    default_config_file_path = Path(__file__).parent.parent / 'data' / 'config.yaml'

    parser = argparse.ArgumentParser(prog=__file__)

    parser.set_defaults(handler=_setup)
    parser.add_argument('-v', '--verbosity', default=0, help='Increases the output verbosity', action='count')
    parser.add_argument('-c', default=default_config_file_path, help='Path to config file', metavar='CONFIG-FILE')

    args = parser.parse_args().__dict__.copy()
    return args 


def main():
    '''Entry point
    '''
    args = _cli()
    args.pop('handler')(**args)

if __name__ == '__main__':
    main()
