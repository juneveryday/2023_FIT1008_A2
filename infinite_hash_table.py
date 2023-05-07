from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR
from data_structures.hash_table import *
from data_structures.linked_stack import LinkedStack

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:

        self.top_level_table : ArrayR[tuple[K,V|ArrayR [K,V]]] = ArrayR(length = self.TABLE_SIZE)
        self.level = 0
        self.count = 0



    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1



    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """

        index_list , array_stack = self._infinite_probe(key = key)
        current_array = array_stack.pop()
        current_index = index_list.pop()
        return current_array[current_index][1]
                

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        self.level = 0
        outer_array = self.top_level_table
        
        while True:
            index_position = self.hash(key = key)
            
            if outer_array[index_position] == None:
                outer_array[index_position] = (key,value)
                self.count += 1
                return

            elif outer_array[index_position][0] == key:
                outer_array[index_position] = (key,value)
                return

            elif not isinstance(outer_array[index_position][1] , ArrayR):
                outer_key , outer_value = outer_array[index_position]

                inner_array : ArrayR[tuple[K,V|ArrayR [K,V]]] = ArrayR(length = self.TABLE_SIZE)
                outer_array[index_position] = (key[0 : self.level + 1], inner_array)
                
                self.level += 1
                outer_array = inner_array
                index_position = self.hash(key = outer_key)                   
                outer_array[index_position] = (outer_key , outer_value)

            else: 
                outer_key , outer_value = outer_array[index_position]
                self.level += 1
                outer_array = outer_value



    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        
        index_list , array_stack = self._infinite_probe(key = key)
        current_array = array_stack.pop()
        current_index = index_list.pop()
        current_array[current_index] = None
        self.count -= 1


        while not array_stack.is_empty():
            temp_list : list[tuple[K , V]] = []
            for i in range (len(current_array)):
                if current_array[i] != None:
                    if isinstance(current_array[i][1] , ArrayR):
                        return
                    else:
                        temp_list.append(current_array[i])

            if len(temp_list) == 1:
                current_array = array_stack.pop()
                current_index = index_list.pop()
                current_array[current_index] = temp_list[0]
            else:
                return


    def get_location(self, key : K) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """

        return self._infinite_probe(key = key)[0]



    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    
    def _infinite_probe(self, key : K) -> tuple[list[int] , LinkedStack[ArrayR]] :
        """
        
        """

        self.level = 0
        outer_array = self.top_level_table
        index_list : list[int] = []
        array_stack : LinkedStack[ArrayR] = LinkedStack()

        while True:
            index_position = self.hash(key = key)
            
            if outer_array[index_position] == None or (outer_array[index_position][0] != key and not isinstance(outer_array[index_position][1], ArrayR)):
                raise KeyError("key ", key ," does not exist")
            
            elif not isinstance(outer_array[index_position][1], ArrayR):
                index_list.append(index_position)
                array_stack.push(item = outer_array)
                return index_list , array_stack

            else:
                index_list.append(index_position)
                array_stack.push(item = outer_array)
                outer_array = outer_array[index_position][1]
                self.level += 1


    def __len__(self) -> int:
        return self.count


    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = ""
        temp_stack : LinkedStack[ArrayR] = LinkedStack()
        current_array : ArrayR = self.top_level_table
        outer_string = self.array_traversal(current_array = current_array , stack = temp_stack)
        result += outer_string

        while not temp_stack.is_empty():
            current_array = temp_stack.pop()
            inner_string = self.array_traversal(current_array = current_array , stack = temp_stack)

            result += inner_string 

        return result


    def array_traversal(self , current_array : ArrayR , stack : LinkedStack[ArrayR]) -> str:
        result = ""
    
        for array_index in range (len(current_array)):
            if current_array[array_index] != None:
                current_key, current_value = current_array[array_index]
                if isinstance(current_value , ArrayR):
                    stack.push(current_value)
                
                else:
                    result += str(current_key) + " , " + str(current_value) + "\n"

        return result



