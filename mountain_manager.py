from mountain import Mountain
from algorithms.binary_search import binary_search
from double_key_table import DoubleKeyTable



"""It is assumed that all Double Key Table methods are O(1)"""

class MountainManager:

    def __init__(self) -> None:

        """
        defining the magic method : __init__ 
        - This initialises an object of the DoubleKeyTable class
        - The outer key is the difficulty level, inner key is the name and the value is Mountain object
        - It defines the hash function that is to be used

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
        
        self.mountain_table : DoubleKeyTable[int , str , Mountain] = DoubleKeyTable()
        self.mountain_table.hash1 = lambda k: (k % self.mountain_table.table_size)



    def add_mountain(self, mountain: Mountain) -> None:

        """
        - Adds a mountain to the manager

        Args:
        - self
        - mountain - of Mountain class
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        """

        self.mountain_table[mountain.difficulty_level , mountain.name] = mountain
        


    def remove_mountain(self, mountain: Mountain) -> None:

        """
        - Removes a mountain to the manager

        Args:
        - self
        - mountain - of Mountain class
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        """

        try:
            del self.mountain_table[mountain.difficulty_level , mountain.name]
        except KeyError:
            return
        else:
            return

        

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:

        """
        - Removes the old mountain and add the new mountain

        Args:
        - self
        - old - of Mountain class - the mountain to be removed
        - new - of Mountain class - the mountain to be added
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        """

        self.remove_mountain(mountain = old)
        self.add_mountain(mountain = new)


    
    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:

        """
        - Return a list of all mountains with the input difficulty 'diff' 

        Args:
        - self
        - diff - int
        
        Raises:
        - None

        Returns:
        - List of Mountain

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        """

        same_diff_mountain : list[Mountain] = self.mountain_table.values(diff)
        return same_diff_mountain

          

    def group_by_difficulty(self) -> list[list[Mountain]]:

        """
        - Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.

        Args:
        - self
        
        Raises:
        - None

        Returns:
        - A list of list of Mountain

        Complexity:
        - Worst case: O(N) , where N is the number of elements in the outer hash table - self.mountain_table
        - Best case: O(1)
        """

        grouped_list_diff : list[list[Mountain]] = []
        all_diff_iter = self.mountain_table.iter_keys(None)

        while True:
            try:
                key = next(all_diff_iter)
                
            except StopIteration:
                break
            
            else:
                mount_value = self.mountain_table.values(key = key)
                grouped_list_diff.append(mount_value)

        return grouped_list_diff
        