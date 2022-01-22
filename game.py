
import arcade
import os

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850
SCREEN_TITLE = "MODULE 1 Platformer Game"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 150

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 14
GRAVITY = 0.6


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """
        Initializer
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.winner = False
        self.loser = False

        #Sounds
        self.game_over_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")

        # Sprite lists
        self.wall_list = None
        self.enemy_list = None
        self.player_list = None
        self.coin_list = None

        # Set up the player
        self.player_sprite = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.game_over = False

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Draw bottom floor
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x
            self.wall_list.append(wall)

        # Function for drawing the platforms
        def draw_platform(bottom, left):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
            wall.bottom = bottom
            wall.left = left
            self.wall_list.append(wall)

        # Positioning of the platforms
        for x in range(SPRITE_SIZE * 3, SPRITE_SIZE * 8, SPRITE_SIZE):
            draw_platform((SPRITE_SIZE * 3), x)
            draw_platform((SPRITE_SIZE * 6), (x - 350))
            draw_platform((SPRITE_SIZE * 6), (x + 350))
            draw_platform((SPRITE_SIZE * 9), x-50)

        # Function for drawing the coins    
        def draw_coin(bottom, left):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", SPRITE_SCALING * 0.75)
            coin.bottom = bottom
            coin.left = left
            self.coin_list.append(coin)

        # Position of the coins
        draw_coin(SPRITE_SIZE * 2, 660)
        draw_coin(SPRITE_SIZE * 2, 340)
        draw_coin(SPRITE_SIZE * 4, 340)
        draw_coin(SPRITE_SIZE * 7, 750)
        draw_coin(SPRITE_SIZE * 7, 25)
        draw_coin(SPRITE_SIZE * 7, 125)
        draw_coin(SPRITE_SIZE * 10, 290)
        draw_coin(SPRITE_SIZE * 12.5, 290)


        # Draw the crates    
        def draw_crate(bottom, left):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
            wall.bottom = bottom
            wall.left = left
            self.wall_list.append(wall)

        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE * 5):
            draw_crate((SPRITE_SIZE), x)
        draw_crate((SPRITE_SIZE * 5), 325)
        draw_crate((SPRITE_SIZE * 8), 600)


        # -- Draw enemies on the ground
        def draw_enemy(bottom, left, velocity, bound_left, bound_right):
            enemy = arcade.Sprite(":resources:images/enemies/wormGreen.png", SPRITE_SCALING)

            enemy.bottom = bottom
            enemy.left = left
            enemy.change_x = velocity
            enemy.boundary_right = bound_right
            enemy.boundary_left = bound_left
            enemy.change_x = velocity
            self.enemy_list.append(enemy)

        draw_enemy((SPRITE_SIZE),(SPRITE_SIZE * 7), (2), (SPRITE_SIZE * 3), (SPRITE_SIZE * 10))
        draw_enemy((SPRITE_SIZE), (SPRITE_SIZE), 2, (SPRITE_SIZE), (SPRITE_SIZE * 10))
        draw_enemy((SPRITE_SIZE * 4), (SPRITE_SIZE * 4), (3), (SPRITE_SIZE * 3), (SPRITE_SIZE *8))
        draw_enemy((SPRITE_SIZE * 7),(SPRITE_SIZE * 9), (4), (SPRITE_SIZE * 9), (SPRITE_SIZE *13))
        draw_enemy((SPRITE_SIZE * 7),(SPRITE_SIZE), (0), (SPRITE_SIZE - 20), (SPRITE_SIZE *3))
        draw_enemy((SPRITE_SIZE * 10),(SPRITE_SIZE * 4), (5), (SPRITE_SIZE * 2), (SPRITE_SIZE * 7))


        # -- Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           SPRITE_SCALING)
        self.player_list.append(self.player_sprite)

        # Starting position of the player
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 270

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()
        self.coin_list.draw()

        if self.winner:
            winner = f"You have won!"
            arcade.draw_text(winner, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150,
                             arcade.color.AO, 80,
                             anchor_x="center")
        elif self.loser:
            loser = "You lost!"
            arcade.draw_text(loser, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150,
                             arcade.color.RED, 100,
                             anchor_x="center")

    def on_key_press(self, key, modifiers):
        """
        Called whenever the mouse moves.
        """
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.jump_sound.play()
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Update the player based on the physics engine
        if not self.game_over:
            # Move the enemies
            self.enemy_list.update()

            # Check each enemy
            for enemy in self.enemy_list:
                # If the enemy hit a wall, reverse
                if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                    enemy.change_x *= -1
                # If the enemy hit the left boundary, reverse
                elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                    enemy.change_x *= -1
                # If the enemy hit the right boundary, reverse
                elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                    enemy.change_x *= -1

            # Update the player using the physics engine
            self.physics_engine.update()

            # See if the player hit a worm. If so, game over.
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
                self.game_over_sound.play()
                self.game_over = True
                self.loser = True
            
            coin_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
                
            for coin in coin_collision_list:
                self.coin_list.remove(coin)
                self.collect_coin_sound.play()
            
            if len(self.coin_list) <= 0: 
                self.game_over = True
                self.winner = True



def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()