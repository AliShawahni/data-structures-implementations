#id1: 324293331
#name1: Muhammad Mansur
#username1: mansur1
#id2: 326683885
#name2: Ali Shawahne
#username2: shawahne






class AVLNode(object):
    """A class representing a node in an AVL tree."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1

    def is_real_node(self):
        """ Returns whether the node is not a virtual node """
        return self.key is not None

    def get_balance_factor(self):
        """ Returns the balance factor of the node """
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        return left_height - right_height


class AVLTree(object):
    """ A class implementing an AVL tree """

    def __init__(self):
        self.root = None
        self.max = None
        self.tree_size = 0
        
    def get_root(self):
        ''' return the root of the tree , comlexity : O(1)'''
        return self.root

    def size(self):
        ''' returns the size of the tree , comlexity : O(1)'''
        return self.tree_size
        
    def max_node(self):
        """ Returns the node with the largest key in the tree , comlexity : O(log(n)) """
        node = self.root
        while node and node.right and node.right.is_real_node():
            node = node.right
        return node
        
    def is_real_node(self):
        """Returns whether the node is not a virtual node , comlexity : O(1)"""
        return self.key is not None

    def get_height(self, node):
        """ Returns the height of a node , comlexity : O(1)"""
        if not node:
            return -1
        elif not node.is_real_node():
            return -1
        else:
           return node.height
        

    def get_balance_factor(self, node):
        """ Returns the balance factor of a node , comlexity : O(1) """
        return self.get_height(node.left) - self.get_height(node.right) if node else 0
    

    def update_height(self, node):
        """ Updates the height of a node based on its children , comlexity : O(1) """
        if not node or not node.is_real_node():
            return None
            
        # Get heights of children
        left_height = self.get_height(node.left)
        right_height = self.get_height(node.right)
        
        # Update node height
        node.height = max(left_height, right_height) + 1
    

    def rotate_left(self, node):
        """ Performs a left rotation around the given node , comlexity : O(1)"""
        new_root = node.right
        node.right = new_root.left
        
        # Update parent pointers for all nodes involved
        if node.right:  # This handles both real and virtual nodes
            node.right.parent = node
        
        new_root.parent = node.parent
        if not node.parent:  # If node is root
            self.root = new_root
        elif node == node.parent.left:
            node.parent.left = new_root
        else:
            node.parent.right = new_root
        
        new_root.left = node
        node.parent = new_root
        
        # Update heights
        self.update_height(node)
        self.update_height(new_root)

    def rotate_right(self, node):
        """ Performs a right rotation around the given node , comlexity : O(1)"""
        new_root = node.left
        node.left = new_root.right
        
        # Update parent pointers for all nodes involved
        if node.left:  # This handles both real and virtual nodes
            node.left.parent = node
            
        new_root.parent = node.parent
        if not node.parent:  # If node is root
            self.root = new_root
        elif node == node.parent.right:
            node.parent.right = new_root
        else:
            node.parent.left = new_root
        
        new_root.right = node
        node.parent = new_root
        
        # Update heights
        self.update_height(node)
        self.update_height(new_root)


    def create_virtual_node(self):
        """Creates and returns a virtual node."""
        virtual_node = AVLNode(None, None)
        virtual_node.height = -1
        return virtual_node

    
    def insert(self, key, value):
        """ Inserts a new node with the given key and value and return :
        (1) pointer of the node , (2) the number of edges we passed by, (3) the number of promotions (case 1 in rebalancing)
            , comlexity : O(log(n)) """
        
        new_node = AVLNode(key, value)
        if not self.root:  # If the tree is empty
            self.root = new_node
            self.root.left = self.create_virtual_node()
            self.root.right = self.create_virtual_node()
            self.root.left.parent = self.root
            self.root.right.parent = self.root
            self.root.height = 0  # Set initial height to 0 for leaf node
            self.tree_size += 1
            self.max = self.max_node()
            return new_node, 0, 0

        current = self.root
        parent = None
        edges = 0

        # Find insertion point
        while current and current.is_real_node():
            parent = current
            edges += 1
            if key < current.key:
                current = current.left
            else:
                current = current.right

        # Set up new node
        new_node.left = self.create_virtual_node()
        new_node.right = self.create_virtual_node()
        new_node.left.parent = new_node
        new_node.right.parent = new_node
        new_node.parent = parent
        new_node.height = 0  # Set initial height to 0 for leaf node

        # Link parent to new node
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self.tree_size += 1
        promoted_count = self.rebalance(new_node)

        self.max = self.max_node()

        return new_node, edges, promoted_count



    def rebalance(self, node):
        """ Rebalances the tree starting from the given node and returns the number of nodes whose height was promoted (case 1)
               , comlexity : O(log(n))"""
        
        promoted_count = 0
        current = node        
        
        while current:
            old_height = current.height
            
            # Update height
            self.update_height(current)
            
                
            # Get balance factor
            balance = self.get_balance_factor(current)
            
            # Left heavy
            if balance > 1:
                if self.get_balance_factor(current.left) < 0:# Left-Right case
                        self.rotate_left(current.left)
                self.rotate_right(current)
                
            # Right heavy
            elif balance < -1:
                if self.get_balance_factor(current.right) > 0:  # Right-Left case
                        self.rotate_right(current.right)
                self.rotate_left(current)
                
            # Check if height was promoted
            elif current.height > old_height:
                promoted_count += 1
                
            current = current.parent
            
        return promoted_count
            
    

    def delete(self,node):
            """ Deletes the given node from the AVL tree , comlexity : O(log(n)) """
            if not node:
                return True
            if not node.is_real_node():
                return True
           
            #node is a leaf
            if not node.left.is_real_node() and not node.right.is_real_node():
                if node == self.root:
                    self.root = None
                    self.tree_size = 0
                    return True
                else:
                    if node.parent.left == node:
                        node.parent.left = self.create_virtual_node()
                    else:
                        node.parent.right = self.create_virtual_node()
                self.rebalance(node.parent)
                self.tree_size -=1
                return True
            #node has one child
            if not node.left.is_real_node() or not node.right.is_real_node():
                    child = node.left if node.left.is_real_node() else node.right  # The single child

                    if node == self.root:
                        self.root = child
                        
                    else:
                        if node.parent.left == node:
                            node.parent.left = child
                        else:
                            node.parent.right = child
                    child.parent = node.parent

                    self.rebalance(child)
                    self.tree_size -=1
                    self.max = self.max_node()
                    return True

            #node has two children
            successor = self.get_min(node.right)
            node.key , node.value = successor.key , successor.value

            current = successor
            
            if not successor.right.is_real_node():
                #successor is a leaf
                if successor.parent.left == successor:
                    successor.parent.left = self.create_virtual_node()
                else:
                    successor.parent.right = self.create_virtual_node()
            else:
                #successor has a child (right one)
                child = successor.right
                if successor.parent.left == successor:
                    successor.parent.left = child
                else:
                    successor.parent.right = child
                child.parent = successor.parent
            
            # Rebalance starting from the successor's parent
            self.rebalance(current.parent)
            self.tree_size -= 1
            self.max = self.max_node()

                   
            

    def get_min(self, node):
        """ Returns the node with the smallest key in the subtree , comlexity : O(log(n))"""
        while node and node.is_real_node() and node.left.is_real_node():
            node = node.left
        return node

    def search(self, key):
        """ Searches for a node by its key , comlexity : O(log(n)) """
        node = self.root
        steps = 0
        while node and node.is_real_node():
            steps += 1
            if key == node.key:
                return node, steps
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None, steps

    def avl_to_array(self):
        ''' convert a tree into in order array , comlexity : O(n)'''
        result = []
        
         
        def in_order_traversal(node):
            'recursivly build the array , comlexity : O(n)'
            
            if not node or not node.is_real_node():
                      return None
            in_order_traversal(node.left)
            result.append((node.key, node.value))
            in_order_traversal(node.right)
        
        in_order_traversal(self.get_root())
        return result
    
 
    def split(self, x):
        ''' split the current tree using a node (x) into two AVL trees , comlexity : O(n)'''
        if x is None:
            return self, AVLTree()
        if not self.root:
            return AVLTree(), AVLTree()

        # Initialize two new trees
        t1 = AVLTree()
        t2 = AVLTree()


        # Assign x.left to t1 and x.right to t2
        if x.left and x.left.is_real_node():
            t1.root = x.left
            t1.root.parent = None
            t1.tree_size = self.get_tree_size_subtree(x.left)

        if x.right and x.right.is_real_node():
            t2.root = x.right
            t2.root.parent = None
            t2.tree_size = self.get_tree_size_subtree(x.right)

        # Traverse up from x to split the parents
        child = x
        current = x.parent
        cnt = 0
        

        while current is not None:
            
            if cnt == 0:
                cnt+=1
                
            if current.key > child.key:  # Current node belongs to t2
                tmp = t2.root
                t2.root = current
                if not tmp or not tmp.is_real_node():
                    t2.root.left = t2.create_virtual_node()
                else:
                    t2.root.left = tmp


                t2.tree_size += 1 + (self.get_tree_size_subtree(current.right) if current.right else 0)
                

            else:  # Current node belongs to t1
                
                tmp = t1.root
                t1.root = current
                if not tmp or not tmp.is_real_node():
                    t1.root.right = t1.create_virtual_node()
                else:
                    t1.root.right = tmp

                t1.tree_size += 1 + (self.get_tree_size_subtree(current.left) if current.left else 0)
                               

            # Move up the tree
            child = current
            current = current.parent

            if t1.root:
                    tmp1 = t1.root.parent
                    t1.root.parent = None
                    t1.rebalance(t1.root)
                    t1.root.parent = tmp1


            if t2.root:
                    tmp2 = t2.root.parent
                    t2.root.parent = None
                    t2.rebalance(t2.root)
                    t2.root.parent = tmp2

            #we can attatch the node from the original tree
            if cnt == 1:
                    x.key = None
                    x.value = None
                    x.height = -1
                    

        if t1.root:
                t1.root.parent = None
        if t2.root:
                t2.root.parent = None
                
        t1.max = t1.max_node()
        t2.max = t2.max_node()

        return t1, t2


    def get_tree_size_subtree(self, node):
        """Calculates the tree_size of the subtree rooted at the given node and updates the height , comlexity : O(n)"""
        if not node or not node.is_real_node():
            return 0

        left_tree_size = self.get_tree_size_subtree(node.left) if node.left else 0
        right_tree_size = self.get_tree_size_subtree(node.right) if node.right else 0

        # Update the height of the current node
        node.height = max(
            node.left.height if node.left and node.left.is_real_node() else -1,
            node.right.height if node.right and node.right.is_real_node() else -1,
        ) + 1

        # Return the total tree_size of the subtree
        return left_tree_size + right_tree_size + 1



    
    def join(self,t,k,v):
        ''' join self with given tree using the node (k,v), comlexity : O(log(n)) '''
        
        #both trees are empty
        if not self.root and not t.root:
            self.insert(k,v)
            self.max = self.max_node()
            return self.root
        
        #self is an empty tree
        if not self.root:
            t.insert(k,v)
            self.root = t.root
            self.tree_size = t.tree_size
            self.max = self.max_node()
            return self.root
        
        #t is an empty tree
        if not t.root:
            self.insert(k,v)
            self.max = self.max_node()
            return self.root
        
        ''' what if both trees have the same height'''
        
        #compare by height
        taller_tree = self if self.root.height > t.root.height else t
        shorter_tree = self if self.root.height < t.root.height else t
        
        #compare by keys
        bigger_tree = self if self.root.key > t.root.key else t
        smaller_tree = self if self.root.key < t.root.key else t

        ''' we have two cases
            (1) taller_tree is bigger_tree
            (2) taller_tree is smaller_tree '''
        #we get the same size in the two cases
        new_tree_size = t.tree_size + self.tree_size + 1

        #first case
        if taller_tree is bigger_tree:
            h = shorter_tree.root.height
            current = taller_tree.root

            while current.height > h:
                current = current.left

            new_node = AVLNode(k,v)
            parent = current.parent

            current.parent = new_node
            new_node.right = current
            new_node.height = h+1
            parent.left = new_node
            new_node.parent = parent
            shorter_tree.root.parent = new_node
            new_node.left = shorter_tree.root

            self.root = taller_tree.root
            self.tree_size = new_tree_size
            self.rebalance(parent)
            self.max = self.max_node()
            return self.root
        
        
        #second case
        else:
            h = shorter_tree.root.height
            current = taller_tree.root

            while current.height > h:
                current = current.right

            new_node = AVLNode(k,v)
            parent = current.parent

            current.parent = new_node
            new_node.left = current
            new_node.height = h+1
            parent.right = new_node
            new_node.parent = parent
            shorter_tree.root.parent = new_node
            new_node.right = shorter_tree.root
            
            self.root = taller_tree.root
            self.tree_size = new_tree_size
            self.rebalance(parent)
            self.max = self.max_node()
        
            return self.root


    
    def finger_insert(self, k, v):
        ''' finger insert starting from max node '''
        current = self.max
        edges = 0

        if not current:
            self.root = AVLNode(k, v)
            self.root.height = 0
            self.root.left = self.create_virtual_node()
            self.root.right = self.create_virtual_node()
            self.root.left.parent = self.root
            self.root.right.parent = self.root
            self.tree_size += 1
            self.max = self.max_node()
            return self.root, edges, 0

        # For inserting value larger than max, we only need one edge
        if k > current.key:
            edges = 1
            parent = current
        else:
            # If we need to go up, start counting edges
            while current and current.parent and current.parent.key > k:
                current = current.parent
                edges += 1
            
            parent = current
            while current and current.is_real_node():
                parent = current
                
                if k < current.key:
                    if not current.left.is_real_node():
                        break
                    current = current.left
                    edges += 1
                else:
                    if not current.right.is_real_node():
                        break
                    current = current.right
                    edges += 1

        new_node = AVLNode(k, v)
        new_node.parent = parent
        new_node.left = self.create_virtual_node()
        new_node.right = self.create_virtual_node()
        new_node.left.parent = new_node
        new_node.right.parent = new_node

        if parent.key > k:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self.tree_size += 1
        self.max = self.max_node()

        promotions = self.rebalance(new_node)

        return new_node, edges, promotions-1
        
    
    def finger_search(self, k):
        '''
        Finger search starting from the max node.
        Returns: (node, number_of_operations) or (None, number_of_operations) if not found.
        '''
        if not self.root:  # Check if the tree is empty
            return None, 0

        current = self.max # Start at the max node
        e = 0

        # Move upwards to find the first ancestor with a key <= k
        while current and current.parent and current.parent.key >= k:
            current = current.parent
            e += 1

        # Check if the root is the target key (handles the case when the root is the desired key)
        if current == self.root and current.key == k:
            return current, e+1

        # Perform binary search starting from this node
        while current and current.is_real_node():
            if current.key == k:
                return current, e+1
            elif current.key > k:
                current = current.left
            else:
                current = current.right
            e += 1

        # If the key is not found, return None
        return None, e





