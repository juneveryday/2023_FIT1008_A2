from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR
from data_structures.hash_table import *

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

        # if sizes is not None:
        #     self.TABLE_SIZE = sizes

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
        raise NotImplementedError()

        


    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        self.level = 0
        self.assign_key_value(key, value)

        #raise NotImplementedError()



    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

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

    def assign_key_value(self, key: K, value: V) -> None:

        index_position = self.hash(key = key)

        if self.top_level_table[index_position] == None:
            self.top_level_table[index_position] = (key , value)

        elif self.top_level_table[index_position][0] == key:
            self.top_level_table[index_position] = (key , value)

        else:
            key_outer , value_outer = self.top_level_table[index_position]

            if key_outer[len(key_outer) - 1] != '*':
                outer_array = self.top_level_table
                inner_array : ArrayR[tuple[K,V|ArrayR [K,V]]] = ArrayR(length = self.TABLE_SIZE)
                outer_array[index_position] = (key[0 : self.level + 1] + "*", inner_array)
                
                print("\ntop test key " , outer_array[index_position][0])
                print("level is " , self.level)
                print("inner index is " , index_position)
                for i in range(len(outer_array)):
                    if outer_array[i] != None:
                        print(i, "Top outer array is " , outer_array[i], " outer key is " , key_outer)


                while True:    
                    self.level += 1
                    print("after level is " , self.level)
                    inner_index_position = self.hash(key = key_outer)
                    print("inner position of outer_key " , key_outer , " is " , inner_index_position)
                    inner_array[inner_index_position] = (key_outer , value_outer)
                    inner_index_position = self.hash(key = key)
                    print("inner position of key " , key , " is " , inner_index_position)

            
                    if inner_array[inner_index_position] == None:
                        inner_array[inner_index_position] = (key , value)

                        """ for i in range(len(outer_array)):
                            if outer_array[i] != None:
                                print(i, "outer array is " , outer_array[i], " outer key is " , key_outer)

                        print("before level is " , self.level) """
                        print("INNER FINAL index is " , inner_index_position) 
                        

                        break

                    else:
                        key_outer , value_outer = inner_array[inner_index_position]
                        outer_array = inner_array
                        inner_array : ArrayR[tuple[K,V|ArrayR [K,V]]] = ArrayR(length = self.TABLE_SIZE)
                        outer_array[inner_index_position] = (key[0 : self.level + 1] + "*" , inner_array)

                        print("\ntest key " , outer_array[inner_index_position][0] , "\n")
                        

                        for i in range(len(outer_array)):
                            if outer_array[i] != None:
                                print(i, "outer array is " , outer_array[i], " outer key is " , key_outer)

                        for i in range(len(inner_array)):
                            if inner_array[i] != None:
                                print(i, "inner array is " , inner_array[i], " inner key is " , key)


                        
                        print("inner index is " , inner_index_position)
                
            else:
                outer_array = self.top_level_table
                #inner_array : ArrayR[tuple[K,V|ArrayR [K,V]]] = ArrayR(length = self.TABLE_SIZE)
                #outer_array[index_position] = (key[0 : self.level + 1] + "*", inner_array)
                outer_array[index_position][1] = inner_array

                while True: 
                    self.level += 1
                    inner_index_position = self.hash(key = key)

                    if inner_array[inner_index_position] == None:
                        inner_array[inner_index_position] = (key , value)
                        break

                    else:
                        key_outer , value_outer = inner_array[inner_index_position]

                        outer_array = inner_array
                        inner_array : ArrayR[tuple[K,V|ArrayR [K,V]]] = ArrayR(length = self.TABLE_SIZE)
                        outer_array[index_position] = (key[0 : self.level + 1] + "*", inner_array)

                        inner_index_position = self.hash(key = key_outer)
                        inner_array[inner_index_position] = (key_outer , value_outer)

                        if inner_array[inner_index_position] == None:
                            inner_array[inner_index_position] = (key , value)
                            break
