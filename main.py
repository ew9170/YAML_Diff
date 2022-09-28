import argparse
import pprint

import yaml
import deepdiff as dd


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_1', nargs='?')
    parser.add_argument('--file_2', nargs='?')
    parser.add_argument('--file', type=str, metavar='FILENAME', help='If provided, output is written to provided file')
    parser.add_argument('--server', type=int, metavar='PORT', help='Run in server mode, provide a port to take files')
    args = parser.parse_args()
    return args


def verify_args(args):
    if args.file_1 is not None and args.file_2 is not None:  # both files are provided
        try:
            f1 = open(args.file_1)
            f2 = open(args.file_2)
            return f1, f2
        except FileNotFoundError as e:
            return None
    else:  # only one of f1 or f2 is provided
        return None


def yaml_text_to_data(file):
    if file is None:
        return None
    try:
        yaml_object = yaml.safe_load(file)
        return yaml_object
    except yaml.YAMLError as e:
        return None


def diffing(yaml_objects):
    pprint.pp(dd.DeepDiff(yaml_objects[0], yaml_objects[1]), indent=2)


def main():
    args = get_arguments()
    files = verify_args(args)
    yaml_objects = []
    if files is not None:
        for file in files:
            yaml_objects.append(yaml_text_to_data(file))
    diffing(yaml_objects)


if __name__ == '__main__':
    main()
