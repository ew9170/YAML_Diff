import unittest
from yaml_diff import *


pvc_kind_str = """
apiVersion: v1
kind: PersistentVolumeClaim
to_be_removed: True
testing_list:
  - item_old
"""

pv_kind_str = """
apiVersion: v1
kind: PersistentVolume
added_bool: True
testing_list:
  - item_new
"""


class YAMLBehavioralTests(unittest.TestCase):
    """
    Story:
    As a user of this library,
    I want to pass YAML files into yaml_diff.py and have it output
    the new value of an updated/added/removed YAML key-value pair
    """
    def test_changed_values(self):
        yaml_objects = [yaml_text_to_data(pvc_kind_str), yaml_text_to_data(pv_kind_str)]
        diff_list = diffing(yaml_objects)
        self.assertTrue(".kind: PersistentVolume" in diff_list)
        self.assertTrue(".to_be_removed: None" in diff_list)
        self.assertTrue(".added_bool: True" in diff_list)
        self.assertTrue(".testing_list[0]: item_new" in diff_list)


if __name__ == '__main__':
    unittest.main()
