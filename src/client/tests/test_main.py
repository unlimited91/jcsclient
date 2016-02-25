import unittest

from client import common

class MyTestCase(unittest.TestCase):
    def test_item_removal_from_dict(self):
        # A normal dict should not be transformed
        in_dict = {'a':'b'}
        expected_resp = {'a':'b'}
        actual_resp = common._remove_item_keys(in_dict)
        self.assertEqual(expected_resp, actual_resp)

        # A dictionary with 'item' key and a dictionary as value should be
        # replaced with a list containing that dictionary
        in_dict = {'a': {'item': {'b': 'c'}}}
        expected_resp = {'a': [{'b': 'c'}]}
        actual_resp = common._remove_item_keys(in_dict)
        self.assertEqual(expected_resp, actual_resp)

        # A dictionary with 'item' key and a list of dictionaries as value should be
        # replaced with the value which was list of dictionaries
        in_dict = {'a': {'item': [{'b': 'c'}, {'d': 'e'}]}}
        expected_resp = {'a': [{'b': 'c'}, {'d': 'e'}]}
        actual_resp = common._remove_item_keys(in_dict)
        self.assertEqual(expected_resp, actual_resp)

        # A dictionary with 'item' as a key shouldn't have any more keys
        in_dict = {'a': {'item': {'b': 'c'}, 'anotherkey': 'd'}}
        self.assertRaises(Exception, common._remove_item_keys, in_dict)

        # 'item' can't be a first-level key
        in_dict = {'item': {'a': 'b'}}
        self.assertRaises(Exception, common._remove_item_keys, in_dict)

        # For 'item' key, value can't be anything which is not a dict or a list
        in_dict = {'a': {'item': 'plainstringvalue'}}
        self.assertRaises(Exception, common._remove_item_keys, in_dict)

        # Anything other than a dictionary shouldn't be processed
        in_dict = 'notreallyadict'
        self.assertRaises(Exception, common._remove_item_keys, in_dict)

        # Test recursion
        in_dict = {'a': {'b': {'item': {'c': {'item': {'d': 'e'}}}}}}
        expected_resp = {'a': {'b': [{'c': [{'d': 'e'}]}]}}
        actual_resp = common._remove_item_keys(in_dict)
        self.assertEqual(expected_resp, actual_resp)

        # For 'item' key, dictionary value can't have 'item' key again
        in_dict = {'a': {'b': {'item': {'item': {'d': 'e'}}}}}
        self.assertRaises(Exception, common._remove_item_keys, in_dict)
