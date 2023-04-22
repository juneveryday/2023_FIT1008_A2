from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes : list|None = None, internal_sizes : list|None = None) -> None:

        self.INTERNAL_TABLE_SIZES = self.TABLE_SIZES

        if sizes != None:
            self.TABLE_SIZES = sizes

        self.outer_size_index = 0
        self.outer_hash_table : ArrayR[tuple[K1, LinearProbeTable[K2, V]]] = ArrayR(self.TABLE_SIZES[self.outer_size_index])
        self.outer_count = 0
                  
        if internal_sizes != None:
            self.INTERNAL_TABLE_SIZES = internal_sizes



    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """

        outer_position = self.hash1(key1)

        for _ in range(self.table_size):
            if self.outer_hash_table[outer_position] is None:
                if is_insert:
                    internal_hash_table =  LinearProbeTable(sizes = self.INTERNAL_TABLE_SIZES)
                    internal_hash_table.hash = lambda k: self.hash2(k, internal_hash_table)
                    self.outer_hash_table[outer_position] = (key1, internal_hash_table)
                    self.outer_count += 1

                    inner_position = internal_hash_table._linear_probe(key = key2 , is_insert = is_insert)
                    return (outer_position, inner_position)

                raise KeyError(key1) #else if is_insert is false

            elif self.outer_hash_table[outer_position][0] == key1:
                internal_hash_table = self.outer_hash_table[outer_position][1]
                inner_position = internal_hash_table._linear_probe(key = key2 , is_insert = is_insert)
                return (outer_position , inner_position)
                
            
            outer_position = (outer_position + 1) % (self.table_size) # else search for the key empty slot

        if is_insert:
            raise FullError("Table is full!")
        
        raise KeyError(key1) # else if is_insert is false and key1 is not present in the hash table



    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """

        k_iter = KeyIterator(outer_table = self, key = key)
        return k_iter


    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """

        key_list = []
        
        for item in self.outer_hash_table:
            if item != None:
                key_item, inner_table_item = item
                if key != None:
                    if key == key_item:
                        return inner_table_item.keys()
                    else:
                        continue
                else:
                    key_list.append(key_item)                    

        return key_list


    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """

        v_iter = ValueIterator(outer_table = self, key = key)
        return v_iter
        

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        
        value_list = []

        for item in self.outer_hash_table:
            if item != None: 
                key_item, inner_table_item = item
                if key != None:
                    if key == key_item:
                        return inner_table_item.values()
                    else:
                        continue
                else:
                    temp_list = inner_table_item.values()

                    for i in temp_list:
                        value_list.append(i)
                    
        return value_list


    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """

        key1 = key[0]
        key2 = key[1]

        outer_index, inner_index = self._linear_probe(key1 = key1, key2 = key2, is_insert = False)
        inner_table = self.outer_hash_table[outer_index][1]
        return inner_table[inner_index][1]


    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        key1 = key[0]
        key2 = key[1]

        outer_key1_index, inner_key2_index = self._linear_probe(key1 = key1, key2 = key2, is_insert = True)

        inner_table = self.outer_hash_table[outer_key1_index][1]
        inner_table[key2] = data

        if len(self) > self.table_size / 2:
            self._rehash()

        

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        key1 = key[0]
        key2 = key[1]

        outer_key1_index, inner_key2_index = self._linear_probe(key1 = key1, key2 = key2, is_insert = False)

        inner_table = self.outer_hash_table[outer_key1_index][1]

        """ if len(self.key_list) != 0:
            self.key_list.remove(key1)
            # key 2 not removed
        

        # doesnt take values and doesnt store index key
        if len(self.value_list) != 0:
            self.value_list.remove(inner_table[key2])
            # key 2 not removed """

        del inner_table[key2]

        if len(inner_table) == 0:
            self.outer_hash_table[outer_key1_index] = None
            self.outer_count -= 1

            # Start moving over the cluster
            outer_key1_index = (outer_key1_index + 1) % self.table_size

            while self.outer_hash_table[outer_key1_index] is not None:
                key1_new, value = self.outer_hash_table[outer_key1_index]
                self.outer_hash_table[outer_key1_index] = None

                # Reinsert.
                new_outer_index, new_inner_index = self._linear_probe(key1_new, key2, True)
                self.outer_hash_table[new_outer_index] = (key1_new, value)
                outer_key1_index = (outer_key1_index + 1) % self.table_size

    

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """

        old_outer_hash_table = self.outer_hash_table
        self.outer_size_index += 1

        if self.outer_size_index >= len(self.TABLE_SIZES):
            return

        self.outer_hash_table : ArrayR[tuple[K1, LinearProbeTable[K2, V]]] = ArrayR(self.TABLE_SIZES[self.outer_size_index])
        self.outer_count = 0

        for item in old_outer_hash_table:
            if item != None:
                key1_new, value = item

                new_outer_index, new_inner_index = self._linear_probe(key1_new, key1_new, True)
                self.outer_hash_table[new_outer_index] = (key1_new, value)
                


    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.outer_hash_table)
        
    
    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.outer_count
    

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """

        result = ""
        for item_outer in self.outer_hash_table:
            if item_outer is not None:
                (key_outer, inner_table) = item_outer

                """ for item_inner in inner_table.array:
                    if item_inner is not None:
                        (key_inner , value) = item_inner
                        result += "(" + str(key_inner) + "," + str(value) + ")\n" """
                
                result += str(key_outer) + ":\n" + str(inner_table)
                result += "\n"

        return result




class KeyIterator(Iterator[K1|K2]):

    def __init__ (self, outer_table : DoubleKeyTable , key : K1|None = None) -> None :
        self.table = outer_table
        self.iterated_key = key
        self.index_position = 0
        

    def __iter__(self) -> Iterator[K1|K2]:
        return self

    def __next__(self) -> K1|K2:

        if self.iterated_key == None:
            temp_key = self.find_key(self.table.outer_hash_table)
            if temp_key != None:
                return temp_key
            
            raise StopIteration
        
        else:
            inner_table = None

            for item in self.table.outer_hash_table:
                if item != None:
                    key_item, inner_table_item = item
                    if self.iterated_key == key_item:
                        inner_table = inner_table_item

            if inner_table != None:
                temp_key = self.find_key(inner_table.array)
                if temp_key != None:
                    return temp_key

            raise StopIteration


    def find_key(self, array : ArrayR) -> K1|K2:

        for _ in range (self.index_position, len(array)):

            if array[self.index_position] != None:
                key_item = array[self.index_position][0]
                self.index_position += 1
                return key_item

            self.index_position += 1

        return None



class ValueIterator(Iterator[V]):

    def __init__ (self, outer_table : DoubleKeyTable , key : K1|None = None) -> None :
        self.table = outer_table
        self.iterated_key = key
        self.index_position = 0
        self.inner_index_position = 0

    def __iter__(self) -> Iterator[V]:
        return self

    def __next__(self) -> V:

        if self.iterated_key == None:

            for _ in range (self.index_position, len(self.table.outer_hash_table)):
                if self.table.outer_hash_table[self.index_position] != None:
                    inner_table = self.table.outer_hash_table[self.index_position][1]

                    temp_value = self.find_value(inner_table.array)
                    if temp_value != None:
                        return temp_value
                        
                self.index_position += 1
                self.inner_index_position = 0
            
        else:
            inner_table = None

            for item in self.table.outer_hash_table:
                if item != None:
                    if self.iterated_key == item[0]:
                        inner_table = item[1]

            if inner_table != None:
                temp_value = self.find_value(inner_table.array)
                if temp_value != None:
                    return temp_value

        raise StopIteration


    def find_value(self, array : ArrayR) -> V:

        for _ in range (self.inner_index_position, len(array)):
            if array[self.inner_index_position] != None:
                value_item = array[self.inner_index_position][1]
                self.inner_index_position += 1
                return value_item
                
            self.inner_index_position += 1
        
        return None



        
        



            
                



             