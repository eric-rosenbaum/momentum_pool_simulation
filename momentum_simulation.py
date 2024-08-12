import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class MomentumSimulator:
    def __init__(self, speed, angle, rest_coeff, friction_coeff, min_speed_threshold, target_location):
        self.SPEED = speed
        self.ANGLE = angle
        self.REST_COEFF = rest_coeff
        self.FRICTION_COEFF = friction_coeff
        self.MIN_SPEED_THRESHOLD = min_speed_threshold
        self.TARGET_LOCATION = [target_location[0], 6 - target_location[1]]

        self.vx_input = self.SPEED * math.cos(-1 * math.radians(self.ANGLE))
        self.vy_input = self.SPEED * math.sin(-1 * math.radians(self.ANGLE))

        self.ball_radius = 0.15
        self.white_ball_position = [1, 3]
        self.black_ball_position = [3, 3]
        self.white_ball_velocity = [self.vx_input, self.vy_input]
        self.black_ball_velocity = [0, 0]

    def calculate_new_velocities(self):
        dx = self.black_ball_position[0] - self.white_ball_position[0]
        dy = self.black_ball_position[1] - self.white_ball_position[1]

        norm = math.sqrt(dx ** 2 + dy ** 2)
        nx = dx / norm
        ny = dy / norm
        tx = -ny
        ty = nx

        v1n = nx * self.white_ball_velocity[0] + ny * self.white_ball_velocity[1]
        v1t = tx * self.white_ball_velocity[0] + ty * self.white_ball_velocity[1]
        v2n = nx * self.black_ball_velocity[0] + ny * self.black_ball_velocity[1]
        v2t = tx * self.black_ball_velocity[0] + ty * self.black_ball_velocity[1]

        v1n_final = v2n * self.REST_COEFF
        v2n_final = v1n * self.REST_COEFF

        self.white_ball_velocity[0] = v1n_final * nx + v1t * tx
        self.white_ball_velocity[1] = v1n_final * ny + v1t * ty
        self.black_ball_velocity[0] = v2n_final * nx + v2t * tx
        self.black_ball_velocity[1] = v2n_final * ny + v2t * ty

    def apply_friction(self, velocity):
        velocity[0] *= (1 - self.FRICTION_COEFF)
        velocity[1] *= (1 - self.FRICTION_COEFF)

        if abs(velocity[0]) < self.MIN_SPEED_THRESHOLD and abs(velocity[1]) < self.MIN_SPEED_THRESHOLD:
            velocity[0] = 0
            velocity[1] = 0

    def simulate(self, steps=500):
        white_positions = [self.white_ball_position[:]]
        black_positions = [self.black_ball_position[:]]

        for _ in range(steps):
            self.apply_friction(self.white_ball_velocity)
            self.apply_friction(self.black_ball_velocity)

            self.white_ball_position[0] += self.white_ball_velocity[0] / 60
            self.white_ball_position[1] += self.white_ball_velocity[1] / 60
            self.black_ball_position[0] += self.black_ball_velocity[0] / 60
            self.black_ball_position[1] += self.black_ball_velocity[1] / 60

            distance = math.hypot(self.white_ball_position[0] - self.black_ball_position[0],
                                  self.white_ball_position[1] - self.black_ball_position[1])
            if distance < self.ball_radius * 2:
                self.calculate_new_velocities()

            white_positions.append(self.white_ball_position[:])
            black_positions.append(self.black_ball_position[:])

            if self.white_ball_velocity == [0, 0] and self.black_ball_velocity == [0, 0]:
                break

        return white_positions, black_positions

    def plot_simulation(self, white_positions, black_positions):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 6)
        ax.set_aspect('equal')

        # Draw the target
        target_circle = patches.Circle(self.TARGET_LOCATION, self.ball_radius * 2, color='red', fill=True)
        ax.add_patch(target_circle)

        # Draw the ball paths
        white_x, white_y = zip(*white_positions)
        black_x, black_y = zip(*black_positions)
        ax.plot(white_x, white_y, 'o-', color='white', label='White Ball')
        ax.plot(black_x, black_y, 'o-', color='black', label='Black Ball')

        ax.legend()
        ax.set_facecolor((0, 150/255, 0))
        plt.show()
