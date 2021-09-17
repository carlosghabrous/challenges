import logging
import re
from collections import namedtuple

FILE_NAME_REGEX = re.compile(r"(?:dend-)?([a-zA-Z0-9_-]*)_(?:axon-)?([a-zA-Z0-9_-]*)(?:-_Scale)?([a-zA-Z0-9_.]*)(?:-_Clone_)?([0-9]+)")

named_tuple_fields = ('dend', 'axon', 'scale', 'clone')
FileInfo = namedtuple('FileInfo', named_tuple_fields, defaults=(None,) * len(named_tuple_fields))

logger = logging.getLogger(__name__)

test_file_list = [
    'dend-Fluo42_right_axon-Fluo42_right_-_Scale_x1.000_y1.050_z1.000',
    'dend-tkb071119a1_ch8_cc2_n_db_100x_1_axon-tkb061101a2_ch5_ct_h_zk_60x_1_-_Scale_x1.000_y1.050_z1.000_-_Clone_0',
    'dend-C180298A-P2_axon-C190898A-P2_-_Scale_x1.000_y1.025_z1.000_-_Clone_11',
    'C280999A-I4_-_Scale_x1.000_y1.050_z1.000_-_Clone_10',
    'C280999A-I4_-_Scale_x1.000_y1.050_z1.000_-_Clone_10',
    'dend-Fluo12_right_axon-Fluo58_left_-_Scale_x1.000_y0.950_z1.000_-_Clone_14',
    'dend-C270999B-P2_axon-C270999B-P2_-_Scale_x1.000_y0.950_z1.000_-_Clone_23',
    'dend-C200897C-P4_axon-C310897B-P3_-_Scale_x1.000_y1.025_z1.000_-_Clone_11',
    'C080300B2_-_Scale_x1.000_y1.050_z1.000_-_Clone_21',
    'C080300B2_-_Scale_x1.000_y1.050_z1.000_-_Clone_21',
    'dend-C140600C-P3_axon-C310897A-P4_-_Scale_x1.000_y1.025_z1.000_-_Clone_8',
    'C050896A-I_-_Scale_x1.000_y1.050_z1.000_-_Clone_1',
    'C050896A-I_-_Scale_x1.000_y1.050_z1.000_-_Clone_1',
    'C050896A-I_-_Scale_x1.000_y1.050_z1.000_-_Clone_1',
    'dend-C060202A6_axon-C060109A1_-_Scale_x1.000_y0.950_z1.000_-_Clone_1',
    'dend-C260897C-P4_axon-C260897C-P2_-_Clone_12',
    'dend-C260897C-P4_axon-C260897C-P2_-_Clone_12',
    'dend-ch150801A1_axon-rp100125_C1_idB_-_Clone_1',
    'dend-tkb060123a1_ch4_cc1_b_hw_60x_1_axon-tkb060508a1_ch3_cc1_h_zk_60x_1_-_Clone_1',
    'dend-C170898A-P4_axon-C271097A-P2_-_Scale_x1.000_y1.025_z1.000_-_Clone_2',
    'dend-tkb061126a2_ch1_cc1_h_zk_60x_1_axon-tkb060508a1_ch3_cc1_h_zk_60x_1_-_Scale_x1.000_y1.050_z1.000_-_Clone_5',
    'dend-C260199A-P2_axon-C310897B-P3_-_Scale_x1.000_y0.975_z1.000_-_Clone_7',
    'dend-C270999B-P2_axon-Fluo18_upper_-_Clone_8',
    'dend-C120398A-P2_axon-C120398A-P3_-_Scale_x1.000_y0.950_z1.000_-_Clone_80',
    'dend-Fluo18_upper_axon-Fluo2_left_-_Scale_x1.000_y0.950_z1.000_-_Clone_23',
    'dend-tkb071114a2_ch2_cc2_n_db_100x_1_axon-tkb061101a2_ch5_ct_h_zk_60x_1_-_Clone_4',
    'dend-tkb060523a2_ch5_cc2_n_nb_60x_1_axon-tkb061101a1_ch4_cc2_h_zk_60x_1_-_Clone_3',
    'dend-C271097A-P1_axon-C271097A-P1_-_Clone_9',
    'dend-Fluo2_right_axon-Fluo6_right_-_Scale_x1.000_y1.025_z1.000_-_Clone_34',
    'dend-C271097A-P3_axon-C180997A-P3_-_Scale_x1.000_y1.025_z1.000_-_Clone_4',
    'dend-C031000B-P3_axon-C240797B-P1_-_Scale_x1.000_y1.050_z1.000_-_Clone_12',
    'dend-C031000B-P3_axon-C240797B-P1_-_Scale_x1.000_y1.050_z1.000_-_Clone_12',
    'dend-tkb061101a1_ch4_cc2_h_zk_60x_1_axon-tkb061101a2_ch6_cc2_h_zk_60x_1_-_Scale_x1.000_y1.050_z1.000_-_Clone_2',
]


def extract_file_info(file_name_list):
    '''Extracts relevant information from each of the file names in file_name_list.

    Based on the file list provided, I am making the assumption the four sections of the file name can be optional.
    I tried to come up with a regular expression that would match them all, but it needs some reworking and the current solution
    does not work as expected. 

    Alternatives: 
    1. Iterate over the regular expression FILE_NAME_REGEX to get it right
    2. Have a regular expression for possible file name. The code below should then look like:
    if re.match(FIRST_REGEX, file_name):
        do_something()

    elif re.match(SECOND_REGEX, file_name):
        do_something_else()

    3. Scan the string and look for the following keywords: 'dend', 'axon', 'Scale', 'Clone'. Everything in between is relevant information. 


    '''
    result = dict()

    for file_name in file_name_list:
        match = re.match(FILE_NAME_REGEX, file_name)
        if match:
            dend, axon, scale, clone = match.group(1), match.group(2), match.group(3), match.group(4)
            file_info = FileInfo(dend, axon, scale, clone)
            result[file_name] = file_info

        else:
            logger.error(f'File {file_name} has been wrongly named!')

    return result


class ImproperFilenameError(Exception):
    pass

if __name__ == '__main__':
    print(extract_file_info(test_file_list))