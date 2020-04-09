import re
import argparse
import logging
import sys
import re
from shutil import copyfile
from datetime import datetime


logger = logging.getLogger(__name__)


def get_args(args):
    """
    Parse command line arguments

    Returns:

    """
    parser = argparse.ArgumentParser(
        description='This script can be used to update variable.tf.')

    parser = argparse.ArgumentParser(
        description='This script can be used to update variable.tf.')
    parser.add_argument('-c', '--config_file', type=str,
                        help='Please provide the config JSON with a list of '
                             'update', required=False)
    parser.add_argument('-a', '--action', type=str,
                        help='Options actions are update/list',
                        choices=['update', 'list'], required=True)
    parser.add_argument('-in', '--in_file', type=str,
                        help='input variable.tf file', required=True)
    parser.add_argument('-out', '--output_file', type=str,
                        help='output variable.tf file', required=False)

    parser.add_argument(
        '-v',
        '--verbose',
        dest='loglevel',
        help='set loglevel to INFO',
        action='store_const',
        const=logging.INFO
    )

    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest='loglevel',
        help='set loglevel to DEBUG',
        action='store_const',
        const=logging.DEBUG
    )

    args = parser.parse_args(args)
    return args


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = '[%(asctime)s] %(levelname)s:%(name)s:  %(message)s'
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt='%Y-%m-%d %H:%M:%S')




def read_variable_file(filepath):
    data = {}
    var = []
    excluded_list = ['', '{', '}']
    with open(filepath) as fp:
        line = fp.readline()
        variable = ''
        i = 0
        while line:
            if line.startswith( 'variable' ):
                if i != 0:
                    data[variable] = var
                    var = []
                name = re.findall('"([^"]*)"', line)
                variable = name[0]
                data[variable]=""
            else:
               l = line.strip()
               if l not in excluded_list and not(l.startswith('#')):
                   var.append(line.strip())
       
            line = fp.readline()
            i +=1
    
        data[variable] = var
        return data


def find_missing_vars(data):
    mandatories = []
    for varible in data.keys():
        values = data[varible]
        d = 0
        for val in values:
            if val.startswith('default'):
                d = 1
                t = [x.strip() for x in val.split('=')]
                if t[1] == '""':
                    mandatories.append(varible)
            #print(t)
        if d ==0:
            mandatories.append(varible)
    return mandatories


d_variables = {'dataproc_workers_machine_type': '20', 'host_project_id': 'data-science-activator'}
def update_variables(d_varibales, d_updates):
    data_updated = {}
    for varible in data.keys():
        if varible in d_variables.keys():
            d = 0
            values = data[varible]
            vals = []
            for val in values:
                if val.startswith('default'):
                    d = 1
                    if d_variables[varible].isdigit():
                        elem = 'default = {}'.format(l_updates[varible])
                    else:
                        elem = 'default = "{}"'.format(d_variables[varible])
                    vals.append(elem)

                else:
                    vals.append(val)
                
            if d ==0:
                if d_variables[varible].isdigit():
                    elem = 'default = {}'.format(d_variables[varible])
                else:
                    elem = 'default = "{}"'.format(d_variables[varible])
                vals.append(elem)
            data_updated[varible] = vals
        else:
            data_updated[varible]= data[varible]
    return data_updated



def update_variable_file(d_updated_varibales, variable_file):
    l_variables = []
    lines = ""
    for varible in d_updated_varibales.keys():
        l = 'variable "{}" {}\n'.format(varible, '{')
        vl = ""
        for val in d_updated_varibales[varible]:
            vl  = vl +"{}\n".format(val)
        l = 'variable "{}" {}\n{}{}\n'.format(varible, '{', vl, '}')
        lines = "{}\n{}".format(lines,l)
    print(lines)


def main(args):
    """

    Args:
        args:

    Returns:

    """
    args = get_args(args)
    loglevel = args.loglevel
    if args.loglevel is None:
        loglevel = logging.INFO
    setup_logging(loglevel)
    logging.info(args)

    input_file = args.in_file
    logging.info("Input variable.tf file is: {}".format(input_file))

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    backup_file = input_file + "-"+dt_string+".backup"
    copyfile(input_file, backup_file)
    logging.info("Input file {} has been backed up to {}".format(
        input_file, backup_file))




def run():

    main(sys.argv[1:])


if __name__ == '__main__':
    run()


