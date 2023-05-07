import unittest
from ed_utils.decorators import number

from mountain import Mountain
from mountain_organiser import MountainOrganiser
from mountain_manager import *

class TestInfiniteHash(unittest.TestCase):

    @number("6.1")
    def test_example(self):
        m1 = Mountain("m1", 2, 2)
        m2 = Mountain("m2", 2, 9)
        m3 = Mountain("m3", 3, 6)
        m4 = Mountain("m4", 3, 1)
        m5 = Mountain("m5", 4, 6)
        m6 = Mountain("m6", 7, 3)
        m7 = Mountain("m7", 7, 7)
        m8 = Mountain("m8", 7, 8)
        m9 = Mountain("m9", 7, 6)
        m10 = Mountain("m10", 8, 4)


        # m1 = Mountain("m1" , 2 , 3)
        # l1 = Mountain("l1" , 2 , 5)
        # l2 = Mountain("l2" , 4 , 1)
        # c1 = Mountain("c1" , 4 , 4)
        # t1 = Mountain("desting" , 76 , 3)
        # t2 = Mountain("testing" , 76 , 3)

        mo = MountainOrganiser()
        # mm = MountainManager()

        # mm.add_mountain(mountain = m1)
        # mm.add_mountain(mountain = l1)
        # mm.add_mountain(mountain = l2)
        # mm.add_mountain(mountain = c1)
        # mm.add_mountain(mountain = t1)

        # diff2 = mm.mountains_with_difficulty(2)
        # print("diff with 2 " , diff2)

        # mo.add_mountains(diff2)
        # print("org with 2 " , mo.sorted_mountain_list)

        # diff4 = mm.mountains_with_difficulty(4)
        # print("diff with 4 " , diff4)

        # mo.add_mountains(diff4)
        # print("org with 2 and 4 " , mo.sorted_mountain_list)

        # diff76 = mm.mountains_with_difficulty(76)
        # print("diff with 76 " , diff76)

        # mo.add_mountains(diff76)
        # print("org with 2 4 and 76 " , mo.sorted_mountain_list)

        # rank = mo.cur_position(t1)
        # del mo.sorted_mountain_list[rank]
        
        # mm.edit_mountain(t1 , t2)
        
        # diff76 = mm.mountains_with_difficulty(76)
        # print("diff with 76 " , diff76)

        # mo.add_mountains(diff76)
        # print("org with 2 4 and 76 " , mo.sorted_mountain_list)
        


        mo.add_mountains([m2, m1])

        # print("list is " , mo.sorted_mountain_list)

        self.assertEqual([mo.cur_position(m) for m in [m1, m2]], [0, 1])
        mo.add_mountains([m4, m3])
        self.assertEqual([mo.cur_position(m) for m in [m1, m2, m3, m4]], [1, 3, 2, 0])
        mo.add_mountains([m9])
        self.assertEqual([mo.cur_position(m) for m in [m1, m2, m3, m4, m9]], [1, 4, 2, 0, 3])
        mo.add_mountains([m7, m5, m6, m8])
        self.assertEqual([mo.cur_position(m) for m in [m1, m2, m3, m4, m5, m6, m7, m8, m9]], [1, 8, 3, 0, 4, 2, 6, 7, 5])

        # print("list is " , mo.sorted_mountain_list)
        
        self.assertRaises(KeyError, lambda: mo.cur_position(m10)) 
  