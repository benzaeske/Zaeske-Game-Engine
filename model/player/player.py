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
        # Positional/physics
        self.position: Vector2 = start_pos
        self.hitbox: Rect = Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = (int(self.position.x), int(self.position.y))
        self.camera: Rect = Rect(0, 0, camera_width, camera_height)
        self.camera.center = (int(self.position.x), int(self.position.y))
        self.camera_w_adjust: float = camera_width / 2
        self.camera_h_adjust: float = camera_height / 2
        self.world_boundary: Tuple[float, float] = world_boundary
        self.facing_direction: int = 1
        self.max_speed: float = max_speed
        # Sprite
        self.surface_rect: Rect = Rect(0, 0, surface_width, surface_height)
        self.surface_rect.center = (int(self.position.x), int(self.position.y))
        self.surface_w_adj: float = surface_width / 2
        self.surface_h_adj: float = surface_height / 2
        # Health
        self.max_health: float = 100.0
        self.health: float = self.max_health
        self.max_hp_surface: Surface = pygame.Surface((self.hitbox.width, 10.0))
        self.max_hp_surface.fill((0, 0, 0))
        self.current_hp_surface: Surface = pygame.Surface((self.hitbox.width, 10.0))
        self.current_hp_surface.fill((222, 0, 0))
        # Shield
        self.max_shield: int = 10
        self.shield: int = 0
        self.shield_radius: float = self.hitbox.width
        self.shield_radius_squared: float = self.shield_radius * self.shield_radius
        self.shield_charge_delay: float = 1.0
        self.current_shield_charge_cooldown: float = self.shield_charge_delay
        self.shield_alpha_scaling: int = 10
        self.shield_surface: Surface = Surface((self.shield_radius * 2, self.shield_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.shield_surface,
                           (255, 255, 0, self.shield_alpha_scaling + (self.shield * self.shield_alpha_scaling)),
                           self.shield_surface.get_rect().center,
                           self.shield_radius)
        self.shield_surface_w_adj: float = self.shield_surface.get_width() / 2
        self.shield_surface_h_adj: float = self.shield_surface.get_height() / 2
        # Fish coherency
        self.cohere_green: int = 0
        self.cohere_yellow: int = 0
        self.cohere_red: int = 0

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
        # Wrap on x axis
        self.position.x = (self.position.x + self.world_boundary[0]) % self.world_boundary[0]
        # Prevent sprite from leaving world boundary on y-axis
        if self.position.y < self.surface_h_adj:
            self.position.y = self.surface_h_adj
        if self.position.y + self.surface_h_adj >= self.world_boundary[1]:
            self.position.y = self.world_boundary[1] - self.surface_h_adj
        # Update Hitbox
        self.hitbox.center = (int(self.position.x), int(self.position.y))
        # Update sprite
        self.surface_rect.center = (int(self.position.x), int(self.position.y))
        # Update camera. Prevent camera from leaving world boundary on y-axis
        self.camera.center = (int(self.position.x), int(self.position.y))
        if self.camera.bottom >= self.world_boundary[1] - 1:
            self.camera.bottom = int(self.world_boundary[1]) - 1
        if self.camera.top < 0:
            self.camera.top = 0
        # Update facing direction for drawing
        if velocity.x != 0:
            if velocity.x > 0:
                self.facing_direction = 1
            else:
                self.facing_direction = -1

    def update_hp(self, change: float) -> None:
        self.health += change
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0

    def charge_shield(self, dt) -> None:
        if self.shield < self.max_shield:
            self.current_shield_charge_cooldown -= dt
            if self.current_shield_charge_cooldown <= 0:
                self.current_shield_charge_cooldown = self.shield_charge_delay
                self.increment_shield()

    def increment_shield(self) -> None:
        self.shield += 1
        if self.shield > self.max_shield:
            self.shield = self.max_shield

    def decrement_shield(self) -> None:
        self.shield -= 1
        if self.shield < 0:
            self.shield = 0

    def update_shield_alpha(self) -> None:
        self.shield_surface: Surface = Surface((self.shield_radius * 2, self.shield_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.shield_surface,
                           (255, 255, 0, self.shield_alpha_scaling + (self.shield * self.shield_alpha_scaling)),
                           self.shield_surface.get_rect().center,
                           self.shield_radius)

    def get_camera_adjusted_position(self) -> Tuple[float, float]:
        return (
            self.surface_rect.left - self.camera.left,
            self.camera.bottom - self.surface_rect.bottom,
        )

    def get_camera_adjusted_hp_pos(self) -> Tuple[float, float]:
        return (
            self.hitbox.left - self.camera.left,
            self.camera.bottom - self.hitbox.top - self.max_hp_surface.get_height(),
        )

    def get_camera_adjusted_shield_pos(self) -> Tuple[float, float]:
        return (
            self.position.x - self.camera.left - self.shield_surface_w_adj,
            self.camera.bottom - self.position.y - self.shield_surface_h_adj
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
