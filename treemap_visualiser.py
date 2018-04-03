"""Assignment 2: Treemap Visualiser

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code to run the treemap visualisation program.
It is responsible for initializing an instance of AbstractTree (using a
concrete subclass, of course), rendering it to the user using pygame,
and detecting user events like mouse clicks and key presses and responding
to them.
"""
import pygame
from tree_data import FileSystemTree
from population import PopulationTree


# Screen dimensions and coordinates
ORIGIN = (0, 0)
WIDTH = 1024
HEIGHT = 768
FONT_HEIGHT = 30                       # The height of the text display.
TREEMAP_HEIGHT = HEIGHT - FONT_HEIGHT  # The height of the treemap display.

# Font to use for the treemap program.
FONT_FAMILY = 'Consolas'


def run_visualisation(tree):
    """Display an interactive graphical display of the given tree's treemap.

    @type tree: AbstractTree
    @rtype: None
    """
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Render the initial display of the static treemap.
    render_display(screen, tree, '')

    # Start an event loop to respond to events.
    event_loop(screen, tree)


def render_display(screen, tree, text):
    """Render a treemap and text display to the given screen.

    Use the constants TREEMAP_HEIGHT and FONT_HEIGHT to divide the
    screen vertically into the treemap and text comments.

    @type screen: pygame.Surface
    @type tree: AbstractTree
    @type text: str
        The text to render.
    @rtype: None
    """
    # First, clear the screen
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                     (0, 0, WIDTH, HEIGHT))
    tree_map = tree.generate_treemap((0, 0, WIDTH, TREEMAP_HEIGHT))
    for rect in tree_map:
        pygame.draw.rect(screen, rect[1], rect[0])
    _render_text(screen, text)
    pygame.display.flip()
    # This must be called *after* all other pygame functions have run.


def _render_text(screen, text):
    """Render text at the bottom of the display.

        @type screen: pygame.Surface
        @type text: str
        @rtype: None
        """
    # The font we want to use
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    text_surface = font.render(text, 1, pygame.color.THECOLORS['white'])

    # Where to render the text_surface
    text_pos = (0, HEIGHT - FONT_HEIGHT + 4)
    screen.blit(text_surface, text_pos)


def event_loop(screen, tree):
    """Respond to events (mouse clicks, key presses) and update the display.

        Note that the event loop is an *infinite loop*: it continually waits for
        the next event, determines the event's type, and then updates the state
        of the visualisation or the tree itself, updating the display if
        necessary.
        This loop ends when the user closes the window.

        @type screen: pygame.Surface
        @type tree: AbstractTree
        @rtype: None
        """
    # We strongly recommend using a variable to keep track of the currently-
    # selected leaf (type AbstractTree | None).
    # But feel free to remove it, and/or add new variables, to help keep
    # track of the state of the program.
    selected_leaf = None

    while True:
        # Wait for an event
        event = pygame.event.poll()
        message = ''
        if event.type == pygame.QUIT:
            return
        elif event.type == pygame.MOUSEBUTTONUP:
            rect = 0, 0, WIDTH, TREEMAP_HEIGHT
            if event.button == 1:
                selected_leaf = left_click_event(selected_leaf, event, rect,
                                                 tree)
            if event.button == 3:
                selected_leaf = right_click_event(selected_leaf, event, rect,
                                                  tree)
        elif event.type == pygame.KEYUP:
            selected_leaf = key_press_event(selected_leaf, event)
        if selected_leaf:
            message = generate_display_message(selected_leaf)
        render_display(screen, tree, message)
        # Remember to call render_display if any data_sizes change,
        # as the treemap will change in this case.


def left_click_event(selected_leaf, event, rect, tree):
    """ generate an event for a left click on the pygame screen

    - When there is a left click on the screen, this function will search for a
    leaf corresponding to the coordinates of the click.
    - If the leaf is already selected, this function will return None
    - If the leaf is not selected,  this function will return the coresponding
    leaf.

    @type selected_leaf = AbstractTree
    @type event = pygame.event
    @type rect = (int, int, int, int)
    @type tree = AbstractTree
    @rtype = AbstracTree
    """
    if selected_leaf == tree.find_leaf(rect, event.pos):
        return None
    else:
        return tree.find_leaf(rect, event.pos)


def right_click_event(selected_leaf, event, rect, tree):
    """generate an event for right click on the pygame screen

    - When there is a right click on the screen, this function will search for a
    leaf corresponding to the coordinates of the click.
    - The corresponding leaf will be removed from the tree.
    - If the selected leaf is the same as the removed tree, selected leaf will
    be unselected

    @type selected_leaf = AbstractTree
    @type event = pygame.event
    @type rect = (int, int, int, int)
    @type tree = AbstractTree
    @rtype = AbstracTree
    """
    leaf_for_deletion = tree.find_leaf(rect, event.pos)
    leaf_for_deletion.delete_selected_leaf()
    if leaf_for_deletion == selected_leaf:
        selected_leaf = None
    return selected_leaf


def key_press_event(selected_leaf, event):
    """generate an event for key press

    - if key pressed is up button, the selected leaf will increase by 1% in size
    - if key pressed is down button, the selected leaf will decrease by 1% in
    size
    - if no leaf is selected, this function will do nothing

    @type selected_leaf = AbstractTree
    @type event = pygame.event
    @rtype = None | AbtstractTree
    """
    if selected_leaf:
        if event.key == pygame.K_UP:
            selected_leaf.mutate_size('increase')
        elif event.key == pygame.K_DOWN:
            selected_leaf.mutate_size('decrease')
        return selected_leaf


def generate_display_message(selected_leaf):
    """generate a display message for the selected leaf

    @type selected_leaf = AbstractTree
    @rtype = str
    """
    path = selected_leaf.get_separator()
    data_size = str(selected_leaf.data_size)
    return path + '     ' + '(' + data_size + ')'


def run_treemap_file_system(path):
    """Run a treemap visualisation for the given path's file structure.

    Precondition: <path> is a valid path to a file or folder.

    @type path: str
    @rtype: None
    """
    file_tree = FileSystemTree(path)
    run_visualisation(file_tree)


def run_treemap_population():
    """Run a treemap visualisation for World Bank population data.

    @rtype: None
    """
    pop_tree = PopulationTree(True)
    run_visualisation(pop_tree)


if __name__ == '__main__':
    import python_ta
    # Remember to change this to check_all when cleaning up your code.
    python_ta.check_all(config='pylintrc.txt')

    # To check your work for Tasks 1-4, try uncommenting the following function
    # call, with the '' replaced by a path like
    # 'C:\\Users\\David\\Documents\\csc148\\assignments' (Windows) or
    # '/Users/dianeh/Documents/courses/csc148/assignments' (OSX)
    run_treemap_file_system('TestFolder')
    # To check your work for Task 5, uncomment the following function call.
    # run_treemap_population()
