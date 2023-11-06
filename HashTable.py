class HashTable:
    def __init__(self, initial_capacity=16, load_factor=0.7):
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def _hash(self, key):
        # A simple hash function that sums the ASCII values of the characters in the key
        hash_value = 0
        for char in key:
            hash_value += ord(char)
        return hash_value % self.capacity

    def _resize(self):
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        # Rehash existing key-value pairs into the new table
        for bucket in self.table:
            if bucket:
                for key, value in bucket:
                    new_index = self._hash(key) % new_capacity
                    if not new_table[new_index]:
                        new_table[new_index] = []
                    new_table[new_index].append((key, value))

        self.capacity = new_capacity
        self.table = new_table

    def put(self, key, value):
        if self.size >= self.load_factor * self.capacity:
            self._resize()

        index = self._hash(key)
        if not self.table[index]:
            self.table[index] = []
        # Check if the key already exists in the bucket
        for i, (existing_key, _) in enumerate(self.table[index]):
            if existing_key == key:
                self.table[index][i] = (key, value)  # Update the value
                return
        self.table[index].append((key, value))
        self.size += 1

    def get(self, key):
        index = self._hash(key)
        if self.table[index]:
            for existing_key, value in self.table[index]:
                if existing_key == key:
                    return value
        return None

    def remove(self, key):
        index = self._hash(key)
        if self.table[index]:
            for i, (existing_key, _) in enumerate(self.table[index]):
                if existing_key == key:
                    self.table[index].pop(i)
                    self.size -= 1
                    return

if __name__ == '__main__':
    ht = HashTable()

    ht.put("key1", "value1")
    ht.put("key2", "value2")
    ht.put("key3", "value3")

    print(ht.get("key1"))  # Output: "value1"
    print(ht.get("key2"))  # Output: "value2"
    print(ht.get("key3"))  # Output: "value3"

    ht.remove("key2")
    print(ht.get("key2"))  # Output: None
