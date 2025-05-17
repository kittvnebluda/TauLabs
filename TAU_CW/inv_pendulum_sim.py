import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inverted Pendulum Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Simulation parameters
dt = 0.01  # Time step

g = 9.81  # Gravity (m/s^2)

# Pendulum properties
m = 1.0  # Mass of the pendulum (kg)
pendulum_length = 2.0  # Length of the rectangular pendulum (m)
pendulum_width = 0.2  # Width of the rectangular pendulum (m)
pixels_per_meter = 100  # Scale factor

# Cart properties
M = 5.0  # Mass of the cart (kg)
cart_width = 0.5  # Width of the cart (m)
cart_height = 0.3  # Height of the cart (m)
cart_x = WIDTH // 2 / pixels_per_meter  # Initial cart position (m)
cart_velocity = 0.0  # Initial cart velocity (m/s)
cart_acceleration = 0.0  # Initial cart acceleration (m/s^2)

# Initial conditions for pendulum
theta = 0.0  # Initial angle (rad)
angular_velocity = 0.0  # Initial angular velocity (rad/s)
angular_acceleration = 0.0  # Angular acceleration (rad/s^2)

f = 0.0  # External torque (Nm)
u = 0.0  # Control input force (N)

# Helpful variables
r = pendulum_length / 2
Jpr = m * pendulum_length**2 / 12 + m * r*r
K = (M + m) * Jpr + (m * r)**2

# State-space model
A = np.array([
    [0, 1, 0, 0],
    [0, 0, -(m*r)**2/K, 0],
    [0, 0, 0, 1],
    [0, 0, -g*(m*r*K+(m*r)**3)/Jpr/K, 0]
])
B = np.array([
    0, (Jpr + m*r**2)/K, 0, -m*r/K
]).T
Bf = np.array([
    0, (m*r)**2-Jpr/r, 0, m*r/Jpr+m/K-(m*r)**3/Jpr/K
]).T
C = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0]
])

x = np.array([cart_x, 0.0, 0.0, 0.0])  # [x, dot_x, phi, dot_phi]

# Simulation loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update physics
    torque = 1.0 * np.sin(pygame.time.get_ticks() / 1000)  # Example torque varying sinusoidally
    f = torque  # Map external torque to state-space model

    # Compute state derivative using state-space equations
    x_dot = A @ x + B * u + Bf * f
    x += x_dot.flatten() * dt

    # Compute output
    y = C @ x

    # Extract variables for visualization
    cart_x = y[0]  # Position of the cart
    theta = y[1]  # Angle of the pendulum

    # Clear screen
    screen.fill(WHITE)

    # Draw cart
    cart_pixel_x = int(cart_x * pixels_per_meter)
    cart_pixel_y = HEIGHT // 2
    cart_rect = pygame.Rect(cart_pixel_x - int(cart_width * pixels_per_meter / 2),
                            cart_pixel_y - int(cart_height * pixels_per_meter / 2),
                            int(cart_width * pixels_per_meter),
                            int(cart_height * pixels_per_meter))
    pygame.draw.rect(screen, BLUE, cart_rect)

    # Draw pivot
    pivot_x = cart_pixel_x
    pivot_y = cart_pixel_y - int(cart_height * pixels_per_meter / 2)
    pygame.draw.circle(screen, BLACK, (pivot_x, pivot_y), 5)

    # Calculate pendulum rectangle corners
    pendulum_end_x = pivot_x + pendulum_length * pixels_per_meter * np.sin(theta)
    pendulum_end_y = pivot_y + pendulum_length * pixels_per_meter * np.cos(theta)
    
    pendulum_rect = pygame.Rect(0, 0, int(pendulum_width * pixels_per_meter), int(pendulum_length * pixels_per_meter))
    pendulum_rect.center = (pivot_x + (pendulum_end_x - pivot_x) / 2,
                            pivot_y + (pendulum_end_y - pivot_y) / 2)
    pendulum_surface = pygame.Surface((pendulum_rect.width, pendulum_rect.height), pygame.SRCALPHA)
    pendulum_surface.fill(RED)
    pendulum_surface = pygame.transform.rotate(pendulum_surface, -np.degrees(theta))
    screen.blit(pendulum_surface, pendulum_rect.topleft)

    # Display state variables
    font = pygame.font.SysFont(None, 24)
    state_text = font.render(f"State: x={x[0]:.2f}, phi={x[2]:.2f}", True, BLACK)
    input_text = font.render(f"Input Force (u): {u:.2f} N", True, BLACK)
    screen.blit(state_text, (10, 10))
    screen.blit(input_text, (10, 40))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(1 / dt)

pygame.quit()