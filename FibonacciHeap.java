
//id1: 324293331
//name1: Muhammad Mansur
//username1: mansur1
//id2: 326683885
//name2: Ali Shawahne
//username2: shawahne


/**
 * FibonacciHeap
 *
 * An implementation of Fibonacci heap over positive integers.
 *
 */
public class FibonacciHeap
{
	
	public HeapNode min;
	private int size;
	private int totalLinks;
	private int totalCuts;
	private int numtrees;
	
	
	/**
	 *
	 * Constructor to initialize an empty heap.
	 *
	 */
	//complexity: O(1)
	public FibonacciHeap()
	{
		this.min = null;
		this.size = 0;
		this.totalCuts = 0;
		this.totalLinks = 0;
		
	}

	/**
	 * 
	 *
	 * Insert a node into the roots list.
	 *
	 */
	//complexity: O(1)
	private void addtorootlist(HeapNode node) {
		if (min == null) {
			node.next = node.prev = node;
			min = node;
		}
		else {
			HeapNode next0 = min.next;
			min.next = node;
			node.next = next0;
			next0.prev = node;
			node.prev = min;

		}
	
	}
	
	/**
	 * 
	 * pre: key > 0
	 *
	 * Insert (key,info) into the heap and return the newly generated HeapNode.
	 *
	 */
	//complexity: O(1)
	public HeapNode insert(int key, String info) 
	{    
		HeapNode new_node = new HeapNode(key,info);
		if (this.min == null) {
			this.min = new_node;
		}
		else {
			addtorootlist(new_node);
			if (new_node.key < this.min.key) {this.min = new_node;}
		
		}
		size++;
		this.numtrees++;	
		return new_node;
	}

	/**
	 * 
	 * Return the minimal HeapNode, null if empty.
	 *
	 */
	//complexity: O(1)
	public HeapNode findMin()
	{
		return this.min;
	}

	/**
	 * 
	 * returns the minimal HeapNode in the subtree, null if empty. 
	 *
	 */
	//complexity: O(n)
	public HeapNode find_min_in_sequence(HeapNode node)
	{
		if (node == null)
			return null;
		HeapNode min_node = node;
		HeapNode curr_node = node.next;
		while(curr_node != node)
		{
			if (curr_node.key < min_node.key)
				min_node = curr_node;
			curr_node = curr_node.next;
		}
		return min_node;
	}
	
	/**
	 * 
	 * updates the parent fields of the childs of the minimal node to point to null, when the min is going to be deleted 
	 *
	 */
	//complexity: O(logn)
	public void update_deleted_node_childs()
	{
		if (this.min.child == null)
			return;
		HeapNode currChild = this.min.child;
		currChild.parent = null;
		currChild = currChild.next;
		while(currChild != this.min.child)
		{
			currChild.parent = null;
			currChild = currChild.next;
		}
		return;
	}
	
	//links two trees with the same degree
	//complexity: O(1)
	public HeapNode link(HeapNode root1, HeapNode root2)
	{
		//make sure that root1.key > root2.key and handle the case where both nodes have the same key and one of them is the heap min
		if (root1.key < root2.key || this.min == root1)
		{
			HeapNode temp = root2;
			root2 = root1;
			root1 = temp;
		}
		root2.next = root2;
		root2.prev = root2;
		root2.parent = null;
		root2.rank += 1;
		root1.parent = root2;
		if (root2.child == null)
		{
			root2.child = root1;
		}
		else
		{
			root1.next = root2.child;
			root1.prev = root2.child.prev;
			root2.child.prev.next = root1;
			root2.child.prev = root1;
		}
		this.numtrees -= 1;
		this.totalLinks += 1;
		return root2;	
	}
	
	// consolidate\successively link trees with same degree,
	// following the algorithm presented in the lecture
	// complexity: WC- O(n) , amortized- O(logn)
	public void consolidate()
	{
		int max_rank = 1;
		double x = 1;
		while (x <= this.size())
		{
			x = x * 1.5;
			max_rank += 1;
		}
		HeapNode[] roots_array = new HeapNode[max_rank + 1];
		for (int i = 0; i < roots_array.length; i++)
			roots_array[i] = null;
		HeapNode first_sup_tree = this.min;
		HeapNode curr_sup_tree = first_sup_tree;
		HeapNode curr_sup_tree_next = curr_sup_tree.next;
		curr_sup_tree.prev = curr_sup_tree.next = curr_sup_tree;
		roots_array[curr_sup_tree.rank] = curr_sup_tree;
		curr_sup_tree = curr_sup_tree_next;
		while (curr_sup_tree != first_sup_tree)
		{
			int rank = curr_sup_tree.rank;
			HeapNode linked_subtree = curr_sup_tree;
			HeapNode next_sup_tree = curr_sup_tree.next;
			curr_sup_tree.prev = curr_sup_tree.next = curr_sup_tree;
			while (roots_array[rank] != null)
			{
				linked_subtree = link(roots_array[rank], linked_subtree);
				roots_array[rank] = null;
				rank += 1;
			}
			roots_array[rank] = linked_subtree;
			curr_sup_tree = next_sup_tree;
		}
		//find the first and the last subtrees in the array
		HeapNode currNode = null, lastNode = null;
		int first_node_index = -1, last_node_index = roots_array.length;
		for (int i = 0; i < roots_array.length; i++)
			if (roots_array[i] != null)
			{
				currNode = roots_array[i];
				first_node_index = i;
				break;
			}
		for (int i = roots_array.length - 1; i >= 0; i--)
			if (roots_array[i] != null)
			{
				lastNode = roots_array[i];
				last_node_index = i;
				break;
			}
		currNode.prev = lastNode;
		lastNode.next = currNode;
		for (int i = first_node_index + 1; i < roots_array.length; i++)
		{
			if (roots_array[i] != null)
			{
				currNode.next = roots_array[i];
				roots_array[i].prev = currNode;
				currNode = roots_array[i];
			}
		}
		return;
	}
	
	/**
	 * 
	 * Delete the minimal item
	 *
	 */
	// complexity: WC- O(n) , amortized- O(logn)
	public void deleteMin()
	{
		if (this.size() == 0 && this.min == null)
		{
			return;
		}
		HeapNode min_node = this.min;
		this.totalCuts += min_node.rank;
		HeapNode new_min_node;
		this.size -= 1;
		this.numtrees = this.numtrees + min_node.rank -1;
		if (min_node.next == min_node && min_node.child == null)
		{
			this.numtrees = 0;
			this.min = null;
			return;
		}
		this.update_deleted_node_childs();
		if (min_node.next != min_node)
		{
			min_node.prev.next = min_node.next;
			min_node.next.prev = min_node.prev;
			new_min_node = find_min_in_sequence(min_node.next);
			if (min_node.child != null)
			{
				HeapNode temp_new_min_node = find_min_in_sequence(min_node.child);
				if (temp_new_min_node.key < new_min_node.key)
					new_min_node = temp_new_min_node;
				min_node.prev.next = min_node.child;
				min_node.child.prev.next = min_node.next;
				min_node.next.prev = min_node.child.prev;
				min_node.child.prev = min_node.prev;
			}
		}
		else
		{
			new_min_node = find_min_in_sequence(min_node.child);
		}
		this.min = new_min_node;
		consolidate();
	}

	/**
	 * 
	 * pre: 0<diff<x.key
	 * 
	 * Decrease the key of x by diff and fix the heap. 
	 * 
	 */
	// complexity: WC- O(n) , amortized- O(1)
	public void decreaseKey(HeapNode x, int diff) {
		if (x == null) {return;}
	    x.key -= diff;

	    // If x violates heap property, perform a cut
	    if (x.parent != null && x.key < x.parent.key) {
	        cut(x);
	    }
	    
	    // Update min node if necessary
	    if (x.key < min.key) {
	        min = x;
	    }
	}
	
	
	
	// complexity: WC- O(n) , amortized- O(1)
	public void cut(HeapNode x) {
		if (x.parent == null)
			return;
	    HeapNode parent = x.parent;
	    // Detach x from parent's child list
	    if (x.next == x) { // x is the only child
	        parent.child = null;
	    }
	    else { // x has siblings
	        x.next.prev = x.prev;
	        x.prev.next = x.next;

	        if (parent.child == x) {
	            parent.child = x.next;
	        }
	    }

	    x.parent = null;
	    parent.rank--; // Decrement parent's rank
	    // Handle marking and cascading cuts
	    if (parent.mark && parent.parent != null) {
	        cut(parent); // Cascading cut
	    } else {
	        parent.mark = true; // Mark parent if it was not already marked
	    }

	    // Add x to the root list
	    x.prev = x;
	    x.next = x;
	    x.mark = false; // Reset mark
	    addtorootlist(x);
	    
        this.numtrees ++;
	    totalCuts++; // Increment total cuts
	}
		

	/**
	 * 
	 * Delete the x from the heap.
	 *
	 */
	// complexity: WC- O(n) , amortized- O(logn)
	public void delete(HeapNode x) 
	{    
		if (x == null) {return;}
		if (x == min) {deleteMin();}
		else {
			this.totalCuts += x.rank;
			size--;
			if (x.parent == null && x.child == null) {
				x.prev.next = x.next;
				x.next.prev = x.prev;
				x.prev = x.next = null;
				this.numtrees--;
					}
			//x is a root
			else {
				if (x.parent == null) {
					HeapNode first = x.child;
					HeapNode last = first.prev;
					
					x.child = null;
					x.prev.next = first;
					first.prev = x.prev;
					
					x.next.prev = last;
					last.next = x.next;
					x.prev = x.next = null;
			
					this.numtrees = this.numtrees + x.rank - 1;
				}
				else {
					if (x.child == null) {
						cut(x);
						x.prev.next = x.next;
						x.next.prev = x.prev;
						this.numtrees--;
						}
					else {
						cut(x);
						HeapNode first = x.child;
						HeapNode last = first.prev;
						
						x.child = null;
						x.prev.next = first;
						first.prev = x.prev;
						
						x.next.prev = last;
						last.next = x.next;
						x.prev = x.next = null;
						
						this.numtrees = this.numtrees + x.rank - 1;
						
				}}
			}
		}	
	}


	/**
	 * 
	 * Return the total number of links.
	 * 
	 */
	// complexity: O(1)
	public int totalLinks()
	{
		return this.totalLinks; 
	}


	/**
	 * 
	 * Return the total number of cuts.
	 * 
	 */
	// complexity: O(1)
	public int totalCuts()
	{
		return this.totalCuts;
	}


	/**
	 * 
	 * Meld the heap with heap2
	 *
	 */
	// complexity: O(1)
	public void meld(FibonacciHeap heap2)
	{
		/* if heap2 is empty we do not change anything */
		if (heap2 == null || heap2.min == null) {return;}
		
		/* the current heap is empty */
		if (this.min == null) {this.min = heap2.min;}
		
		/* both heaps are not empty therefore we meld them */
		else {
			HeapNode tmp1 = this.min.next;
			HeapNode tmp2 = heap2.min.next;
			
			this.min.next = tmp2;
			heap2.min.next = tmp1;
			
			tmp1.prev = heap2.min;
			tmp2.prev = this.min;
			
			if(this.min.key > heap2.min.key) {this.min = heap2.min;}	
			
		}
		this.totalCuts = this.totalCuts + heap2.totalCuts;
		this.totalLinks = this.totalLinks + heap2.totalLinks;
		this.size = this.size + heap2.size;	
		this.numtrees += heap2.numtrees;
		
	}

	/**
	 * 
	 * Return the number of elements in the heap
	 *   
	 */
	// complexity: O(1)
	public int size()
	{
		return this.size;
	}


	/**
	 * 
	 * Return the number of trees in the heap.
	 * 
	 */
	// complexity: O(1)
	public int numTrees()
	{
		return this.numtrees;
	}
	
	
	/**
	 * Class implementing a node in a Fibonacci Heap.
	 *  
	 */
	public static class HeapNode{
		public int key;
		public String info;
		public HeapNode child;
		public HeapNode next;
		public HeapNode prev;
		public HeapNode parent;
		public int rank;
		public boolean mark;
		
		/**
		 *
		 * Constructor to initialize a node with (key, info).
		 *
		 */
		// complexity: O(1)
		public 	HeapNode(int key, String info) {
			this.key = key;
			this.info = info;
			this.child = null;
			this.next = this;
			this.prev = this;
			this.parent = null;
			this.rank = 0;
			this.mark = false;
		}
		
	}
	
}