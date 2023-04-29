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

        # self.level = 0
        # table = self.top_level_table

        # while True:
        #     pos = self.hash(key)

        #     #inside index is not empty
        #     if isinstance(table[pos], tuple) and isinstance(table[pos][1], ArrayR):
        #         table = table[pos][1]
        #         self.level += 1
        #         print("level is " , self.level)
        #         print(key)
        #         continue

        #     elif isinstance(table[pos], tuple) and isinstance(table[pos][1], int):
        #         collision = table[pos] #lin 1
        #         print("collision will be :",collision, " in ",pos)
        #         table[pos] = (collision[0][:self.level],ArrayR(self.TABLE_SIZE))
        #         table = table[pos][1]
        #         self.level += 1
        #         print("level is " , self.level)
        #         table[self.hash(collision[0])] = collision
        #         print(" so now, i will make this ",collision, " into ",self.hash(collision[0]),"and",(key,value)," one will be in",self.hash(key))
        #         table[self.hash(key)] = (key,value)
                
                
        #         while self.hash(collision[0]) == self.hash(key): #lin and link are in same location
        #             print("However, now it detected we need to do one more hash table!")
                    
        #             print("going to make new table in",self.hash(collision[0]))
        #             table[pos] = (collision[0][:self.level],ArrayR(self.TABLE_SIZE))
        #             table = table[pos][1]
        #             self.level += 1
        #             print("level is " , self.level)

        #             table[self.hash(collision[0])] = collision
        #             table[self.hash(key)] = (key,value)
        #             print(" so now, i will make this ",collision, " into ",self.hash(collision[0]),"and",(key,value)," one will be in",self.hash(key))
        #             print("Done~")
                
        #         return

        #     else:
        #         table[pos] = (key,value)
        #         self.count += 1
        #         print("level is " , self.level)
        #         print("first, i will put this ",table[pos],"into",self.hash(key))
        #         print("done")
        #         return

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

        outer_array = self.top_level_table
        index_position = 0

        while True:
            # outer_key , outer_value = outer_array[index_position]

            # print("outer key and value is " , outer_key , outer_value , "at index " , index_position)

            index_position = self.hash(key = key)
            print("index position of input key is " , key ,index_position)
            
            if outer_array[index_position] == None:
                outer_array[index_position] = (key,value)

                for i in range (len(outer_array)):
                    if outer_array[i] != None:
                        print("outer array at index " , i , " is " , outer_array[i])

                return

            elif outer_array[index_position][0] == key:
                outer_array[index_position] = (key,value)

                for i in range (len(outer_array)):
                    if outer_array[i] != None:
                        print("outer array at index " , i , " is " , outer_array[i])

                return

            elif isinstance(outer_array[index_position][1] , int):
                outer_key , outer_value = outer_array[index_position]
                print("outer key and value is " , outer_key , outer_value , "at index " , index_position)

                inner_array : ArrayR[tuple[K,V|ArrayR [K,V]]] = ArrayR(length = self.TABLE_SIZE)
                outer_array[index_position] = (key[0 : self.level + 1], inner_array)

                print("new key and value is " , outer_array[index_position])
                
                self.level += 1

                print("new level is " , self.level)
                outer_array = inner_array
                
                index_position = self.hash(key = outer_key)                   
                outer_array[index_position] = (outer_key , outer_value)

                print("index position for original key is" , outer_key , index_position)

                continue


            else: 
                outer_key , outer_value = outer_array[index_position]
                print("outer key and value is " , outer_key , outer_value , "at index " , index_position)

                inner_array = outer_value

                print("outer key " , outer_key )

                for i in range (len(inner_array)):
                        if inner_array[i] != None:
                            print("inner array at index " , i , " is " , inner_array[i])

                self.level += 1
                print("next level is " , self.level)

                outer_array = inner_array

                continue



            
            # outer_key , outer_value = outer_array[index_position]

            # print("outer key and value is " , outer_key , outer_value , "at index " , index_position)
            
            # if isinstance(outer_value, ArrayR):
            #     while True:
            #         inner_array = outer_value

            #         print("outer key " , outer_key )

            #         for i in range (len(inner_array)):
            #                 if inner_array[i] != None:
            #                     print("inner array at index " , i , " is " , inner_array[i])

            #         self.level += 1
            #         print("next level is " , self.level)

            #         outer_array = inner_array
            
            #         index_position = self.hash(key = key)

            #         print("index position for input key is" , key , index_position)

            #         outer_key , outer_value = outer_array[index_position]
            
            #         if outer_array[index_position] == None:
            #             outer_array[index_position] = (key , value)

            #             for i in range (len(outer_array)):
            #                 if outer_array[i] != None:
            #                     print("outer array at index " , i , " is " , outer_array[i])

            #             return

            #         elif isinstance(outer_value, ArrayR):
            #             print("gone in elif to the next level\n")
                        
            #             continue

            #         else:
            #             while True:   
                
            #                 inner_array : ArrayR[tuple[K,V|ArrayR [K,V]]] = ArrayR(length = self.TABLE_SIZE)
            #                 outer_array[index_position] = (key[0 : self.level + 1], inner_array)

            #                 print("new key and value is " , outer_array[index_position])
                            
            #                 self.level += 1

            #                 print("new level is " , self.level)
            #                 outer_array = inner_array
                            
            #                 index_position = self.hash(key = outer_key)                   
            #                 outer_array[index_position] = (outer_key , outer_value)

            #                 print("index position for original key is" , outer_key , index_position)


            #                 index_position = self.hash(key = key)

            #                 print("index position for input key is" , key , index_position)
                    
            #                 if outer_array[index_position] == None:
            #                     outer_array[index_position] = (key , value)

            #                     for i in range (len(outer_array)):
            #                         if outer_array[i] != None:
            #                             print("outer array at index " , i , " is " , outer_array[i])

            #                     return

            #                 else:
            #                     outer_key , outer_value = outer_array[index_position]
            #                     print("gone in 30 secs, back to the else")



            # else:
            #     while True:   
                
            #         inner_array : ArrayR[tuple[K,V|ArrayR [K,V]]] = ArrayR(length = self.TABLE_SIZE)
            #         outer_array[index_position] = (key[0 : self.level + 1], inner_array)

            #         print("new key and value is " , outer_array[index_position])
                    
            #         self.level += 1

            #         print("new level is " , self.level)
            #         outer_array = inner_array
                    
            #         index_position = self.hash(key = outer_key)                   
            #         outer_array[index_position] = (outer_key , outer_value)

            #         print("index position for original key is" , outer_key , index_position)


            #         index_position = self.hash(key = key)

            #         print("index position for input key is" , key , index_position)
            
            #         if outer_array[index_position] == None:
            #             outer_array[index_position] = (key , value)

            #             for i in range (len(outer_array)):
            #                 if outer_array[i] != None:
            #                     print("outer array at index " , i , " is " , outer_array[i])

            #             return

            #         else:
            #             outer_key , outer_value = outer_array[index_position]
            #             print("gone in 30 secs, back to the else")

            

                
            