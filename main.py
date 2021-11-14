import tkinter as tk


class GameObject(object):  # game object class defines game objects
    def __init__(self, canvas, item):  # initializes game object
        self.canvas = canvas  # canvas is the canvas on which the game object is drawn
        self.item = item  # item is the item on the canvas that represents the game object

    def get_position(self):  # returns the position of the game object
        return self.canvas.coords(self.item)  # defines a ball object

    def move(self, x, y):  # moves the game object to a new position
        self.canvas.move(self.item, x, y)  # moves the item on the canvas

    def delete(self):  # deletes the game object
        self.canvas.delete(self.item)  # deletes the item on the canvas


class Ball(GameObject):  # Ball game object class
    def __init__(self, canvas, x, y):  # initializes the ball
        self.radius = 10  # radius of the ball
        self.direction = [1, -1]  # direction of the ball
        self.speed = 10  # speed of the ball
        item = canvas.create_oval(x-self.radius, y-self.radius,
                                  x+self.radius, y+self.radius,
                                  fill='white')  # creates the ball
        super(Ball, self).__init__(canvas, item)  # initializes the game object

    def update(self):  # updates the ball
        coords = self.get_position()  # gets the position of the ball
        width = self.canvas.winfo_width()  # gets the width of the canvas
        if coords[0] <= 0 or coords[2] >= width:  # if the ball hits the left or right wall
            self.direction[0] *= -1  # reverse the direction of the ball
        if coords[1] <= 0:  # if the ball hits the top wall
            self.direction[1] *= -1  # reverse the direction of the ball
        # get the x component of the ball's direction
        x = self.direction[0] * self.speed
        # get the y component of the ball's direction
        y = self.direction[1] * self.speed
        self.move(x, y)  # move the ball

    def collide(self, game_objects):  # checks if the ball collides with any game objects
        coords = self.get_position()  # gets the position of the ball
        x = (coords[0] + coords[2]) * 0.5  # gets the x coordinate of the ball
        if len(game_objects) > 1:  # if there are more than one game objects
            self.direction[1] *= -1  # reverse the direction of the ball
        elif len(game_objects) == 1:  # if there is only one game object
            game_object = game_objects[0]  # get the game object
            coords = game_object.get_position()  # get the position of the game object
            if x > coords[2]:  # if the ball is to the right of the game object
                self.direction[0] = 1  # move the ball to the right
            elif x < coords[0]:  # if the ball is to the left of the game object
                self.direction[0] = -1  # move the ball to the left
            else:  # if the ball is in the middle of the game object
                self.direction[1] *= -1  # reverse the direction of the ball

        for game_object in game_objects:  # for each game object
            if isinstance(game_object, Brick):  # if the game object is a brick
                game_object.hit()  # hit the brick


class Paddle(GameObject):  # Paddle object class
    def __init__(self, canvas, x, y):  # Paddle object constructor
        self.width = 80  # Paddle width
        self.height = 10  # Paddle height
        self.ball = None  # Ball object
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='orange')  # Paddle object
        super(Paddle, self).__init__(canvas, item)  # init paddle object

    def set_ball(self, ball):  # Set ball object
        self.ball = ball  # Set ball object

    def move(self, offset):  # Move paddle object
        coords = self.get_position()  # Get paddle object position
        width = self.canvas.winfo_width()  # Get canvas width
        # If paddle object position is in canvas
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)  # Move paddle object
            if self.ball is not None:  # If ball object is not None
                self.ball.move(offset, 0)  # Move the ball by offset


class Brick(GameObject):  # Brick class defines the color and size of bricks
    # Dictionary of colors for bricks
    COLORS = {1: '#54B36B', 2: '#28C7DF', 3: '#93671B'}

    def __init__(self, canvas, x, y, hits):  # Initialize the bricks
        self.width = 75  # Width of the brick
        self.height = 20  # Height of the brick
        self.hits = hits  # Number of hits the brick has
        color = Brick.COLORS[hits]  # Color of the brick
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')  # Create the brick
        super(Brick, self).__init__(canvas, item)  # Initialize the brick

    def hit(self):  # Function to hit the brick
        self.hits -= 1  # Decrease the number of hits
        if self.hits == 0:  # If the number of hits is 0
            self.delete()  # Delete the brick
        else:  # If the number of hits is not 0
            self.canvas.itemconfig(self.item,
                                   fill=Brick.COLORS[self.hits])  # Change the color of the brick


class Game(tk.Frame):
    # This defines the main game engine class
    # Game runs in main TK root window
    def __init__(self, master):
        super(Game, self).__init__(master)  # This calls the parent class init
        self.lives = 3  # Number of lives
        self.width = 610  # Width of the game window
        self.height = 400  # Height of the game window

        # This creates the game window
        self.canvas = tk.Canvas(self, bg='#006B3C',
                                width=self.width,
                                height=self.height,)
        self.canvas.pack()  # This packs the canvas into the game window
        self.pack()  # This packs the game window into the root window

        self.items = {}  # This is a dictionary of all the items in the game
        self.ball = None  # This is the ball object
        # This is the paddle object
        self.paddle = Paddle(self.canvas, self.width/2, 326)
        # This adds the paddle to the items dictionary
        self.items[self.paddle.item] = self.paddle
        for x in range(5, self.width - 5, 75):  # This creates the bricks
            self.add_brick(x + 37.5, 50, 2)
            self.add_brick(x + 37.5, 70, 1)
            self.add_brick(x + 37.5, 90, 1)

        self.hud = None  # This is the hud object
        self.setup_game()  # This calls the setup game function
        self.canvas.focus_set()  # This sets the focus to the canvas
        self.canvas.bind('<Left>',
                         lambda _: self.paddle.move(-10))  # This binds the left arrow key to the paddle
        self.canvas.bind('<Right>',
                         lambda _: self.paddle.move(10))  # This binds the right arrow key to the paddle

    def setup_game(self):
        # This sets up the game
        self.add_ball()  # This adds the ball to the game
        self.update_lives_text()  # This updates the lives text
        self.text = self.draw_text(300, 200,
                                   'Press Space to start')  # This draws the instructions
        # This binds the space bar to the start game function
        self.canvas.bind('<space>', lambda _: self.start_game())

    def add_ball(self):
        # This adds the ball to the game
        if self.ball is not None:
            # This checks if the ball is not None
            self.ball.delete()
        paddle_coords = self.paddle.get_position()  # This gets the paddle coordinates
        # This gets the x coordinate of the paddle
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 310)  # This creates the ball
        # This sets the paddle's ball to the ball
        self.paddle.set_ball(self.ball)

    def add_brick(self, x, y, hits):  # This adds the bricks to the game
        brick = Brick(self.canvas, x, y, hits)  # This creates the brick
        # This adds the brick to the items dictionary
        self.items[brick.item] = brick

    def draw_text(self, x, y, text, size='40'):  # This draws the text
        font = ('Comic Sans MS', size)  # This sets the font
        return self.canvas.create_text(x, y, text=text,
                                       font=font)  # This creates the text

    def update_lives_text(self):  # This updates the lives text
        text = 'Lives: % s' % self.lives  # This sets the text
        if self.hud is None:  # This checks if the hud is not None
            # This creates the HUD if none exists
            self.hud = self.draw_text(50, 20, text, 15)
        else:
            # This updates the HUD if one exists
            self.canvas.itemconfig(self.hud, text=text)

    def start_game(self):  # This starts the game
        self.canvas.unbind('<space>')  # This unbinds the space bar
        self.canvas.delete(self.text)  # This deletes the instructions
        self.paddle.ball = None  # This sets the paddle's ball to None
        self.game_loop()  # This calls the game loop

    def game_loop(self):  # This is the game loop
        self.check_collisions()  # This checks for collisions
        # This gets the number of bricks
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:  # If there are no bricks
            self.ball.speed = None  # This sets the ball's speed to None
            self.draw_text(300, 200, 'You win!')  # This draws the win text
        # If the ball goes off the bottom
        elif self.ball.get_position()[3] >= self.height:
            self.ball.speed = None  # This sets the ball's speed to None
            self.lives -= 1  # This subtracts a life
            if self.lives <= 0:  # If there are no lives
                self.update_lives_text()  # This updates the lives text
                # This draws the lose text
                self.draw_text(300, 200, 'You Lose!!! Game Over!')
            else:  # If there are lives
                # This sets up the game after 1 second
                self.after(1000, self.setup_game)
        else:  # If the ball is in the game
            self.ball.update()  # This updates the ball
            # This calls the game loop after 50 milliseconds
            self.after(50, self.game_loop)

    def check_collisions(self):  # This checks for collisions
        ball_coords = self.ball.get_position()  # This gets the ball coordinates
        # This gets the items that the ball overlaps
        items = self.canvas.find_overlapping(*ball_coords)
        # This gets the objects that the ball overlaps
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)  # This calls the ball collide function


def main():
    root = tk.Tk()  # set up the root window
    root.title('Brick Murderer')  # name the title
    game = Game(root)  # start the game object
    game.mainloop()  # end the main loop when the game ends


if __name__ == '__main__':
    # if running from terminal, execute this
    main()
