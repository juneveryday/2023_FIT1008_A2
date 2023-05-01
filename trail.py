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

        list_of_mountains = self.collect_mountains()

        return list_of_mountains

        


    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """

        list_of_mountains : list[list[Mountain]] = [[]]

        list_of_mountains = self.collect_mountain_list()

        for i in range (len(list_of_mountains) -1 , -1 , -1):
            if len(list_of_mountains[i]) != k:
                del list_of_mountains[i]

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
    


    def collect_mountains(self) -> list[Mountain]:
        
        temp_mountain_list : list[Mountain] = []

        if self.store == None:
            return []
        
        else:
            if isinstance(self.store , TrailSeries):
                temp_mountain_list.append(self.store.mountain)
                temp_mountain_list += self.store.following.collect_mountains()

            elif isinstance(self.store , TrailSplit):
                temp_mountain_list += self.store.path_top.collect_mountains()
                temp_mountain_list += self.store.path_bottom.collect_mountains()
                temp_mountain_list += self.store.path_follow.collect_mountains()

            return temp_mountain_list
    

    
    def collect_mountain_list(self) -> list[list[Mountain]]:
        if self.store == None:
            return [[]]
        
        else:
            if isinstance(self.store , TrailSeries):

                temp_mountain_list : list[list[Mountain]] = None
                temp_mountain_list = [[self.store.mountain]]

                temp_list = self.store.following.collect_mountain_list()

                temp_mountain_list = self.combine_list(list1 = temp_mountain_list , list2 = temp_list)

                return temp_mountain_list
            
            elif isinstance(self.store , TrailSplit):
                temp_top_list : list[list[Mountain]]= [[]]
                temp_bot_list : list[list[Mountain]]= [[]]
                temp_fol_list : list[list[Mountain]]= [[]]

                temp_top_list = self.store.path_top.collect_mountain_list()

                temp_bot_list = self.store.path_bottom.collect_mountain_list()

                temp_fol_list = self.store.path_follow.collect_mountain_list()

                temp_top_list = self.combine_list(list1 = temp_top_list , list2 = temp_fol_list)

                temp_bot_list = self.combine_list(list1 = temp_bot_list , list2 = temp_fol_list)

                return temp_top_list + temp_bot_list
            

            
    def combine_list(self, list1 : list[list[Mountain]] , list2 : list[list[Mountain]]) -> list[list[Mountain]]:

        temp_list : list[list[Mountain]] = None
        for list_index1 in range (len(list1)):
            for list_index2 in range (len(list2)):
                if temp_list != None:
                    temp_list += [list1[list_index1] + list2[list_index2]]
                else:
                    temp_list = [list1[list_index1] + list2[list_index2]]

        return temp_list



