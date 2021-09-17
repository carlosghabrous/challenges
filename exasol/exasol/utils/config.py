from pathlib import Path
from typing import List

def _is_ip_address_v4_ok(ip_address: str) -> str:
    '''Validates a IPv4 addresss

    Args:
        ip_address (str): Input internet addresss

    Returns:
        str: Error message if any
    '''

    IP_V4_ADDRESS_FIELD_NUM = 4
    msg = list()

    ip_list = ip_address.split('.')

    len_ip = len(ip_list)
    if len_ip != IP_V4_ADDRESS_FIELD_NUM:
        msg.append(f'IP address v4 contains only {len_ip} fields')

    try:
        ip_int_list = list(map(int, ip_list))

    except ValueError:
        msg.append('IP address malformed: could not convert fields to integers')

    
    ip_int_list = list(filter(lambda field: 0 < field < 255, ip_int_list))
    if len(ip_int_list) != IP_V4_ADDRESS_FIELD_NUM:
        msg.append('IP address malformed: field(s) values out of range')

    return '\n'.join(msg) 

def _is_port_list_ok(port_list: List) -> str:
    '''Validates ports in a list

    Args:
        port_list (List): List of ports

    Returns:
        str: Error message if any
    '''
    msg = list()

    try:
        port_list_int = list(map(int, port_list))

    except ValueError:
        msg.append('Port(s) malformed: could not convert to integer(s)')
        port_list_int = list()

    valid_ports = list(filter(lambda port:1024 < port < 65535, port_list_int))

    if len(port_list_int) != len(valid_ports):
        msg.append('Port(s) malformed: field(s) values out of range')

    return '\n'.join(msg) 

def _is_path_ok(some_path: str) -> str:
    '''Validates a path

    Args:
        some_path (str): The provided path

    Returns:
        str: Error message if any
    '''
    msg = ''
    file_path = Path(__file__).parent.parent.parent / some_path

    if not Path(file_path).exists(): 
        msg = f'Path {file_path} does not exist'

    return msg


# Maps the object to be validated to its validation function
_snitchers = {'server': _is_ip_address_v4_ok,
                'ports': _is_port_list_ok, 
                'certificate': _is_path_ok,
                'private_key': _is_path_ok}

def validate(configuration: dict) -> dict:
    '''Validates YAML configuration file

    Args:
        configuration (dict): Dictionary comming from the YAML configuration file

    Raises:
        KeyError: Raised if missing parameter in configuration file
        ValueError: Raised if parameters are malformed in the configuration file

    Returns:
        dict: [description]
    '''
    for key, snitcher in _snitchers.items():
        if not configuration.get(key, None):
            raise KeyError(f'"{key}" parameter missing from configuration file')

        msg = snitcher(configuration[key])
        if msg:
            raise ValueError(msg)

    return configuration