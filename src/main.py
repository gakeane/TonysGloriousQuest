
import arcade
import os


SPRITE_SCALING = 0.5

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Better Move Sprite with Keyboard Example"

MOVEMENT_SPEED = 5


class Player(arcade.Sprite):

    def __init__(self, sprite_image, sprite_scale, start_pos_x, start_pos_y):
        """ """

        super().__init__(sprite_image, sprite_scale)

        self.center_x = start_pos_x
        self.center_y = start_pos_y

    def update(self):
        """ updates the posistion of the character on the screen """

        self.center_x += self.change_x
        self.center_y += self.change_y

        self.check_boundaries()

    # move to server
    def check_boundaries(self):
        """ Ensures player does not go off the screen """

        # Don't go off the left
        if self.left < 0:
            self.left = 0

        # Don't go off the right
        if self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        # Don't go off the bottom
        if self.bottom < 0:
            self.bottom = 0

        # Don't go off the top
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1



class Keyboard:
    """ """

    def __init__(self):
        """ """

        self.keys = dict()
        self.keys[arcade.key.UP] = False
        self.keys[arcade.key.DOWN] = False
        self.keys[arcade.key.LEFT] = False
        self.keys[arcade.key.RIGHT] = False



class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # class for handling whic keys have been pressed
        self.keyboard = Keyboard()

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(":resources:images/animated_characters/male_person/malePerson_idle.png", SPRITE_SCALING, 25, 25)
        self.player_list.append(self.player_sprite)


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Here we pull from the socket to get the updated information for what we display
        # We also send data to the game server based on what was pressed
        # The game server tracks what has changed, It should be given inputs and send back posistions

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.keyboard.keys[arcade.key.UP] and not self.keyboard.keys[arcade.key.DOWN]:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.keyboard.keys[arcade.key.DOWN] and not self.keyboard.keys[arcade.key.UP]:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.keyboard.keys[arcade.key.LEFT] and not self.keyboard.keys[arcade.key.RIGHT]:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.keyboard.keys[arcade.key.RIGHT] and not self.keyboard.keys[arcade.key.LEFT]:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # Call update to move the sprite
        # If using a physics engine, call update on it instead of the sprite
        # list.
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.ESCAPE:
            exit(0)

        self.keyboard.keys[key] = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        self.keyboard.keys[key] = False


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()



if __name__ == '__main__':
    main()
