import re
import argparse
import logging
import sys
import re
from shutil import copyfile
from datetime import datetime
import json


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
                        help='output variable.tf file', default= "",
                        required=False)

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
                    if variable != '':
                        data[variable] = var
                    var = []
                name = re.findall('"([^"]*)"', line)
                variable = name[0]
                if variable != '':
                    data[variable]=""
            else:
               l = line.strip()
               if l not in excluded_list and not(l.startswith('#')):
                   var.append(line.strip())
       
            line = fp.readline()
            i +=1
        if variable != '':
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


def update_variables(d_varibales, d_updates):
    data_updated = {}
    for varible in d_varibales.keys():
        if varible in d_updates.keys():
            d = 0
            values = d_varibales[varible]
            vals = []
            for val in values:
                if val.startswith('default'):
                    d = 1
                    if d_updates[varible].isdigit():
                        elem = 'default = {}'.format(d_updates[varible])
                    else:
                        elem = 'default = "{}"'.format(d_updates[varible])
                    vals.append(elem)

                else:
                    vals.append(val)
                
            if d ==0:
                if d_updates[varible].isdigit():
                    elem = 'default = {}'.format(d_updates[varible])
                else:
                    elem = 'default = "{}"'.format(d_updates[varible])
                vals.append(elem)
            data_updated[varible] = vals
        else:
            data_updated[varible]= d_varibales[varible]
    return data_updated



def update_variable_file(d_updated_variables, variable_file):
    lines = ""
    for variable in d_updated_variables.keys():
        l = 'variable "{}" {}\n'.format(variable, '{')
        vl = ""
        for val in d_updated_variables[variable]:
            vl  =vl +"{}\n".format('  '+val)
        l = 'variable "{}" {}\n{}{}\n'.format(variable, '{', vl, '}')
        lines = "{}\n{}".format(lines,l)

    with open(variable_file, "w") as f:
        f.write(lines)


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

    if args.action == 'list':
        data = read_variable_file(input_file)
        missings = find_missing_vars(data)
        logging.info("Variables that needs to be updated are:")
        logging.info(missings)
        update_file=''
        if args.output_file == "":
            update_file = 'update_file.txt'
        else:
            update_file = args.output_file

        with open(update_file, "w") as f:
            for miss in missings:
                f.write(miss+"\n")

    elif args.action == 'update':
        logging.info("Updating variable file has been started.")
        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
        backup_file = input_file + "-" + dt_string + ".backup"
        copyfile(input_file, backup_file)
        logging.info("Input file {} has been backed up to {}".format(
            input_file, backup_file))

        replacement_file = args.config_file
        d_variables = read_variable_file(input_file)

        with open(replacement_file) as json_file:
            d_updates = json.load(json_file)

        d_updated_variables = update_variables(d_variables, d_updates)
        if args.output_file == "":
            update_variable_file(d_updated_variables, input_file)
            logging.info("Updated variable file has been written into {"
                         "}".format(input_file))
        else:
            update_variable_file(d_updated_variables, args.output_file)
            logging.info("Updated variable file has been written into {"
                         "}".format(args.output_file))


def run():
    main(sys.argv[1:])


if __name__ == '__main__':
    run()


