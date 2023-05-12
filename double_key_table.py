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

        """
        defining the magic method : __init__ 
        - This initialises an object of the ArrayR class, outer array count, table sizes and outer table size index

        Args:
        - self
        - sizes - a list for the sizes of the outer array
        - internal_sizes - a list for the sizes of the inner array

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        """

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
        - Find the correct position for this key in the hash table using linear probing.

        Args:
        - self
        - key1 - outer key
        - key2 - inner key
        - is_insert - bool to insert (true) or search (false)

        Raises:
        - raises KeyError: When the key pair is not in the table, but is_insert is False.
        - raises FullError: When a table is full and cannot be inserted.

        Returns:
        - tuple[int , int] - the outer and inner indices corresponding to where input keys would be hashed

        Complexity:
        - Worst case: O(len(key1) + N * (len(key2) + other_function)) , where N is the table size and other_function is O(_linear_probe) of LinearProbeTable
        - Best case: O(len(key1) + len(key2) + other_function)
        """

        outer_position = self.hash1(key1)
        inner_position = -1

        for _ in range(self.table_size):
            if self.outer_hash_table[outer_position] is None:
                if is_insert:
                    if key2 != None:
                        internal_hash_table : LinearProbeTable[K2 , V] =  LinearProbeTable(sizes = self.INTERNAL_TABLE_SIZES)
                        internal_hash_table.hash = lambda k: self.hash2(k, internal_hash_table)
                        self.outer_hash_table[outer_position] = (key1, internal_hash_table)  
                        inner_position = internal_hash_table._linear_probe(key = key2 , is_insert = is_insert)

                    self.outer_count += 1    
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

        Args:
        - self
        - key - outer key or None

        Raises:
        - raises StopIteration

        Returns:
        - Iterator

        Complexity:
        - Worst case: 
        - Best case: 
        """

        return KeyIterator(outer_table = self, key = key) 


    def keys(self, key:K1|None=None) -> list[K1|K2]:
       
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        Args:
        - self
        - key - outer key or None

        Raises:
        - None

        Returns:
        - A list of keys

        Complexity:
        - Worst case: O(N * other_function) , where N is the length of the outer array - self.outer_hash_table and other function is O(inner_table_item.keys)
        - Best case: O(N)
        """
        
        key_list : list[K1|K2] = []
        
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

        Args:
        - self
        - key - outer key or None

        Raises:
        - raises StopIteration

        Returns:
        - Iterator

        Complexity:
        - Worst case: 
        - Best case: 
        """

        return ValueIterator(outer_table = self, key = key)
        
        

    def values(self, key:K1|None=None) -> list[V]:
        
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        Args:
        - self
        - key - outer key or None

        Raises:
        - None

        Returns:
        - A list of values

        Complexity:
        - Worst case: O(N * other_function) , where N is the length of the outer array - self.outer_hash_table and other function is O(inner_table_item.keys)
        - Best case: O(N * other_function)
        """
        
        value_list : list[V] = []

        for item in self.outer_hash_table:
            if item != None: 
                key_item, inner_table_item = item
                if key != None:
                    if key == key_item:
                        return inner_table_item.values()
                    else:
                        continue
                else:
                    value_list.extend(inner_table_item.values())
                    
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

        Args:
        - self
        - key - tuple of outer and inner key

        Raises:
        - Raises KeyError: when the key doesn't exist.

        Returns:
        - Value corresponding to the input keys 

        Complexity:
        The complexites are the same as O(_linear_probe) of DoubleKeyTable
        - Worst case: O(len(key1) + N * (len(key2) + other_function)) , where N is the table size and other_function is O(_linear_probe) of LinearProbeTable
        - Best case: O(len(key1) + len(key2) + other_function) 
        """

        outer_index, inner_index = self._linear_probe(key1 = key[0], key2 = key[1], is_insert = False)
        inner_table : LinearProbeTable[K2,V] = self.outer_hash_table[outer_index][1]
        return inner_table[key[1]]


    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        
        """
        Set an (key, value) pair in our hash table.

        Args:
        - self
        - key - tuple of outer and inner key
        - data - value

        Raises:
        - Raises FullError: when the table cannot be resized further.

        Returns:
        - None

        Complexity:
        The complexites are the same as O(_linear_probe) of DoubleKeyTable
        - Worst case: O(len(key1) + N * (len(key2) + other_function)) , where N is the table size and other_function is O(_linear_probe) of LinearProbeTable
        - Best case: O(len(key1) + len(key2) + other_function) 
        """

        outer_index, inner_index = self._linear_probe(key1 = key[0], key2 = key[1], is_insert = True)
        inner_table : LinearProbeTable[K2,V] = self.outer_hash_table[outer_index][1]
        inner_table[key[1]] = data

        if len(self) > self.table_size / 2:
            self._rehash()

        

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        
        """
        Deletes a (key, value) pair in our hash table.

        Args:
        - self
        - key - tuple of outer and inner key

        Raises:
        - raises KeyError: when the key doesn't exist.

        Returns:
        - value

        Complexity:
        - Worst case: O(_linear_probe + other_function1 + M * other_function2) where _linear_probe is of DoubleKeyTable class, 
            other_function1 is delitem of LinearProbeTable and other_function2 is _linear_probe of LinearProbeTable
        - Best case: O(_linear_probe + other_function1) , when len(inner_table) != 0
        """
        
        outer_index, inner_index = self._linear_probe(key1 = key[0], key2 = key[1], is_insert = False)

        inner_table : LinearProbeTable[K2,V] = self.outer_hash_table[outer_index][1]

        del inner_table[key[1]]

        if len(inner_table) == 0:
            self.outer_hash_table[outer_index] = None
            self.outer_count -= 1

            # Start moving over the cluster
            outer_index = (outer_index + 1) % self.table_size

            while self.outer_hash_table[outer_index] is not None:
                key1_new, value = self.outer_hash_table[outer_index]
                self.outer_hash_table[outer_index] = None

                # Reinsert.
                new_outer_index, new_inner_index = self._linear_probe(key1 = key1_new, key2 = None, is_insert = True)
                self.outer_hash_table[new_outer_index] = (key1_new, value)
                outer_index = (outer_index + 1) % self.table_size

    

    def _rehash(self) -> None:
        
        """
        Need to resize table and reinsert all values

        Args:
        - self

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(N * _linear_probe) , where N is len(old_outer_hash_table) and _linear_probe is of DoubleKeyTable
        - Best case: O(N * _linear_probe) 
        """

        old_outer_hash_table = self.outer_hash_table
        self.outer_size_index += 1

        if self.outer_size_index >= len(self.TABLE_SIZES):
            return

        self.outer_hash_table : ArrayR[tuple[K1, LinearProbeTable[K2, V]]] = ArrayR(self.TABLE_SIZES[self.outer_size_index])
        self.outer_count = 0

        for item in old_outer_hash_table:
            if item != None:
                key, value = item

                new_outer_index, new_inner_index = self._linear_probe(key1 = key, key2 = None, is_insert = True)
                self.outer_hash_table[new_outer_index] = (key, value)
                


    @property
    def table_size(self) -> int:
        
        """
        Return the current size of the table (different from the length)

        Args:
        - self

        Raises:
        - None

        Returns:
        - int - current table size

        Complexity:
        - Worst case: O(1)
        - Best case: O(1) 
        """
        return len(self.outer_hash_table)
        
    
    def __len__(self) -> int:
        
        """
        Returns number of elements in the hash table

        Args:
        - self

        Raises:
        - None

        Returns:
        - int - total number of elements in the hash table

        Complexity:
        - Worst case: O(1)
        - Best case: O(1) 
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
                
                result += str(key_outer) + ":\n" + str(inner_table)
                result += "\n"

        return result




class KeyIterator(Iterator[K1|K2]):

    def __init__ (self, outer_table : DoubleKeyTable , key : K1|None = None) -> None :

        """
        defining the magic method : __init__ 
        - This initialises an object of the DoubleKeyTable class, iterated key and index position

        Args:
        - self
        - outer_table - of DoubleKeyTable class
        - key - outer key or None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        """

        self.table = outer_table
        self.iterated_key = key
        self.index_position = 0
        

    def __iter__(self) -> Iterator[K1|K2]:

        """
        defining the magic method : __iter__ 
        - it returns itself, i.e. iterator object

        Args:
        - self

        Raises:
        - None

        Returns:
        - Iterator

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        """

        return self

    def __next__(self) -> K1|K2:

        """
        defining the magic method : __next__ 
        - it returns the next item

        Args:
        - self

        Raises:
        - Raises StopIteration

        Returns:
        - key - K1 or K2

        Complexity:
        - Worst case: O(N + find_key) , where N is the lenght of self.table.outer_hash_table and find_key is of DoubleKeyTable class (worst case)
        - Best case: O(find_key) , this would take the best case of find_key
        """

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

        """
        - This is to find the key needed

        Args:
        - self
        - array - of ArrayR class

        Raises:
        - None

        Returns:
        - key - K1 or K2

        Complexity:
        - Worst case: O(N) , where N is the length of array
        - Best case: O(1)
        """

        for _ in range (self.index_position, len(array)):

            if array[self.index_position] != None:
                key_item = array[self.index_position][0]
                self.index_position += 1
                return key_item

            self.index_position += 1

        return None



class ValueIterator(Iterator[V]):

    def __init__ (self, outer_table : DoubleKeyTable , key : K1|None = None) -> None :

        """
        defining the magic method : __init__ 
        - This initialises an object of the DoubleKeyTable class, iterated key, index position and inner index position

        Args:
        - self
        - outer_table - of DoubleKeyTable class
        - key - outer key or None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        """

        self.table = outer_table
        self.iterated_key = key
        self.index_position = 0
        self.inner_index_position = 0

    def __iter__(self) -> Iterator[V]:

        """
        defining the magic method : __iter__ 
        - it returns itself, i.e. iterator object

        Args:
        - self

        Raises:
        - None

        Returns:
        - Iterator

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        """

        return self

    def __next__(self) -> V:

        """
        defining the magic method : __next__ 
        - it returns the next item

        Args:
        - self

        Raises:
        - Raises StopIteration

        Returns:
        - value - of the input keys

        Complexity:
        - Worst case: O(N * find_value) , where N is the lenght of self.table.outer_hash_table and find_value is of DoubleKeyTable class (worst case)
        - Best case: O(N + find_value) , this would take the best case of find_value
        """

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

        """
        - This is to find the value needed

        Args:
        - self
        - array - of ArrayR class

        Raises:
        - None

        Returns:
        - value - of the input keys

        Complexity:
        - Worst case: O(N) , where N is the length of array
        - Best case: O(1)
        """

        for _ in range (self.inner_index_position, len(array)):
            if array[self.inner_index_position] != None:
                value_item = array[self.inner_index_position][1]
                self.inner_index_position += 1
                return value_item
                
            self.inner_index_position += 1
        
        return None



        
        



            
                



             