import argparse
import pprint
import sys
import yaml
import deepdiff as dd


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_1', nargs='?', help="If provided, both files are necessary")
    parser.add_argument('file_2', nargs='?', help="Providing files does nothing if server mode is set")
    parser.add_argument('--file', type=str, metavar='FILENAME', help='If provided, output is written to provided file')
    parser.add_argument('--server', type=int, metavar='PORT',
                        help='(NOT IMPLEMENTED) Run in server mode, provide a port to take files')
    args = parser.parse_args()

    if args.server is not None:
        print("Server mode is not implemented")
        exit(0)

    if args.file_1 is None or args.file_2 is None:
        parser.print_help()
        exit(0)

    return args


# helper function that verifies user provided arguments
def verify_args(args):
    if args.file_1 is not None and args.file_2 is not None:  # both files are provided
        try:
            f1 = open(args.file_1)
            f2 = open(args.file_2)
            return f1, f2
        except FileNotFoundError as e:
            print(e)
            return None
    else: # should never happen
        print("Insufficient files provided", file=sys.stderr)
        exit(-1)


# converts a yaml file into a python dictionary
def yaml_text_to_data(file):
    if file is None:
        return None
    try:
        yaml_object = yaml.safe_load(file)
        return yaml_object
    except yaml.YAMLError as e:
        return None


def dict_str_to_dot_str(dict_str):
    return_string = dict_str
    if dict_str is not None and len(dict_str) > 0:
        return_string = return_string.replace("['", ".").replace("']", "").replace("root", "")
    return str(return_string)


def diffing(yaml_objects):
    diffs = dd.DeepDiff(yaml_objects[0], yaml_objects[1], verbose_level=2)
    pprint.pp(diffs)
    diff_str_array = []
    # diffs contains a mapping from the string
    # 'values_changed' to a dictionary containing keys that have differing values

    if 'values_changed' in diffs:
        for changed_value in diffs['values_changed']:
            diff_string = ""
            diff_string += dict_str_to_dot_str(changed_value) + ": " \
                           + str(diffs['values_changed'][changed_value]['new_value'])
            diff_str_array.append(diff_string)
    if 'dictionary_item_added' in diffs:
        for added_value in diffs['dictionary_item_added']:
            diff_string = ""
            diff_string += dict_str_to_dot_str(added_value) + ": " + str(diffs['dictionary_item_added'][added_value])
            diff_str_array.append(diff_string)
    if 'dictionary_item_removed' in diffs:
        for deleted_value in diffs['dictionary_item_removed']:
            diff_string = ""
            diff_string += dict_str_to_dot_str(deleted_value) + ": " + "None"
            diff_str_array.append(diff_string)
    if 'iterable_item_added' in diffs:
        for iterable_added in diffs['iterable_item_added']:
            diff_string = ""
            diff_string += dict_str_to_dot_str(iterable_added) + ": " + str(
                diffs['iterable_item_added'][iterable_added])
            diff_str_array.append(diff_string)
    if 'iterable_item_removed' in diffs:
        for iterable_removed in diffs['iterable_item_removed']:
            diff_string = ""
            diff_string += dict_str_to_dot_str(iterable_removed) + ": " + "None"
            diff_str_array.append(diff_string)
    if 'type_changes' in diffs:
        for item_changed in diffs['type_changes']:
            diff_string = ""
            diff_string += dict_str_to_dot_str(item_changed) + ": " + str(
                diffs['type_changes'][item_changed]['new_value'])
            diff_str_array.append(diff_string)

    return diff_str_array


def output(diff_list, args):
    if args.server is None:
        for diff in diff_list:
            print(diff)


def server():
    print("Server mode not implemented")
    exit(0)


def main():
    args = get_arguments()
    files = verify_args(args)
    yaml_objects = []
    if args.server is not None:
        server()
    else:
        if files is not None:
            for file in files:
                yaml_objects.append(yaml_text_to_data(file))
            diff_list = diffing(yaml_objects)
            output(diff_list, args)


if __name__ == '__main__':
    main()
