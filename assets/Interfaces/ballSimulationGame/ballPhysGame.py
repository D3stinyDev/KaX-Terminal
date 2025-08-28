import customtkinter as ctk
import math
import random

class BallPhysicsGame(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Ball Physics Simulation")
        self.geometry("1000x700")
        self.resizable(False, False)

        # Default settings
        self.ball_radius = 30
        self.ball_color = "#FFFFFF"
        self.ball_outline = "#000000"
        self.ball_opacity = 1.0
        self.gravity = 0.5
        self.bounce_factor = 1.0
        self.simulation_speed = 20
        self.circle_radius = 250
        self.circle_outline_thickness = 3
        self.bg_color = "#000000"
        self.init_dx = 0
        self.init_dy = 0
        self.random_color = False
        self.simulation_paused = False

        # Layout frames
        self.sidebar = ctk.CTkFrame(self, width=250, fg_color="#222")
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
        self.canvas = ctk.CTkCanvas(self, bg=self.bg_color, width=750, height=700, highlightthickness=0)
        self.canvas.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

        # Central circle parameters
        self.circle_center = (375, 350)
        self.circle = self.canvas.create_oval(
            self.circle_center[0] - self.circle_radius,
            self.circle_center[1] - self.circle_radius,
            self.circle_center[0] + self.circle_radius,
            self.circle_center[1] + self.circle_radius,
            outline="white", width=self.circle_outline_thickness
        )

        self.balls = []      # Canvas object IDs
        self.ball_data = []  # Each: [x, y, dx, dy, radius, color, outline, opacity]

        # Dragging state
        self.dragging_ball = None
        self.drag_offset = (0, 0)

        # Controls (Settings Panel)
        ctk.CTkLabel(self.sidebar, text="Settings", font=("Arial", 20, "bold")).pack(pady=(20, 10))

        self.radius_slider = ctk.CTkSlider(self.sidebar, from_=10, to=80, number_of_steps=70, command=self.set_radius)
        self.radius_slider.set(self.ball_radius)
        ctk.CTkLabel(self.sidebar, text="Ball Radius").pack(pady=(10, 0))
        self.radius_slider.pack(pady=(0, 10))

        self.gravity_slider = ctk.CTkSlider(self.sidebar, from_=0, to=2, number_of_steps=40, command=self.set_gravity)
        self.gravity_slider.set(self.gravity)
        ctk.CTkLabel(self.sidebar, text="Gravity").pack(pady=(10, 0))
        self.gravity_slider.pack(pady=(0, 10))

        self.bounce_slider = ctk.CTkSlider(self.sidebar, from_=0.5, to=1.0, number_of_steps=50, command=self.set_bounce)
        self.bounce_slider.set(self.bounce_factor)
        ctk.CTkLabel(self.sidebar, text="Bounce Factor").pack(pady=(10, 0))
        self.bounce_slider.pack(pady=(0, 10))

        self.speed_slider = ctk.CTkSlider(self.sidebar, from_=5, to=50, number_of_steps=45, command=self.set_speed)
        self.speed_slider.set(self.simulation_speed)
        ctk.CTkLabel(self.sidebar, text="Simulation Speed").pack(pady=(10, 0))
        self.speed_slider.pack(pady=(0, 10))

        ctk.CTkLabel(self.sidebar, text="Ball Color").pack(pady=(10, 0))
        self.color_entry = ctk.CTkEntry(self.sidebar, placeholder_text="#RRGGBB")
        self.color_entry.insert(0, self.ball_color)
        self.color_entry.pack(pady=(0, 10))
        self.color_entry.bind("<Return>", self.set_color)

        ctk.CTkLabel(self.sidebar, text="Ball Outline Color").pack(pady=(10, 0))
        self.outline_entry = ctk.CTkEntry(self.sidebar, placeholder_text="#RRGGBB")
        self.outline_entry.insert(0, self.ball_outline)
        self.outline_entry.pack(pady=(0, 10))
        self.outline_entry.bind("<Return>", self.set_outline)

        self.opacity_slider = ctk.CTkSlider(self.sidebar, from_=0.1, to=1.0, number_of_steps=9, command=self.set_opacity)
        self.opacity_slider.set(self.ball_opacity)
        ctk.CTkLabel(self.sidebar, text="Ball Opacity").pack(pady=(10, 0))
        self.opacity_slider.pack(pady=(0, 10))

        ctk.CTkLabel(self.sidebar, text="Initial Velocity X").pack(pady=(10, 0))
        self.init_dx_slider = ctk.CTkSlider(self.sidebar, from_=-10, to=10, number_of_steps=20, command=self.set_init_dx)
        self.init_dx_slider.set(self.init_dx)
        self.init_dx_slider.pack(pady=(0, 10))

        ctk.CTkLabel(self.sidebar, text="Initial Velocity Y").pack(pady=(10, 0))
        self.init_dy_slider = ctk.CTkSlider(self.sidebar, from_=-10, to=10, number_of_steps=20, command=self.set_init_dy)
        self.init_dy_slider.set(self.init_dy)
        self.init_dy_slider.pack(pady=(0, 10))

        self.random_color_checkbox = ctk.CTkCheckBox(self.sidebar, text="Random Ball Color", command=self.toggle_random_color)
        self.random_color_checkbox.pack(pady=(10, 10))

        ctk.CTkLabel(self.sidebar, text="Circle Size").pack(pady=(10, 0))
        self.circle_slider = ctk.CTkSlider(self.sidebar, from_=100, to=340, number_of_steps=240, command=self.set_circle_radius)
        self.circle_slider.set(self.circle_radius)
        self.circle_slider.pack(pady=(0, 10))

        ctk.CTkLabel(self.sidebar, text="Circle Outline Thickness").pack(pady=(10, 0))
        self.circle_outline_slider = ctk.CTkSlider(self.sidebar, from_=1, to=10, number_of_steps=9, command=self.set_circle_outline)
        self.circle_outline_slider.set(self.circle_outline_thickness)
        self.circle_outline_slider.pack(pady=(0, 10))

        ctk.CTkLabel(self.sidebar, text="Background Color").pack(pady=(10, 0))
        self.bg_entry = ctk.CTkEntry(self.sidebar, placeholder_text="#RRGGBB")
        self.bg_entry.insert(0, self.bg_color)
        self.bg_entry.pack(pady=(0, 10))
        self.bg_entry.bind("<Return>", self.set_bg_color)

        self.pause_btn = ctk.CTkButton(self.sidebar, text="Pause Simulation", command=self.toggle_pause)
        self.pause_btn.pack(pady=(20, 10))

        self.remove_balls_btn = ctk.CTkButton(self.sidebar, text="Remove All Balls", command=self.remove_all_balls)
        self.remove_balls_btn.pack(pady=(10, 10))

        ctk.CTkLabel(self.sidebar, text="Left click: Place ball\nRight drag: Move ball", font=("Arial", 12)).pack(pady=(40, 0))

        # Bind mouse click to place ball
        self.canvas.bind("<Button-1>", self.place_ball)
        self.canvas.bind("<Button-3>", self.start_drag_ball)
        self.canvas.bind("<B3-Motion>", self.drag_ball)
        self.canvas.bind("<ButtonRelease-3>", self.stop_drag_ball)

        self.animate_balls()

    # Settings callbacks
    def set_radius(self, value):
        self.ball_radius = int(value)

    def set_gravity(self, value):
        self.gravity = float(value)

    def set_bounce(self, value):
        self.bounce_factor = float(value)

    def set_speed(self, value):
        self.simulation_speed = int(value)

    def set_color(self, event=None):
        color = self.color_entry.get()
        if len(color) == 7 and color.startswith("#"):
            self.ball_color = color

    def set_outline(self, event=None):
        outline = self.outline_entry.get()
        if len(outline) == 7 and outline.startswith("#"):
            self.ball_outline = outline

    def set_opacity(self, value):
        self.ball_opacity = float(value)

    def set_init_dx(self, value):
        self.init_dx = float(value)

    def set_init_dy(self, value):
        self.init_dy = float(value)

    def toggle_random_color(self):
        self.random_color = not self.random_color

    def set_circle_radius(self, value):
        self.circle_radius = int(value)
        self.canvas.coords(
            self.circle,
            self.circle_center[0] - self.circle_radius,
            self.circle_center[1] - self.circle_radius,
            self.circle_center[0] + self.circle_radius,
            self.circle_center[1] + self.circle_radius,
        )
        # Remove balls outside new circle
        for i, ball in reversed(list(enumerate(self.balls))):
            x, y, _, _, r, _, _, _ = self.ball_data[i]
            if math.hypot(x - self.circle_center[0], y - self.circle_center[1]) + r > self.circle_radius:
                self.canvas.delete(ball)
                del self.balls[i]
                del self.ball_data[i]

    def set_circle_outline(self, value):
        self.circle_outline_thickness = int(value)
        self.canvas.itemconfig(self.circle, width=self.circle_outline_thickness)

    def set_bg_color(self, event=None):
        color = self.bg_entry.get()
        if len(color) == 7 and color.startswith("#"):
            self.bg_color = color
            self.canvas.configure(bg=self.bg_color)

    def toggle_pause(self):
        self.simulation_paused = not self.simulation_paused
        self.pause_btn.configure(text="Resume Simulation" if self.simulation_paused else "Pause Simulation")

    # Ball logic
    def place_ball(self, event):
        x, y = event.x, event.y
        r = self.ball_radius
        dist = math.hypot(x - self.circle_center[0], y - self.circle_center[1])
        if dist + r <= self.circle_radius:
            color = self.random_color_hex() if self.random_color else self.ball_color
            outline = self.ball_outline
            opacity = self.ball_opacity
            # Tkinter does not support alpha for canvas ovals, so we skip opacity visually
            ball = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=outline)
            dx = self.init_dx
            dy = self.init_dy
            self.balls.append(ball)
            self.ball_data.append([x, y, dx, dy, r, color, outline, opacity])

    def random_color_hex(self):
        return f'#{random.randint(0, 0xFFFFFF):06x}'

    def remove_all_balls(self):
        for ball in self.balls:
            self.canvas.delete(ball)
        self.balls.clear()
        self.ball_data.clear()

    def animate_balls(self):
        if not self.simulation_paused:
            self.handle_collisions()
            for i, ball in enumerate(self.balls):
                self.move_ball(i, ball)
        self.after(self.simulation_speed, self.animate_balls)

    def move_ball(self, index, ball):
        # Don't move if being dragged
        if self.dragging_ball == ball:
            return

        x, y, dx, dy, r, color, outline, opacity = self.ball_data[index]

        # Gravity
        dy += self.gravity

        # Predict next position
        nx = x + dx
        ny = y + dy

        # Distance from center after move
        dist = math.hypot(nx - self.circle_center[0], ny - self.circle_center[1])

        # Bounce off the inner circle boundary
        if dist + r >= self.circle_radius:
            # Calculate normal at collision point
            angle = math.atan2(ny - self.circle_center[1], nx - self.circle_center[0])
            nx_vec = math.cos(angle)
            ny_vec = math.sin(angle)
            # Velocity vector
            v_dot_n = dx * nx_vec + dy * ny_vec
            # Reflect velocity
            dx = dx - 2 * v_dot_n * nx_vec
            dy = dy - 2 * v_dot_n * ny_vec
            # Apply bounce factor
            dx *= self.bounce_factor
            dy *= self.bounce_factor
            # Move ball just inside the boundary
            nx = self.circle_center[0] + (self.circle_radius - r - 1) * nx_vec
            ny = self.circle_center[1] + (self.circle_radius - r - 1) * ny_vec

        # Update position
        self.ball_data[index] = [nx, ny, dx, dy, r, color, outline, opacity]
        self.canvas.coords(ball, nx - r, ny - r, nx + r, ny + r)
        self.canvas.itemconfig(ball, fill=color, outline=outline)

    def handle_collisions(self):
        n = len(self.balls)
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1, dx1, dy1, r1, _, _, _ = self.ball_data[i]
                x2, y2, dx2, dy2, r2, _, _, _ = self.ball_data[j]
                dist = math.hypot(x2 - x1, y2 - y1)
                if dist < r1 + r2:
                    # Simple elastic collision
                    angle = math.atan2(y2 - y1, x2 - x1)
                    nx = math.cos(angle)
                    ny = math.sin(angle)
                    # Project velocities onto normal
                    v1n = dx1 * nx + dy1 * ny
                    v2n = dx2 * nx + dy2 * ny
                    # Swap normal components
                    dx1_new = dx1 + (v2n - v1n) * nx
                    dy1_new = dy1 + (v2n - v1n) * ny
                    dx2_new = dx2 + (v1n - v2n) * nx
                    dy2_new = dy2 + (v1n - v2n) * ny
                    self.ball_data[i][2] = dx1_new
                    self.ball_data[i][3] = dy1_new
                    self.ball_data[j][2] = dx2_new
                    self.ball_data[j][3] = dy2_new
                    # Separate balls to avoid sticking
                    overlap = r1 + r2 - dist
                    self.ball_data[i][0] -= overlap/2 * nx
                    self.ball_data[i][1] -= overlap/2 * ny
                    self.ball_data[j][0] += overlap/2 * nx
                    self.ball_data[j][1] += overlap/2 * ny

    def start_drag_ball(self, event):
        x, y = event.x, event.y
        for i, ball in enumerate(self.balls):
            bx, by, _, _, r, _, _, _ = self.ball_data[i]
            if math.hypot(x - bx, y - by) <= r:
                self.dragging_ball = ball
                self.drag_offset = (bx - x, by - y)
                break

    def drag_ball(self, event):
        if self.dragging_ball is not None:
            i = self.balls.index(self.dragging_ball)
            r = self.ball_data[i][4]
            # Keep inside the circle
            nx = event.x + self.drag_offset[0]
            ny = event.y + self.drag_offset[1]
            dist = math.hypot(nx - self.circle_center[0], ny - self.circle_center[1])
            if dist + r > self.circle_radius:
                # Clamp to circle edge
                angle = math.atan2(ny - self.circle_center[1], nx - self.circle_center[0])
                nx = self.circle_center[0] + (self.circle_radius - r - 1) * math.cos(angle)
                ny = self.circle_center[1] + (self.circle_radius - r - 1) * math.sin(angle)
            self.ball_data[i][0] = nx
            self.ball_data[i][1] = ny
            self.ball_data[i][2] = 0  # Stop velocity while dragging
            self.ball_data[i][3] = 0
            self.canvas.coords(self.dragging_ball, nx - r, ny - r, nx + r, ny + r)

    def stop_drag_ball(self, event):
        self.dragging_ball = None

if __name__ == "__main__":
    app = ctk.CTk()
    game = BallPhysicsGame(app)
    app.mainloop()