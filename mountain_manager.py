from mountain import Mountain
from algorithms.binary_search import binary_search

class MountainManager:

    def __init__(self) -> None:
        self.mountain_list : list[Mountain] = []




    def add_mountain(self, mountain: Mountain) -> None:
        mountain_index = binary_search(l = self.mountain_list, item = mountain, key = lambda x : (x.difficulty_level, x.name), is_insert = True)
        #print("index is " , mountain_index , "mountain is ", mountain)
        self.mountain_list.insert(mountain_index , mountain)



    def remove_mountain(self, mountain: Mountain) -> None:
        mountain_index = binary_search(l = self.mountain_list, item = mountain, key = lambda x : (x.difficulty_level, x.name))
        #print("index is " , mountain_index , "mountain is ", mountain)
        del self.mountain_list[mountain_index]

        

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        self.remove_mountain(mountain = old)
        self.add_mountain(mountain = new)


    
    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        same_diff_mountain : list[Mountain] = []

        for diff_index in range(len(self.mountain_list)):
            if self.mountain_list[diff_index].difficulty_level == diff:
                same_diff_mountain.append(self.mountain_list[diff_index])

        #print("mount with same diff" ,diff , " are " , same_diff_mountain)
        return same_diff_mountain

        

    def group_by_difficulty(self) -> list[list[Mountain]]:

        """ index_diff = 0
        grouped_list_diff : list[list[Mountain]] = []

        while (index_diff < len(self.mountain_list)):
            
            grouped_list : list[Mountain] = []
        
            while True:
                grouped_list.append(self.mountain_list[index_diff])
                index_diff += 1

                if index_diff >= len(self.mountain_list) or self.mountain_list[index_diff - 1].difficulty_level != self.mountain_list[index_diff].difficulty_level:
                    break
                
            grouped_list_diff.append(grouped_list)

        return grouped_list_diff """

        index_diff = 0
        grouped_list_diff : list[list[Mountain]] = []

        while (index_diff < len(self.mountain_list)):
            
            grouped_list : list[Mountain] = self.mountains_with_difficulty(self.mountain_list[index_diff].difficulty_level)
            index_diff += len(grouped_list)
    
            grouped_list_diff.append(grouped_list)
            
        #print("\nlol is" , grouped_list_diff)
        return grouped_list_diff
            