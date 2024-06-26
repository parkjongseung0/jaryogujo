import time
class Node:
    def __init__(self, key, size, color='RED'):
        self.key = key
        self.size = size
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0, 0, 'BLACK')
        self.root = self.TNULL

    def insert(self, key, size):
        node = Node(key, size)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 'RED'

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = 'BLACK'
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)

    def delete(self, key):
        self.delete_node_helper(self.root, key)

    def get_best_fit(self, size):
        best_fit = None
        x = self.root
        while x != self.TNULL:
            if x.size >= size:
                best_fit = x
                x = x.left
            else:
                x = x.right
        return best_fit

    def fix_insert(self, k):
        while k.parent.color == 'RED':
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 'RED':
                    u.color = 'BLACK'
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 'RED':
                    u.color = 'BLACK'
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'BLACK'

    def delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.key == key:
                z = node

            if node.key <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == 'BLACK':
            self.fix_delete(x)

    def fix_delete(self, x):
        while x != self.root and x.color == 'BLACK':
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 'RED':
                    s.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 'BLACK' and s.right.color == 'BLACK':
                    s.color = 'RED'
                    x = x.parent
                else:
                    if s.right.color == 'BLACK':
                        s.left.color = 'BLACK'
                        s.color = 'RED'
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 'BLACK'
                    s.right.color = 'BLACK'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 'RED':
                    s.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 'BLACK' and s.left.color == 'BLACK':
                    s.color = 'RED'
                    x = x.parent
                else:
                    if s.left.color == 'BLACK':
                        s.right.color = 'BLACK'
                        s.color = 'RED'
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 'BLACK'
                    s.left.color = 'BLACK'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'BLACK'

    def rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y


class Allocator:
    def __init__(self):
        self.chunk_size = 16 * 1024  # 16KB
        self.arena = []  # 실제 할당된 메모리 청크의 시작 주소를 저장하는 리스트
        self.used_chunks = {}  # {id: (start, size)}
        self.free_chunks = RedBlackTree()  # Red-Black Tree for free chunks
        self.total_allocated = 0  # total allocated memory size
        self.start_time = time.time()

        # Initialize with one big free chunk
        self.free_chunks.insert(0, self.chunk_size)

    def print_stats(self):
        total_arena = len(self.arena) * self.chunk_size / 1024 / 1024  # MB
        in_use = self.total_allocated / 1024 / 1024  # MB
        utilization = in_use / total_arena if total_arena > 0 else 0
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        print(f"Execution Time: {elapsed_time:.2f} seconds")
        print(f"Arena: {total_arena:.2f} MB")
        print(f"In-use: {in_use:.2f} MB")
        print(f"Utilization: {utilization:.2f}")
        print(len(self.arena))
        print(self.used_chunks)

    def malloc(self, id, size):
        node = self.free_chunks.get_best_fit(size)

        if node:
            start = node.key
            remaining_size = node.size - size
            if remaining_size > 0:
                self.free_chunks.insert(start + size, remaining_size)
            self.free_chunks.delete(node.key)
            self.used_chunks[id] = (start, size)
            self.total_allocated += size
        else:
            new_chunk_start = len(self.arena) * self.chunk_size
            self.arena.append([0] * self.chunk_size)
            self.free_chunks.insert(new_chunk_start + size, self.chunk_size - size)
            self.used_chunks[id] = (new_chunk_start, size)
            self.total_allocated += size

    def free(self, id):
        if id in self.used_chunks:
            start, size = self.used_chunks.pop(id)
            self.total_allocated -= size
            self.free_chunks.insert(start, size)
            # Consider merging adjacent free chunks for better utilization

if __name__ == "__main__":
    allocator = Allocator()
    start_time=time.time()
    # 테스트 케이스 추가
    test_requests = [
        ('a', 1, 1024),
        ('a', 2, 2048),
        ('a', 3, 3072),
        ('a', 4, 4096),
        ('f', 2),
        ('a', 5, 1536),
        ('f', 1),
        ('a', 6, 512),
        ('a', 7, 7168),
        ('f', 4),
        ('a', 8, 1024),
        ('a', 9, 4096),
        ('a', 10, 6144),
        ('a', 11, 2048),
        ('a', 12, 4096),
        ('a', 13, 2048),
        ('a', 14, 1024)
    ]

    for req in test_requests:
        if req[0] == 'a':
            allocator.malloc(req[1], req[2])
        elif req[0] == 'f':
            allocator.free(req[1])
        # print(req)
    allocator.print_stats()
