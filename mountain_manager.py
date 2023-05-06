from mountain import Mountain
from algorithms.binary_search import binary_search
from double_key_table import DoubleKeyTable

import copy

class MountainManager:

    def __init__(self) -> None:
        self.mountain_table : DoubleKeyTable[int , str , Mountain] = DoubleKeyTable()
        self.mountain_table.hash1 = lambda k: (k % self.mountain_table.table_size)



    def add_mountain(self, mountain: Mountain) -> None:
        self.mountain_table[mountain.difficulty_level , mountain.name] = mountain
        


    def remove_mountain(self, mountain: Mountain) -> None:
        try:
            del self.mountain_table[mountain.difficulty_level , mountain.name]
        except KeyError:
            return
        else:
            return

        

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        self.remove_mountain(mountain = old)
        self.add_mountain(mountain = new)


    
    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        same_diff_mountain : list[Mountain] = self.mountain_table.values(diff)
        return same_diff_mountain

          

    def group_by_difficulty(self) -> list[list[Mountain]]:

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

        