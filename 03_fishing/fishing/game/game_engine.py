"""
GameEngine: owns the hook and the fish, and runs one frame's worth of
game logic.

Starter version: the hook casts and retracts automatically in a
continuous loop - there's no player control over casting yet (that's
Task 3), only one fish type exists (Task 2 adds more), and there's no
round timer (Task 4). Catch detection also has a known bug (see
game/catch.py) that Task 1 asks you to fix.
"""
import pygame
from game.hook import Hook, IDLE
from game.fish import Fish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y


class GameEngine:
    def __init__(self):
        self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
        self.fish_list = [
            Fish(x=100, y=180, speed=2, point_value=10, color=(80, 180, 220)),
            Fish(x=400, y=280, speed=-2, point_value=25, color=(240, 150, 60)),
            Fish(x=250, y=380, speed=3, point_value=10, color=(80, 180, 220)),
        ]
        self.hooked_fish = None
        self.score = 0
        self.round_duration = 30_000
        self.round_start_time = pygame.time.get_ticks()
        self.round_active = True

    def start_cast(self):
        if self.round_active and self.hook.state == IDLE:
            self.hook.start_cast()

    def reset_round(self):
        self.score = 0
        self.round_start_time = pygame.time.get_ticks()
        self.round_active = True
        self.hooked_fish = None
        self.hook.state = IDLE

    def update(self):
        if self.round_active:
            elapsed = pygame.time.get_ticks() - self.round_start_time
            if elapsed >= self.round_duration:
                self.round_active = False
                self.hooked_fish = None
            else:
                self.hook.update()

        if not self.round_active:
            return

        for fish in self.fish_list:
            fish.update(WIDTH)
    

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y
            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self.hooked_fish = None
        else:
            caught = check_catch(self.hook, self.fish_list)
            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    def draw(self, surface, font):
        from game import renderer
        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)
        renderer.draw_scene(surface, self.hook, draw_list)
        if self.round_active:
            elapsed = pygame.time.get_ticks() - self.round_start_time
            remaining = max(0, (self.round_duration - elapsed + 999) // 1000)
            renderer.draw_text(surface, font, f"Time: {remaining}", (10, 10))
            renderer.draw_text(surface, font, f"Score: {self.score}", (10, 40))
        else:
            renderer.draw_text(surface, font, "TIME UP!", (10, 10))
            renderer.draw_text(surface, font, f"Final Score: {self.score}", (10, 40))
            renderer.draw_banner(surface, font, "ROUND OVER - Press R to play again")