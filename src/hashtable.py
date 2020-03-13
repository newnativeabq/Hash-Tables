# '''
# Linked List hash table key/value pair
# '''
import hashlib


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __repr__(self):
        return f'{self.key}: {self.value}'

    def delete(self):
        self.key = None 
        self.value = None
        if self.next is not None:
            temp_link = self.next
            self.next = None
            return temp_link
        else:
            return None


class LinkedList():
    def __init__(self, node: Node):
        self.head = node
    
    def search_key(self, key):
        current_node = self.head 
        if current_node.key == key:
            return current_node
        else:
            while current_node.next is not None:
                # print('searching')
                current_node = current_node.next
                if current_node.key == key:
                    return current_node
        return None

    def add(self, key, value):
        print('Adding: ', key, value)
        end = self.head
        while end.next is not None:
            print('chain node', end.key, end.value)
            end = end.next
        end.next = Node(key, value)
        print('added node', end.next.key, end.next.value)

    def remove(self, key):
        current_node = self.head 
        # Check head for key/node deletion
        if current_node.key == key:
            self.head = current_node.delete()
        else:
            while current_node.next is not None:
                next_node = current_node.next
                if next_node.key == key:
                    current_node.next = next_node.delete()

        raise KeyError('Key Not Found')

    def list(self):
        nodes = []
        node = self.head
        while node is not None:
            nodes.append(node)
            node = node.next 
        return nodes





class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity


    def __repr__(self):
        return ', '.join([str(node.key) + ': ' + str(node.value) for node in self.list_nodes()])


    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        a = hashlib.md5(key.encode('utf-8'))
        b = a.hexdigest()
        return hash(int(b, 16))


    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        pass


    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash(key) % self.capacity


    def insert(self, key, value):
        '''
        Store the value with the given key.

        # Part 1: Hash collisions should be handled with an error warning. (Think about and
        # investigate the impact this will have on the tests)

        # Part 2: Change this so that hash collisions are handled with Linked List Chaining.

        Fill this in.
        '''
        index = self._hash_mod(key)
        print('working_index: ', index)
        if self.storage[index] is None:
            self.storage[index] = LinkedList(node = Node(key, value))
        else:
            llist = self.storage[index]
            search = llist.search_key(key)
            if search is None:
                llist.add(key, value)
            else:
                search.value = value


    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        index = self._hash_mod(key)
        if self.storage[index] is None:
            raise KeyError('Key Not Found')
        else:
            llist = self.storage[index]
            search = llist.search_key(key)
            if search is None:
                raise KeyError('Key Not Found')
            else:
                search.delete()

    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        index = self._hash_mod(key)
        if self.storage[index] is None:
            print(f'Head Index {index} is None')
            raise KeyError(f'Key Not Found {key}')

        else:
            llist = self.storage[index]
            search = llist.search_key(key)
            print('Search Result', search)
            if search is None:
                raise KeyError(f'Key Not Found {key}')
            else:
                return search.value

    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''
        temp_hash_table = HashTable(capacity = self.capacity * 2)
        for node in self.list_nodes():
            print('moving node ', node.key, node.value)
            temp_hash_table.insert(node.key, node.value)
        self.storage = temp_hash_table.storage

    def list_nodes(self):
        nodes = []
        for llist in self.storage:
            if llist is not None:
                for node in llist.list():
                    nodes.append(node)
        return nodes


if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    # print("Hash Table: ", ht.storage[0].head, ht.storage[1].head)

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    print(ht)

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
