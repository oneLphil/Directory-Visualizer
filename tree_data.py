"""Assignment 2: Trees for Treemap

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
import os
from random import randint
import math


class AbstractTree:
    """A tree that is compatible with the treemap visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you adding and implementing
    new public *methods* for this interface.

    === Public Attributes ===
    @type data_size: int
        The total size of all leaves of this tree.
    @type colour: (int, int, int)
        The RGB colour value of the root of this tree.
        Note: only the colours of leaves will influence what the user sees.

    === Private Attributes ===
    @type _root: obj | None
        The root value of this tree, or None if this tree is empty.
    @type _subtrees: list[AbstractTree]
        The subtrees of this tree.
    @type _parent_tree: AbstractTree | None
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - colour's elements are in the range 0-255.

    - If _root is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - _subtrees IS allowed to contain empty subtrees (this makes deletion
      a bit easier).

    - if _parent_tree is not empty, then self is in _parent_tree._subtrees
    """
    def __init__(self, root, subtrees, data_size=0):
        """Initialize a new AbstractTree.

        If <subtrees> is empty, <data_size> is used to initialize this tree's
        data_size. Otherwise, the <data_size> parameter is ignored, and this
        tree's data_size is computed from the data_sizes of the subtrees.

        If <subtrees> is not empty, <data_size> should not be specified.

        This method sets the _parent_tree attribute for each subtree to self.

        A random colour is chosen for this tree.

        Precondition: if <root> is None, then <subtrees> is empty.

        @type self: AbstractTree
        @type root: object
        @type subtrees: list[AbstractTree]
        @type data_size: int
        @rtype: None
        >>> T = AbstractTree('Test', [], 15)
        >>> T._root
        'Test'
        >>> T._subtrees
        []
        >>> T.data_size
        15
        >>> T2 = AbstractTree('Test2', [T])
        >>> T2._subtrees[0]._root
        'Test'
        >>> T.data_size
        15
        """
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None
        self.data_size = data_size
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        for tree in subtrees:
            tree._parent_tree = self
            self.data_size += tree.data_size

    def is_empty(self):
        """Return True if this tree is empty.

        @type self: AbstractTree
        @rtype: bool
        """
        return self._root is None

    def generate_treemap(self, rect):
        """Run the treemap algorithm on this tree and return the rectangles.

        Each returned tuple contains a pygame rectangle and a colour:
        ((x, y, width, height), (r, g, b)).

        One tuple should be returned per non-empty leaf in this tree.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]

        >>> T1 = AbstractTree('Test1', [], 15)
        >>> rects = T1.generate_treemap((0, 0, 200, 100))
        >>> rects[0][0]
        (0, 0, 200, 100)
        >>> T2 = AbstractTree('Test2', [], 15)
        >>> T3 = AbstractTree('Test3', [], 15)
        >>> T = AbstractTree('Test', [T1, T2, T3])
        >>> rects = T.generate_treemap((0, 0, 100, 80))
        >>> rects[0][0]
        (0, 0, 33, 80)
        >>> rects[1][0]
        (33, 0, 33, 80)
        >>> rects[2][0]
        (66, 0, 34, 80)
        >>> rects = T.generate_treemap((0, 0, 100, 100))
        >>> rects[0][0]
        (0, 0, 100, 33)
        >>> rects[1][0]
        (0, 33, 100, 33)
        >>> rects[2][0]
        (0, 66, 100, 34)
        """
        # Read the handout carefully to help get started identifying base cases,
        # and the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # coordinates of a rectangle, as follows.
        # x, y, width, height = rect
        tree_map = []
        x, y, width, height = rect
        self.delete_empty_trees()
        if self.data_size == 0:
            return tree_map
        elif self._subtrees == []:
            tree_map.append((rect, self.colour))
            return tree_map
        elif width > height:
            accumulated_width = 0
            for subtree in self._subtrees:
                if subtree == self._subtrees[len(self._subtrees) - 1]:
                    sub_width = width - accumulated_width
                else:
                    sub_width = subtree.proportionate_tree(width)
                sub_rect = x, y, sub_width, height
                tree_map += (subtree.generate_treemap(sub_rect))
                x += sub_width
                accumulated_width += sub_width
        else:
            accumulated_height = 0
            for subtree in self._subtrees:
                if subtree == self._subtrees[len(self._subtrees) - 1]:
                    sub_height = height - accumulated_height
                else:
                    sub_height = subtree.proportionate_tree(height)
                sub_rect = x, y, width, sub_height
                tree_map += (subtree.generate_treemap(sub_rect))
                y += sub_height
                accumulated_height += sub_height
        return tree_map

    def find_leaf(self, rect, coordinations):
        """find the corresponding leaf given the coordinations and the pygame
         rectangle

         If the coordinations are outside of <rect>, this function will do nothing

        @type self = AbstractTree
        @type rect = (int, int, int, int)
            input is in pygame format: (x, y, width, height)
        @type coordinations = (int, int)
            coordinates where the <rect> was clicked
        @rtype = AbstractTree

        >>> T1 = AbstractTree('Test1', [], 15)
        >>> T2 = AbstractTree('Test2', [], 15)
        >>> T3 = AbstractTree('Test3', [], 15)
        >>> T = AbstractTree('Test', [T1, T2, T3])
        >>> leaf = T.find_leaf((0, 0, 200, 100), (100, 50))
        >>> leaf == T2
        True
        """
        x, y, width, height = rect
        coord_x, coord_y = coordinations
        if self._subtrees == []:
            return self
        elif width > height:
            accumulated_width = 0
            for subtree in self._subtrees:
                if subtree == self._subtrees[len(self._subtrees) - 1]:
                    sub_width = width - accumulated_width
                else:
                    sub_width = subtree.proportionate_tree(width)
                sub_rect = x, y, sub_width, height
                if x <= coord_x <= x + sub_width:
                    return subtree.find_leaf(sub_rect, coordinations)
                accumulated_width += sub_width
                x += sub_width
        elif height >= width:
            accumulated_height = 0
            for subtree in self._subtrees:
                if subtree == self._subtrees[len(self._subtrees) - 1]:
                    sub_height = height - accumulated_height
                else:
                    sub_height = subtree.proportionate_tree(height)
                sub_rect = x, y, width, sub_height
                if y <= coord_y <= y + sub_height:
                    return subtree.find_leaf(sub_rect, coordinations)
                accumulated_height += sub_height
                y += sub_height

    def proportionate_tree(self, parameter):
        """return the proportionated parameter of this tree's data size compared
        to the parent tree's data size given a paremeter representing the data
        size of the parent tree

        The returned parameter is rounded down to the nearest integer

        @type self = AbstractTree
        @type parameter = int
            parameter to be proportionated
        @rtype = int

        >>> T1 = AbstractTree('Test1', [], 15)
        >>> T2 = AbstractTree('Test2', [], 15)
        >>> T3 = AbstractTree('Test3', [], 15)
        >>> T = AbstractTree('Test', [T1, T2, T3])
        >>> T._subtrees[0].proportionate_tree(100)
        33
        """
        return int((self.data_size/self._parent_tree.data_size)*parameter)

    def mutate_size(self, parameter):
        """increase or decrease the data_size of this tree by 1% depending
        parameter and update all parent trees' data size

        parameter can only be 'increase' or 'decrease'
        the 1% mutation is rounded up to the nearest integer
        the data size of this tree cannot be decreased below 1

        @type self = AbstractTree
        @type parameter = str
            'increase' or 'decrease'
        @rtype = None

        >>> T1 = AbstractTree('Test1', [], 10)
        >>> T2 = AbstractTree('Test2', [], 10)
        >>> T3 = AbstractTree('Test3', [], 10)
        >>> T = AbstractTree('Test', [T1, T2, T3])
        >>> T._subtrees[0].mutate_size('increase')
        >>> T._subtrees[0].data_size
        11
        >>> T.data_size
        31
        >>> T._subtrees[0].mutate_size('decrease')
        >>> T._subtrees[0].data_size
        10
        >>> T.data_size
        30
        >>> T1 = AbstractTree('Test3', [], 1)
        >>> T = AbstractTree('Test', [T1])
        >>> T._subtrees[0].mutate_size('decrease')
        >>> T._subtrees[0].data_size
        1
        >>> T.data_size
        1
        """
        size_change = math.ceil(self.data_size*0.01)
        if parameter == 'increase':
            self.data_size += size_change
            self.update_data_size(size_change)
        elif parameter == 'decrease':
            if self.data_size > 1:
                self.data_size -= size_change
                self.update_data_size(-size_change)

    def delete_selected_leaf(self):
        """delete remove this leaf it's parent tree

        The parent trees of this tree will have data_size updated after deletion

        @type self = AbstractTree
        @rtype = None

        >>> T1 = AbstractTree('Test3', [], 1)
        >>> T = AbstractTree('Test', [T1])
        >>> T._subtrees[0].delete_selected_leaf()
        >>> T._subtrees
        []
        """
        if self._parent_tree:
            self._parent_tree.delete_child(self)
        else:
            self.data_size = 0

    def delete_child(self, child):
        """delete the subtree of this tree if input tree is in subtree

        If child is not in the <_subtrees> of this tree, the method will do
        nothing
        The parent trees of this tree will have data_size updated after deletion

        @type self = AbstractTree
        @type child = AbstractTree
            the subtree targeted for deletion
        @rtype = None
        >>> T1 = AbstractTree('Test3', [], 1)
        >>> T = AbstractTree('Test', [T1])
        >>> T.delete_child(T1)
        >>> T._subtrees
        []
        >>> T.data_size
        0
        """
        count = 0
        for subtree in self._subtrees:
            if subtree == child:
                data_size = self._subtrees[count].data_size
                subtree.update_data_size(-data_size)
                self._subtrees.pop(count)
                count = len(self._subtrees)
            count += 1

    def update_data_size(self, data_size):
        """update the data_size on parent trees of this tree

        <data_size> can be positive or negative.
        If data_size is positive all parent trees' data size will increase
        If data_size is negative all parent trees' data size will decrease


        @type self = AbstractTree
        @type data_size = int
            the data size to be updated in parent trees
        @rtype = None

        >>> T1 = AbstractTree('Test3', [], 1)
        >>> T = AbstractTree('Test', [T1])
        >>> T.data_size
        1
        >>> T1.update_data_size(10)
        >>> T.data_size
        11
        >>> T1.update_data_size(-1)
        >>> T.data_size
        10
        """
        if self._parent_tree is None:
            pass
        else:
            self._parent_tree.data_size += data_size
            self._parent_tree.update_data_size(data_size)

    def delete_empty_trees(self):
        """delete all empty subtrees in this tree

        @type self = AbstractTree
        @rtype = None

        >>> T1 = AbstractTree('Test1', [], 1)
        >>> T2 = AbstractTree('Test2', [], 0)
        >>> T3 = AbstractTree('Test3', [], 0)
        >>> T = AbstractTree('Test', [T1, T2, T3])
        >>> len(T._subtrees)
        3
        >>> T.delete_empty_trees()
        >>> len(T._subtrees)
        1
        """
        if self.data_size == 0:
            self.delete_selected_leaf()
        else:
            index = 0
            while index < len(self._subtrees):
                if self._subtrees[index].data_size == 0:
                    self._subtrees[index].delete_empty_trees()
                else:
                    index += 1

    def get_separator(self):
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.

        @type self: AbstractTree
        @rtype: str
        """
        raise NotImplementedError


class FileSystemTree(AbstractTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _root attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/David/csc148/assignments'

    The data_size attribute for regular files as simply the size of the file,
    as reported by os.path.getsize.
    """
    def __init__(self, path):
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.

        @type self: FileSystemTree
        @type path: str
        @rtype: None

        >>> T = FileSystemTree('TestFolder')
        >>> T.data_size
        11
        >>> T = FileSystemTree('TestFolder\\F1')
        >>> T.data_size
        3
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        if not os.path.isdir(path):
            AbstractTree.__init__(self, os.path.basename(path),
                                  [], os.path.getsize(path))
        else:
            subtrees = []
            for filename in os.listdir(path):
                subpath = os.path.join(path, filename)
                subtrees.append(FileSystemTree(subpath))
            AbstractTree.__init__(self, os.path.basename(path), subtrees)

    def get_separator(self):
        """return the path from the highest parent tree to the current leaf
         selected

         @type self = FileSystemTree
         @rtype = str

        >>> x = FileSystemTree('TestFolder')
        >>> subfolder = x._subtrees[0]
        >>> subfolder.get_separator()
        'TestFolder\\F1'
        >>> leaf = x._subtrees[0]._subtrees[0]
        >>> leaf.get_separator()
        'TestFolder\\F1\\T1.txt'
        """
        path = self._root
        if self._parent_tree is None:
            return path
        else:
            return os.path.join(self._parent_tree.get_separator(), path)

if __name__ == '__main__':
    import python_ta
    # Remember to change this to check_all when cleaning up your code.
    python_ta.check_all(config='pylintrc.txt')
