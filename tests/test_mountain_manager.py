import unittest
from ed_utils.decorators import number

from copy import copy
from mountain import Mountain
from mountain_manager import MountainManager

class TestInfiniteHash(unittest.TestCase):

    @number("5.1")
    def test_example(self):
        m1 = Mountain("m1", 2, 2)
        m2 = Mountain("m2", 2, 9)
        m3 = Mountain("m3", 3, 6)
        m4 = Mountain("m4", 3, 1)
        m5 = Mountain("m5", 4, 6)
        m6 = Mountain("m6", 7, 3)
        m7 = Mountain("m7", 7, 7)
        m8 = Mountain("m8", 7, 8)
        m9 = Mountain("m9", 76, 6)
        m10 = Mountain("m10", 8, 4)

        mm = MountainManager()
        mm.add_mountain(m7)
        mm.add_mountain(m2)
        mm.add_mountain(m6)
        mm.add_mountain(m3)
        mm.add_mountain(m1)

        # print("sorted order is\n " ,mm.mountain_table)

        def make_set(my_list):
            
            """
            Since mountains are unhashable, add a method to get a set of all mountain ids.
            Ensures that we can compare two lists without caring about order."""
            
            return set(id(x) for x in my_list)

        # def make_set(my_list):
            
        #     """
        #     Since mountains are unhashable, add a method to get a set of all mountain ids.
        #     Ensures that we can compare two lists without caring about order."""
            
        #     return set(x.name for x in my_list)

        # set1 = make_set(mm.mountains_with_difficulty(3))
        # set2 = make_set([m3])

        # print("\nset 1 is " , set1)
        # print("\nset 2 is " , set2)

        self.assertEqual(make_set(mm.mountains_with_difficulty(3)), make_set([m3]))
        self.assertEqual(make_set(mm.mountains_with_difficulty(4)), make_set([]))
        self.assertEqual(make_set(mm.mountains_with_difficulty(7)), make_set([m6, m7]))

        mm.add_mountain(m4)
        mm.add_mountain(m5)
        mm.add_mountain(m8)
        mm.add_mountain(m9)

        res = mm.group_by_difficulty()
        # print("\nlol is " , res)
        self.assertEqual(len(res), 5)
        self.assertEqual(make_set(res[0]), make_set([m1, m2]))
        self.assertEqual(make_set(res[1]), make_set([m3, m4]))
        self.assertEqual(make_set(res[2]), make_set([m5]))
        self.assertEqual(make_set(res[3]), make_set([m6, m7, m8]))

        
        # mm.add_mountain(m10)

        #print("sorted order is\n " ,mm.mountain_list)

        # mm.remove_mountain(m5)

        #print("remvomed mountain m5\n " ,mm.mountain_list)


        mm.add_mountain(m10)

        # mount_diff_7 = mm.mountains_with_difficulty(7)
        # print("mount 7: " , mount_diff_7)

        # temp_mount = mount_diff_7[1]
        # print("temp mount is " , temp_mount)

        # print("\nall mounts are ", mm.mountain_table)

        # temp_mount.name = "wes"
        # print("\ntemp mount is " , temp_mount)

        # print("mount 7: " , mount_diff_7)

        # print("\nall mounts are ", mm.mountain_table)


        mm.edit_mountain(m5 , m10)
        mm.edit_mountain(m5 , m10)

        res = mm.group_by_difficulty()
        # print("\nlol is " , res)
        self.assertEqual(len(res), 5)

        self.assertEqual(make_set(res[3]), make_set([m10])) 

