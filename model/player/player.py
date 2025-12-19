from abc import ABC, abstractmethod
from typing import Tuple

import pygame
from pygame import Surface, Vector2, Rect
from pygame.key import ScancodeWrapper

from model.utils.vectorutils import limit_magnitude


class Player(ABC):

    def __init__(
        self,
        hitbox_width: float,
        hitbox_height: float,
        surface_width: float,
        surface_height: float,
        camera_width: float,
        camera_height: float,
        world_boundary: Tuple[float, float],
        start_pos: Vector2 = Vector2(0.0, 0.0),
        max_speed: float = 1.0,
    ) -> None:
        self.hitbox: Rect = Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = (int(start_pos.x), int(start_pos.y))
        self.surface_width: float = surface_width
        self.surface_height: float = surface_height
        self.camera_width: float = camera_width
        self.camera_height: float = camera_height
        self.camera_w_adjust: float = camera_width / 2
        self.camera_h_adjust: float = camera_height / 2
        self.world_boundary: Tuple[float, float] = world_boundary
        self.position: Vector2 = start_pos
        self.facing_direction: int = 1
        self.max_speed: float = max_speed
        self.max_health: float = 100.0
        self.health: float = self.max_health
        self.max_hp_surface: Surface = pygame.Surface((self.hitbox.width, 10.0))
        self.max_hp_surface.fill((0, 0, 0))
        self.current_hp_surface: Surface = pygame.Surface((self.hitbox.width, 10.0))
        self.current_hp_surface.fill((222, 0, 0))

    def move_player(
        self,
        key_presses: ScancodeWrapper,
        dt: float,
    ) -> None:
        """
        Moves the player according to the keys pressed. Movement is scaled with delta time like all other entities.
        Limits the camera position to be confined within positive x,y coordinates and under the provided world boundary.
        """
        velocity: Vector2 = Vector2(0.0, 0.0)
        # Calculate velocity as the sum of key presses
        if key_presses[pygame.K_LEFT]:
            velocity += Vector2(-self.max_speed, 0)
        if key_presses[pygame.K_RIGHT]:
            velocity += Vector2(self.max_speed, 0)
        if key_presses[pygame.K_UP]:
            velocity += Vector2(0, self.max_speed)
        if key_presses[pygame.K_DOWN]:
            velocity += Vector2(0, -self.max_speed)
        limit_magnitude(velocity, self.max_speed)
        self.position += velocity * dt
        # Don't let the camera go outside the world boundary
        if self.position.x - self.camera_w_adjust < 0:
            self.position.x = self.camera_w_adjust
        if self.position.x + self.camera_w_adjust >= self.world_boundary[0]:
            self.position.x = self.world_boundary[0] - self.camera_w_adjust - 1
        if self.position.y - self.camera_h_adjust < 0:
            self.position.y = self.camera_h_adjust
        if self.position.y + self.camera_h_adjust >= self.world_boundary[1]:
            self.position.y = self.world_boundary[1] - self.camera_h_adjust - 1
        # Update Hitbox
        self.hitbox.center = (int(self.position.x), int(self.position.y))
        # Update facing direction for drawing
        if velocity.x != 0:
            if velocity.x > 0:
                self.facing_direction = 1
            else:
                self.facing_direction = -1

    def get_camera_adjusted_position(self) -> Tuple[float, float]:
        """
        Returns the coordinates to center the player surface on the screen
        """
        return (
            self.camera_w_adjust - self.surface_width / 2,
            self.camera_h_adjust - self.surface_height / 2,
        )

    def get_camera_adjusted_hp_pos(self) -> Tuple[float, float]:
        """
        Returns the coordinates to center the hp bar on the player's hitbox
        """
        return (
            self.camera_w_adjust - self.hitbox.width / 2,
            self.camera_h_adjust + self.hitbox.height / 2
        )

    @abstractmethod
    def get_surface(self):
        pass


class Turtle(Player):
    def __init__(
        self,
        camera_width: float,
        camera_height: float,
        world_boundary: Tuple[float, float],
    ) -> None:
        hitbox_width: float = 100.0
        hitbox_height: float = 100.0
        surface_width: float = 128.0
        surface_height: float = 128.0
        turtle_speed: float = 256.0
        self.surface_left: Surface = pygame.image.load("images/turtle-side-left.png")
        self.surface_left = self.surface_left.convert_alpha()
        self.surface_left = pygame.transform.scale(
            self.surface_left, (surface_width, surface_height)
        )
        self.surface_right: Surface = pygame.image.load("images/turtle-side-right.png")
        self.surface_right = self.surface_right.convert_alpha()
        self.surface_right = pygame.transform.scale(
            self.surface_right, (surface_width, surface_height)
        )
        super().__init__(
            hitbox_width,
            hitbox_height,
            surface_width,
            surface_height,
            camera_width,
            camera_height,
            world_boundary,
            Vector2(world_boundary[0] / 2, world_boundary[1] / 2),
            turtle_speed,
        )

    def get_surface(self):
        if self.facing_direction > 0:
            return self.surface_right
        else:
            return self.surface_left
