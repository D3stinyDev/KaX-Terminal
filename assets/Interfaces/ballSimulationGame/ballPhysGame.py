import tkinter as tk
import random
import math

class PhysicsBallGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Physics Ball Simulation")
        self.root.geometry("700x700")

        # Set up the canvas
        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack()

        # Draw a solid background
        self.draw_solid_background()

        # Draw the circle boundary
        self.circle_radius = 200
        self.circle_x = 300
        self.circle_y = 300
        self.canvas.create_oval(self.circle_x - self.circle_radius, self.circle_y - self.circle_radius,
                                self.circle_x + self.circle_radius, self.circle_y + self.circle_radius,
                                outline='black', width=3)

        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.place_ball)

        # Create a frame for the buttons
        self.button_frame = tk.Frame(root, bg='lightblue')
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Reset button
        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_game, bg='lightgreen', font=('Arial', 12), relief=tk.RAISED)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Buttons for resizing balls
        self.size_increase_button = tk.Button(self.button_frame, text="Increase Size", command=self.increase_size, bg='lightcoral', font=('Arial', 12), relief=tk.RAISED)
        self.size_increase_button.pack(side=tk.LEFT, padx=10)
        self.size_decrease_button = tk.Button(self.button_frame, text="Decrease Size", command=self.decrease_size, bg='lightcoral', font=('Arial', 12), relief=tk.RAISED)
        self.size_decrease_button.pack(side=tk.LEFT, padx=10)

        # Buttons for changing speed
        self.speed_increase_button = tk.Button(self.button_frame, text="Increase Speed", command=self.increase_speed, bg='lightsalmon', font=('Arial', 12), relief=tk.RAISED)
        self.speed_increase_button.pack(side=tk.LEFT, padx=10)
        self.speed_decrease_button = tk.Button(self.button_frame, text="Decrease Speed", command=self.decrease_speed, bg='lightsalmon', font=('Arial', 12), relief=tk.RAISED)
        self.speed_decrease_button.pack(side=tk.LEFT, padx=10)

        self.balls = []
        self.gravity = 0.03  # Simulate lunar gravity
        self.size_change_step = 2
        self.speed_change_step = 1

        self.update_physics()

    def draw_solid_background(self):
        # Fill the canvas with a solid color
        self.canvas.create_rectangle(0, 0, 600, 600, fill='white', outline='')

    def place_ball(self, event):
        # Check if the click is within the circle
        dx = event.x - self.circle_x
        dy = event.y - self.circle_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= self.circle_radius:
            # Place the ball with a random color
            color = self.random_color()
            ball = Ball(self.canvas, event.x, event.y, self.gravity, self.circle_x, self.circle_y, self.circle_radius, color)
            self.balls.append(ball)

    def update_physics(self):
        # Update position and check collisions
        for i, ball in enumerate(self.balls):
            ball.update_position()
            self.handle_boundary_collision(ball)
            for other_ball in self.balls[i+1:]:
                self.handle_ball_collision(ball, other_ball)
        self.root.after(20, self.update_physics)

    def handle_boundary_collision(self, ball):
        # Calculate distance from center of the circle
        dx = ball.x - self.circle_x
        dy = ball.y - self.circle_y
        distance_from_center = math.sqrt(dx**2 + dy**2)

        if distance_from_center + ball.radius > self.circle_radius:
            # Reflect the ball's velocity when it hits the boundary
            overlap = (distance_from_center + ball.radius) - self.circle_radius

            # Normalize the direction from the center to the ball's current position
            norm_dx = dx / distance_from_center
            norm_dy = dy / distance_from_center

            # Reflect the velocity
            dot_product = ball.vx * norm_dx + ball.vy * norm_dy
            ball.vx -= 2 * dot_product * norm_dx
            ball.vy -= 2 * dot_product * norm_dy

            # Adjust the position to keep the ball inside the circle
            ball.x -= norm_dx * overlap
            ball.y -= norm_dy * overlap

    def handle_ball_collision(self, ball1, ball2):
        dx = ball2.x - ball1.x
        dy = ball2.y - ball1.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < ball1.radius + ball2.radius:
            # Calculate new velocities for both balls after collision
            # Calculate normal vector
            nx = dx / distance
            ny = dy / distance

            # Relative velocity
            dvx = ball2.vx - ball1.vx
            dvy = ball2.vy - ball1.vy
            dot_product = (dvx * nx + dvy * ny) * 2

            # Update velocities based on collision
            ball1.vx += dot_product * nx
            ball1.vy += dot_product * ny
            ball2.vx -= dot_product * nx
            ball2.vy -= dot_product * ny

            # Separate balls slightly to prevent sticking
            overlap = ball1.radius + ball2.radius - distance
            separation = overlap / 2

            ball1.x -= nx * separation
            ball1.y -= ny * separation
            ball2.x += nx * separation
            ball2.y += ny * separation

    def reset_game(self):
        for ball in self.balls:
            self.canvas.delete(ball.id)
        self.balls = []

    def increase_size(self):
        for ball in self.balls:
            ball.change_size(self.size_change_step)

    def decrease_size(self):
        for ball in self.balls:
            ball.change_size(-self.size_change_step)

    def increase_speed(self):
        for ball in self.balls:
            ball.change_speed(self.speed_change_step)

    def decrease_speed(self):
        for ball in self.balls:
            ball.change_speed(-self.speed_change_step)

    def random_color(self):
        while True:
            # Generate a random color
            color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # Check if the color is not near black or white
            if not self.is_black_or_white(color):
                return color

    def is_black_or_white(self, color):
        # Convert hex color to RGB
        rgb = [int(color[i:i+2], 16) for i in (1, 3, 5)]
        # Check if the color is near black or white
        return all(val < 50 or val > 205 for val in rgb)  # Tolerance for near-black and near-white

class Ball:
    def __init__(self, canvas, x, y, gravity, circle_x, circle_y, circle_radius, color):
        self.canvas = canvas
        self.radius = 15
        self.x = x
        self.y = y
        self.gravity = gravity
        self.circle_x = circle_x
        self.circle_y = circle_y
        self.circle_radius = circle_radius
        self.vx = random.uniform(-1, 1)  # Slight horizontal motion
        self.vy = 0  # Start at rest vertically
        self.color = color
        self.id = self.canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                          self.x + self.radius, self.y + self.radius,
                                          fill=self.color, outline='gray', width=2)

    def update_position(self):
        # Apply gravity
        self.vy += self.gravity

        # Update the position with the current velocity
        self.x += self.vx
        self.y += self.vy

        # Update the canvas with the new position
        self.canvas.coords(self.id, self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius)

    def change_size(self, delta):
        # Change the ball's radius and update its graphical representation
        self.radius = max(5, self.radius + delta)
        self.canvas.coords(self.id, self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius)

    def change_speed(self, delta):
        # Change the ball's speed by adjusting velocity
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > 0:
            # Normalize the velocity and adjust its magnitude
            norm_vx = self.vx / speed
            norm_vy = self.vy / speed
            new_speed = max(0, speed + delta)
            self.vx = norm_vx * new_speed
            self.vy = norm_vy * new_speed

if __name__ == "__main__":
    root = tk.Tk()
    game = PhysicsBallGame(root)
    root.mainloop()
