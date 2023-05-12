import unittest
from ed_utils.decorators import number

from double_key_table import DoubleKeyTable

class TestDoubleHash(unittest.TestCase):

    @number("3.1")
    def test_example(self):
        """
        See spec sheet image for clarification.
        """
        # Disable resizing / rehashing.
        dt = DoubleKeyTable(sizes=[12], internal_sizes=[5])
        dt.hash1 = lambda k: ord(k[0]) % 12
        dt.hash2 = lambda k, sub_table: ord(k[-1]) % 5

        dt["Tim", "Jen"] = 1
        dt["Amy", "Ben"] = 2
        dt["May", "Ben"] = 3
        dt["Ivy", "Jen"] = 4
        dt["May", "Tom"] = 5
        dt["Tim", "Bob"] = 6
        self.assertRaises(KeyError, lambda: dt._linear_probe("May", "Jim", False))
        self.assertEqual(dt._linear_probe("May", "Jim", True), (6, 1))
        dt["May", "Jim"] = 7 # Linear probing on internal table
        self.assertEqual(dt._linear_probe("May", "Jim", False), (6, 1))
        self.assertRaises(KeyError, lambda: dt._linear_probe("Het", "Liz", False))
        self.assertEqual(dt._linear_probe("Het", "Liz", True), (2, 2))
        dt["Het", "Liz"] = 8 # Linear probing on external table
        self.assertEqual(dt._linear_probe("Het", "Liz", False), (2, 2))

    @number("3.2")
    def test_delete(self):
        # Disable resizing / rehashing.
        dt = DoubleKeyTable(sizes=[12], internal_sizes=[5])
        dt.hash1 = lambda k: ord(k[0]) % 12
        dt.hash2 = lambda k, sub_table: ord(k[-1]) % 5

        dt["Tim", "Jen"] = 1
        dt["Amy", "Ben"] = 2
        dt["Tim", "Kat"] = 3

        self.assertEqual(dt._linear_probe("Tim", "Kat", False), (0, 1))

        del dt["Tim", "Jen"]
        # We can't do this as it would create the table.
        # self.assertEqual(dt._linear_probe("Het", "Bob", True), (1, 3))
        del dt["Tim", "Kat"]
        # Deleting again should make space for Het.
        dt["Het", "Bob"] = 4
        self.assertEqual(dt._linear_probe("Het", "Bob", False), (0, 3))

        self.assertRaises(KeyError, lambda: dt._linear_probe("Tim", "Jen", False))
        dt["Tim", "Kat"] = 5
        self.assertEqual(dt._linear_probe("Tim", "Kat", False), (1, 1))

    @number("3.3")
    def test_resize(self):
        dt = DoubleKeyTable(sizes=[3, 5], internal_sizes=[3, 5])
        dt.hash1 = lambda k: ord(k[0]) % dt.table_size
        dt.hash2 = lambda k, sub_table: ord(k[-1]) % sub_table.table_size

        dt["Tim", "Bob"] = 1
        # No resizing yet.
        self.assertEqual(dt.table_size, 3)
        self.assertEqual(dt._linear_probe("Tim", "Bob", False), (0, 2))
        dt["Tim", "Jen"] = 2
        # Internal resize.
        self.assertEqual(dt.table_size, 3)
        self.assertEqual(dt._linear_probe("Tim", "Bob", False), (0, 3))

        # External resize
        dt["Pip", "Bob"] = 4
        self.assertEqual(dt.table_size, 5)
        self.assertEqual(dt._linear_probe("Tim", "Bob", False), (4, 3))
        self.assertEqual(dt._linear_probe("Pip", "Bob", False), (0, 2))

    @number("3.4")
    def test_keys_values(self):
        # Disable resizing / rehashing.
        dt = DoubleKeyTable(sizes=[5], internal_sizes=[5])
        dt.hash1 = lambda k: ord(k[0]) % 5
        dt.hash2 = lambda k, sub_table: ord(k[-1]) % 5


        dt["Tim", "Jen"] = 1
        dt["Amy", "Ben"] = 2
        dt["May", "Ben"] = 3
        dt["Ivy", "Jen"] = 4
        dt["May", "Tom"] = 5
        dt["Tim", "Bob"] = 6
        dt["May", "Jim"] = 7
        dt["Het", "Liz"] = 8
 

        self.assertEqual(set(dt.keys()), {"Tim", "Amy", "May", "Ivy", "Het"})
        self.assertEqual(set(dt.keys("May")), {"Ben", "Tom", "Jim"})

        self.assertEqual(set(dt.values()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(set(dt.values("Tim")), {1, 6})

    @number("3.5")
    def test_iters(self):
        # Test that these are actually iterators,
        # and so changing the underlying data structure changes the next value.
        dt = DoubleKeyTable(sizes=[5], internal_sizes=[5])
        dt.hash1 = lambda k: ord(k[0]) % 5
        dt.hash2 = lambda k, sub_table: ord(k[-1]) % 5
        """ dt["May", "Jim"] = 1
        dt["Kim", "Tim"] = 2 """

        dt["Tim", "Jen"] = 1
        dt["Amy", "Ben"] = 2
        dt["Tom", "Ben"] = 3
        dt["Ivy", "Jen"] = 4
        dt["Tom", "Tom"] = 5
        dt["Tim", "Bob"] = 6
        dt["Tom", "Jim"] = 7
        dt["Het", "Liz"] = 8

        # print(str(dt))
        # print ("all the outer are " , dt.keys())
        key_iterator = dt.iter_keys()
        value_iterator = dt.iter_values()

        key = next(key_iterator)
        #print("outer keys are " , key)
        #self.assertIn(key, ["May", "Kim"])

        self.assertIn(key, ["Tim", "Amy", "Tom", "Ivy", "Het"])

        key = next(key_iterator)
        #print ("outer keys are " , key)
        self.assertIn(key, ["Tim", "Amy", "Tom", "Ivy", "Het"])

        key = next(key_iterator)
        #print ("outer keys are " , key)
        self.assertIn(key, ["Tim", "Amy", "Tom", "Ivy", "Het"])

        #print ("all the keys of Tom are " , dt.keys("Tom"))


        key_iterator1 = dt.iter_keys("Tom")
        key1 = next(key_iterator1)
        #print ("key with Tom is " , key1)
        self.assertIn(key1, ["Ben", "Tom", "Jim"])

        key1 = next(key_iterator1)
        #print ("key with Tom is " , key1)
        self.assertIn(key1, ["Ben", "Tom", "Jim"])

        key_iterator2 = dt.iter_keys("Tim")

        #print ("all the keys of Tim are " , dt.keys("Tim"))


        key2 = next(key_iterator2)
        #print ("key with Tim is " ,key2)
        self.assertIn(key2, ["Bob","Jen"])

        key2 = next(key_iterator2)
        #print ("key with Tim is " , key2)
        self.assertIn(key2, ["Bob","Jen"])



        # print("all the values are " , dt.values())
        # print("all Tom values are ", dt.values("Tom"))
        # print("all Tim values are ", dt.values("Tim"))

        value = next(value_iterator)
        #print("all value after next is " , value)
        self.assertIn(value, [1, 2, 3, 4, 5, 6, 7, 8])

        value = next(value_iterator)
        #print("all value after next is " , value)
        self.assertIn(value, [1, 2, 3, 4, 5, 6, 7, 8])

        value_iterator1 = dt.iter_values("Tom")
        value1 = next(value_iterator1)
        #print ("after next values with Tom are " , value1)
        self.assertIn(value1, [3, 5, 7])

        value1 = next(value_iterator1)
        #print ("after next values with Tom are " , value1)
        self.assertIn(value1, [3, 5, 7])

        value_iterator2 = dt.iter_values("Tim")
        value2 = next(value_iterator2)
        #print ("after next values with Tim are " , value2)
        self.assertIn(value2, [1, 6])

        value2 = next(value_iterator2)
        #print ("after next values with Tim are " , value2)
        self.assertIn(value2, [1, 6])


        """ del dt["May", "Jim"]
        del dt["Kim", "Tim"] """

        
        del dt["Tim", "Bob"]
        del dt["Tim", 'Jen']
        del dt["Ivy", "Jen"]

        # print ("after del is called")
        # print ("all the outer keys are " , dt.keys())
        # print ("all the keys of Tom are " , dt.keys("Tom"))
        # print ("all the keys of Tim are " , dt.keys("Tim"))

        # print ("all the values are " , dt.values())
        # print ("all the values of Tom are " , dt.values("Tom"))
        # print ("all the values of Tim are " , dt.values("Tim"))


        try:
            key2 = next(key_iterator2)
        except StopIteration:
            # print("Stop Iteration for key")
            pass
        else:
            #print ("key with Tom is " , key2)
            self.assertIn(key2, ["Ben", "Jen"])
        

        key = next(key_iterator)
        #print ("outer keys are " , key)
        self.assertIn(key, [ "Amy", "Tom", "Het"])

        try:
            value2 = next(value_iterator2)
        except StopIteration:
            # print("Stop Iteration for value")
            pass
        else:
           # print ("after next values with Tom are " , value2)
            self.assertIn(value2, [1, 6])

        value = next(value_iterator)
        #print("all value after next is " , value)
        self.assertIn(value, [2, 3, 5, 7, 8])

        #print("after del\n" , str(dt))


        del dt["Tom", "Ben"]
        del dt["Amy", "Ben"]
        del dt["Tom", "Jim"]
        del dt["Tom", "Tom"]
        del dt["Het", "Liz"]

        # print("after table delete\n" , str(dt))


        try:
            key = next(key_iterator)
        except StopIteration:
            # print("Stop Iteration for key")
            pass
        else:
            #print ("outer keys are " , key)
            self.assertIn(key, [])

        try:
            value = next(value_iterator)
        except StopIteration:
            # print("Stop Iteration for value")
            pass
        else:
            #print ("all value are  " , value2)
            self.assertIn(value, [])




        # Retrieving the next value should either raise StopIteration or crash entirely.
        # Note: Deleting from an element being iterated over is bad practice
        # We just want to make sure you aren't returning a list and are doing this
        # with an iterator.
        self.assertRaises(BaseException, lambda: next(key_iterator))
        self.assertRaises(BaseException, lambda: next(value_iterator))