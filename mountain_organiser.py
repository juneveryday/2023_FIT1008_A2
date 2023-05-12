from __future__ import annotations

from mountain import Mountain
from algorithms.mergesort import mergesort , merge
from algorithms.binary_search import binary_search

class MountainOrganiser:

    def __init__(self) -> None:

        """
        defining the magic method : __init__ 
        - It creates a list of Mountain objects
        - This list is expected to be sorted in the order : tuple(length , name)
        - The index in the list is the rank of the mountain

        Args:
        - self
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        """

        self.sorted_mountain_list : list[Mountain] = []


    def cur_position(self, mountain: Mountain) -> int:

        """
        - Finds the rank of the provided mountain given all mountains included so far
        
        Args:
        - self
        - mountain - of Mountain class
        
        Raises:
        - Raises KeyError if the Mountain object is not added yet

        Returns:
        - int - which is the rank

        Complexity:
        - Worst case: O(log(N)) , where N is the total number of mountains included so far
        - Best case: O(1)
        """
         
        rank = binary_search (l = self.sorted_mountain_list, item = mountain, key = lambda a : (a.length , a.name))
        return rank


    def add_mountains(self, mountains: list[Mountain]) -> None:

        """
        - Adds a list of mountains to the organiser
        
        Args:
        - self
        - mountains - list of Mountain objects
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(Mlog(M) + N), where M is the length of the input list, and N is the total number of mountains included so far
        - Best case: O(1)
        """

        temp_sort = mergesort(l = mountains, key = lambda a : (a.length , a.name)) # O(Mlog(M))
        self.sorted_mountain_list = merge(l1 = temp_sort , l2 = self.sorted_mountain_list , key = lambda a : (a.length , a.name)) # O(N)
 
        
