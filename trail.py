from __future__ import annotations
from dataclasses import dataclass

import copy

from mountain import Mountain
from data_structures.linked_stack import LinkedStack

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""

        self.path_top = None
        self.path_bottom = None
        return self.path_follow.store


@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""

        self.mountain = None
        return self.following.store


    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""

        temp_store = TrailSeries (
                    mountain = mountain,
                    following = Trail(store = self))
                    
        return temp_store


    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""

        temp_store = TrailSplit(
                        path_top = Trail(store = None), 
                        path_bottom = Trail(store = None), 
                        path_follow = Trail(store = self)
                        ) 

        return temp_store

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""

        temp_store = TrailSeries(
                        mountain = self.mountain, 
                        following = Trail (store = 
                                TrailSeries(
                                    mountain = mountain, 
                                    following = self.following
                                    )
                                )
                            )
        return temp_store


    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""

        temp_branch = TrailSeries(
                        mountain = self.mountain, 
                        following = Trail(store = TrailSplit(
                                        path_top = Trail(store = None), 
                                        path_bottom = Trail(store = None), 
                                        path_follow = self.following
                                        )
                                    )
                                )
        return temp_branch


TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""

        temp_trail = Trail (store = TrailSeries(
                                mountain = mountain, 
                                following = self
                                )
                            )
        return temp_trail


    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""

        temp_trail = Trail(store = TrailSplit(
                                path_top = Trail(store = None), 
                                path_bottom = Trail(store = None), 
                                path_follow = self
                                )
                            )
        return temp_trail


    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""

        temp_stack_follow = LinkedStack()
        temp_new_trail : Trail = self

        temp_new_trail.traverse_trail(stack = temp_stack_follow, personality = personality)

        while not temp_stack_follow.is_empty():

            temp_new_trail = temp_stack_follow.pop()

            temp_new_trail.traverse_trail(stack = temp_stack_follow, personality = personality)

        return



    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""

        list_of_mountains : list[Mountain] = []

        self.collect_mountains(mountain_list = list_of_mountains)

        print("list of mountains is " , list_of_mountains)
        print("\nlength of list of mountains is " , len(list_of_mountains))

        return list_of_mountains

        


    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """

        list_of_mountains : list[list[Mountain]] = [[]]

        list_of_mountains = self.collect_mountain_list()

        print("length of list of list is " , len(list_of_mountains))
        for i in range (len(list_of_mountains)):

            print("\nlist of mountains at index " , i , " is " , list_of_mountains[i] , "\n")

            if len(list_of_mountains[i]) != k:
                del list_of_mountains[i]

        print("\nlist  of mountains is " , list_of_mountains , " with length " , len(list_of_mountains))
        return list_of_mountains




    def traverse_trail(self, stack : LinkedStack , personality : WalkerPersonality) -> None:
        
        temp_new_trail = self

        while temp_new_trail.store != None:
            if isinstance (temp_new_trail.store, TrailSeries) :
                personality.add_mountain(temp_new_trail.store.mountain)
                temp_new_trail = temp_new_trail.store.following

            elif isinstance (temp_new_trail.store, TrailSplit) :
                stack.push(temp_new_trail.store.path_follow)
                
                if personality.select_branch(top_branch = temp_new_trail.store.path_top , bottom_branch = temp_new_trail.store.path_bottom) == True:
                    temp_new_trail = temp_new_trail.store.path_top

                else:
                    temp_new_trail = temp_new_trail.store.path_bottom

        return
    


    def collect_mountains(self, mountain_list : list[Mountain]) -> None:
        
        if self.store != None:
            if isinstance(self.store , TrailSeries):
                mountain_list.append(self.store.mountain)
                self.store.following.collect_mountains(mountain_list = mountain_list)

            elif isinstance(self.store , TrailSplit):
                self.store.path_top.collect_mountains(mountain_list = mountain_list)
                self.store.path_bottom.collect_mountains(mountain_list = mountain_list)
                self.store.path_follow.collect_mountains(mountain_list = mountain_list)

        return
    

    
    def collect_mountain_list(self) -> list[list[Mountain]]:
        if self.store != None:
            if isinstance(self.store , TrailSeries):

                print("\nentering trailseries")
                temp_mountain_list : list[list[Mountain]] = None
                temp_mountain_list = [[self.store.mountain]]
                print("\nentering recursion so before it mountain list of list is " , temp_mountain_list)

                temp_list = self.store.following.collect_mountain_list()
                
                if temp_list != None:

                    for list_index in range (len(temp_list)):
                        temp_list[list_index] = temp_mountain_list[0] + temp_list[list_index]

                        print("\nfor index" , list_index , " temp list is " , temp_list[list_index])
                
                    temp_mountain_list = temp_list
                print("\nafter recursion mountain list of list is " , temp_mountain_list, "\n")
                return temp_mountain_list
            
            elif isinstance(self.store , TrailSplit):
                temp_top_list : list[list[Mountain]]= [[]]
                temp_bot_list : list[list[Mountain]]= [[]]
                temp_fol_list : list[list[Mountain]]= [[]]

                print("\nentering trailsplit")
                print("recursively calling top")
                temp_list = self.store.path_top.collect_mountain_list()

                if temp_list != None:
                    temp_top_list = temp_list
                    print("\ntop list is " , temp_top_list, "\n")


                print("recursively calling bottom")
                temp_list = self.store.path_bottom.collect_mountain_list()

                if temp_list != None:
                    temp_bot_list = temp_list
                    print("\nbottom list is " , temp_bot_list, "\n")


                print("recursively calling follow")
                temp_fol_list = self.store.path_follow.collect_mountain_list()

                temp_topfol_list : list[list] = None
                temp_botfol_list : list[list] = None

                if temp_fol_list != None:
                    for list_index in range (len(temp_top_list)):
                        for fol_index in range (len(temp_fol_list)):
                            if temp_topfol_list != None:
                                temp_topfol_list += [temp_top_list[list_index] + temp_fol_list[fol_index]]
                            else:
                                temp_topfol_list = [temp_top_list[list_index] + temp_fol_list[fol_index]]

                    temp_top_list = temp_topfol_list

                    print("\ntop list with follow is " , temp_top_list, "\n")

                    for list_index in range (len(temp_bot_list)):
                        for fol_index in range (len(temp_fol_list)):
                            if temp_botfol_list != None:
                                temp_botfol_list += [temp_bot_list[list_index] + temp_fol_list[fol_index]]
                            else:
                                temp_botfol_list = [temp_bot_list[list_index] + temp_fol_list[fol_index]]

                    temp_bot_list = temp_botfol_list

                    print("\nbottom list with follow is " , temp_bot_list, "\n")

                return temp_top_list + temp_bot_list













               
        # if self.store != None:
        #     if isinstance(self.store , TrailSeries):
        #         print("\nentering trailseries\n")
        #         #mountain_list[list_index].append(self.store.mountain)
        #         mountain_list[list_index] = [self.store.mountain] + mountain_list[list_index]
        #         self.store.following.collect_mountain_list(list_index = list_index , mountain_list = mountain_list)


        #     elif isinstance(self.store , TrailSplit):

        #         print("\n\nentering trailsplit\n")
        #         print("list index is " , list_index)
        #         print("length of mountain list is " , len(mountain_list))
                

        #         if len(mountain_list) <= list_index:
        #             mountain_list.insert(list_index, [])

        #         temp_list_of_mountain : list[Mountain] = copy.deepcopy(mountain_list[list_index])

        #         print("\ntemp list of mount is " , temp_list_of_mountain)
        #         print("before follow list index is " , list_index , "\nMountain list[list index] is " , mountain_list[list_index])

        #         self.store.path_follow.collect_mountain_list(list_index = list_index , mountain_list = mountain_list)
        #         temp_list_of_mountain = mountain_list[list_index] + temp_list_of_mountain

        #         print("\ntemp list of mount is " , temp_list_of_mountain)
        #         print("after follow list index is " , list_index , "\nMountain list[list index] is " , mountain_list[list_index])

        #         print("\ntemp list of mount is " , temp_list_of_mountain)
        #         print("before top list index is " , list_index , "\nMountain list[list index] is " , mountain_list[list_index])

        #         self.store.path_top.collect_mountain_list(list_index = list_index , mountain_list = mountain_list)

                      
        #         list_index += 1

        #         if len(mountain_list) <= list_index:
        #             mountain_list.insert(list_index, [])

        #         #else:
        #         # temp_list_of_mountain : list[Mountain] = mountain_list[list_index]
        #         # mountain_list.insert(list_index , temp_list_of_mountain)

                
        #         mountain_list[list_index] = copy.deepcopy(temp_list_of_mountain)

        #         print("\ntemp list of mount is " , temp_list_of_mountain)
        #         print("before bottom list index is " , list_index , "\nMountain list[list index] is " , mountain_list[list_index])

        #         self.store.path_bottom.collect_mountain_list(list_index = list_index, mountain_list = mountain_list)

        #         print("\ntemp list of mount is " , temp_list_of_mountain)
        #         print("after bottom list index is " , list_index , "\nMountain list[list index] is " , mountain_list[list_index])

        #         self.store.path_follow.collect_mountain_list(list_index = list_index , mountain_list = mountain_list)

        #         print("\ntemp list of mount is " , temp_list_of_mountain)
        #         print("after follow after bottom list index is " , list_index , "\nMountain list[list index] is " , mountain_list[list_index])

        # return












