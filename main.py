import time
from maths import *

CONST_FPS = 60
TEST_TIME = -1


class Point:
    def __init__(self, x, y, size):
        self.center = pygame.Vector2(x, y)
        self.size = size
        self.velocity = pygame.Vector2()
        self.found = False


class Rectangle:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.found = False


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Bug Wars")
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.background_color = "white"
        self.running = True
        self.center_circle: Point | None = None
        self.points = []
        self.rectangles = []

        # FPS/Performance
        self.frame = 0
        self.start_time = time.time()
        self.total_fps = 0
        self.lowest_fps = 60

        # Simulation Mouse Position Variable
        self.mouse_pos = pygame.math.Vector2()

    def find(self, mouse_angles):
        C = self.center_circle.center

        for point in self.points:
            P = point.center

            angle_in_degrees = math.degrees(math.atan2(C.y - P.y, C.x - P.x))
            angle = (angle_in_degrees + 360) % 360

            for mouse_angle in mouse_angles:
                endpoint = pygame.Vector2(
                    C.x - 300 * math.cos(math.radians(mouse_angle)),
                    C.y - 300 * math.sin(math.radians(mouse_angle))
                )

                if distance_segment_to_point(C, endpoint, P) <= point.size:
                    point.found = True
                    return

            if (C.distance_to(P) <= 300 + point.size and
                    mouse_angles[0] <= angle <= mouse_angles[1]):
                point.found = True
            else:
                point.found = False

        for rect in self.rectangles:
            R = rect.rect
            rect.found = is_rectangle_in_sector(R.x, R.y, R.w, R.h, C.x, C.y, 300, mouse_angles[0], mouse_angles[1])

    def angle(self, A, B, aspectRatio):
        x = B[0] - A[0]
        y = B[1] - A[1]
        angle = math.atan2(-y, x / aspectRatio)
        return angle

    def update(self):
        self.screen.fill(self.background_color)

        if self.center_circle.velocity.x != 0 or self.center_circle.velocity.y != 0:
            self.center_circle.velocity = self.center_circle.velocity.normalize() * 5
            self.center_circle.center += self.center_circle.velocity

        C = self.center_circle.center
        M = self.mouse_pos

        angle_in_degrees = math.degrees(math.atan2(C.y - M.y, C.x - M.x))
        normalized_angle = (angle_in_degrees + 360) % 360
        angles = (normalized_angle - 20, normalized_angle + 20)
        # print(normalized_angle)

        self.find(angles)

        pygame.draw.circle(self.screen, "black", self.center_circle.center, self.center_circle.size, 0)

        points = []
        for angle in angles:
            endpoint = pygame.Vector2(
                C.x - 300 * math.cos(math.radians(angle)),
                C.y - 300 * math.sin(math.radians(angle))
            )
            points.append(endpoint)
            pygame.draw.line(self.screen, 'black', self.center_circle.center, endpoint, 1)

        rect = pygame.Rect(C.x - 300, C.y - 300, 600, 600)

        a1 = self.angle((self.center_circle.center.x, self.center_circle.center.y), (points[0].x, points[0].y), 1)
        a2 = self.angle((self.center_circle.center.x, self.center_circle.center.y), (points[1].x, points[1].y), 1)

        # RANGE
        # pygame.draw.circle(self.screen, "red", self.center_circle.center, 300, 0)

        pygame.draw.arc(self.screen, 'black', rect, a2, a1)

        for point in self.points:
            pygame.draw.circle(self.screen, "Red" if point.found else "blue", point.center, point.size, 0)

        for rect in self.rectangles:
            pygame.draw.rect(self.screen, "Red" if rect.found else "blue", rect.rect, 0)

        self.screen.blit(self.screen, (0, 0))

    def start(self):
        self.center_circle = Point(self.screen.get_width() / 2, self.screen.get_height() / 2, 5)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                key = event.unicode

                if key == "c":
                    self.points.append(Point(self.mouse_pos.x, self.mouse_pos.y, 15))

                if key == "r":
                    self.rectangles.append(Rectangle(self.mouse_pos.x, self.mouse_pos.y, 50, 50))

                speed = 5
                if key == "w":
                    self.center_circle.velocity.y = -speed
                if key == "s":
                    self.center_circle.velocity.y = speed
                if key == "a":
                    self.center_circle.velocity.x = -speed
                if key == "d":
                    self.center_circle.velocity.x = speed

            if event.type == pygame.KEYUP:
                key = event.unicode

                if key == "w":
                    self.center_circle.velocity.y = 0
                if key == "s":
                    self.center_circle.velocity.y = 0
                if key == "a":
                    self.center_circle.velocity.x = 0
                if key == "d":
                    self.center_circle.velocity.x = 0

    def displayText(self):
        # Elapsed Time Display text
        font = pygame.font.SysFont("Times New Roman", 25)
        elapsed_time_text = font.render(f"({time.time() - self.start_time:.2f})", False, "black")
        self.screen.blit(elapsed_time_text, (10, self.screen.get_height() - 40))
        if time.time() - self.start_time >= TEST_TIME != -1:
            sim.running = False

        # FPS Display text
        self.detailedFPS()

    def detailedFPS(self):
        font = pygame.font.SysFont("Times New Roman", 15)
        fps = math.floor(self.clock.get_fps())
        if self.frame > 10:
            self.lowest_fps = fps if fps < self.lowest_fps else self.lowest_fps
        self.total_fps += fps
        average_fps = math.floor(self.total_fps / self.frame) if self.frame > 0 else 0

        # Current FPS Display text
        fps_text = font.render(f"FPS: {fps}", False, "black")
        self.screen.blit(fps_text, (5, 5))

        # Average FPS Display text
        average_fps_text = font.render(f"Average: {average_fps}", False, "black")
        self.screen.blit(average_fps_text, (5, 25))

        # Lowest FPS Display text
        lowest_fps_text = font.render(f"Lowest: {self.lowest_fps}", False, "black")
        self.screen.blit(lowest_fps_text, (5, 45))

    def main(self):
        self.events()
        self.update()
        self.displayText()

        pygame.display.update()
        self.clock.tick(CONST_FPS)
        self.frame += 1


if __name__ == '__main__':
    sim = Game()
    sim.start()
    while sim.running:
        sim.main()
    pygame.quit()
