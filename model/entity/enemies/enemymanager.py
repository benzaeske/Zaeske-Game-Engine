import copy
import random
from abc import abstractmethod, ABC

from pygame import Vector2, Rect

from controller.camerainterface import CameraInterface
from model.entity.enemies.enemy import Enemy
from model.entity.entitymanager import EntityManager, ModelContext


class EnemyManager[T: Enemy](EntityManager, ABC):
    """
    Base class for a group of enemies that continue to spawn on a given cooldown interval.
    """
    def __init__(self, initial_cooldown: float, initial_spawn_amount: int) -> None:
        super().__init__()
        self._enemies: set[T] = set()
        self._cooldown: float = initial_cooldown
        self._spawn_timer: float = 0.0
        self._spawn_amount: int = initial_spawn_amount
        self._spawn_state: int = 3 # Used to rotate where random enemy positions are sampled from

    def frame_actions(self, context: ModelContext, camera: CameraInterface, dt: float) -> None:
        # Destroy enemies that have no hp
        for enemy in self._enemies.copy():
            if enemy.get_hp() <= 0:
                self._enemies.remove(enemy)
                context.grid_space.remove_entity(enemy)
                self._notify_observers_entity_deleted(enemy)
        # Spawn new enemies
        if self.tick_spawn_timer(dt):
            self.spawn(context, camera)
        # Accelerate all enemies towards the player and avoid close neighbors
        for enemy in self._enemies:
            enemy.frame_actions(context, dt)

    def movement(self, context: ModelContext, camera: CameraInterface, dt: float) -> None:
        for enemy in self._enemies:
            old_pos: Vector2 = enemy.get_position()
            enemy.move(context, dt)
            context.grid_space.process_moved_entity(old_pos, enemy)

    def tick_spawn_timer(self, dt: float) -> bool:
        """
        Updates the spawner's timer according to the provided delta time since the last frame. Should only be called
        once in the game loop.
        If the spawning cooldown is reached, returns True and reset the timer, otherwise False.
        """
        self._spawn_timer += dt
        if self._spawn_timer >= self._cooldown:
            self._spawn_timer = 0.0
            return True
        return False

    def spawn(self, context: ModelContext, camera: CameraInterface) -> None:
        """
        Creates new enemies according to this spawner's amount property. Adds new enemies to this group's list as well
        as to the grid space.
        """
        for _ in range(self._spawn_amount):
            new_enemy: T = self.get_new_enemy()
            new_enemy.set_position(self._get_initial_position(camera))
            self._enemies.add(new_enemy)
            context.grid_space.add_entity(new_enemy)
            self._notify_observers_entity_created(new_enemy)

    @abstractmethod
    def get_new_enemy(self) -> T:
        """
        Factory method to create a new Enemy. Initial position/velocity/acceleration should not be set here
        """
        pass

    def _get_initial_position(self, camera: CameraInterface) -> Vector2:
        """
        Get a random x and y position just outside camera range. Rotate which side of the camera (left, right, top,
        or bottom) to sample from each time the method is called
        """
        camera_window: Rect = camera.get_window()
        spawn_range: float = 256.0
        pos: Vector2 = Vector2(0.0, 0.0)
        match self._spawn_state:
            case 0:
                # Top
                pos.x = random.uniform(camera_window.left, camera_window.right)
                pos.y = random.uniform(camera_window.bottom, camera_window.bottom + spawn_range) # Pygame Rect uses inverted y
            case 1:
                # Right
                pos.x = random.uniform(camera_window.right, camera_window.right + spawn_range)
                pos.y = random.uniform(camera_window.top, camera_window.bottom)
            case 2:
                # Bottom
                pos.x = random.uniform(camera_window.left, camera_window.right)
                pos.y = random.uniform(camera_window.top, camera_window.top - spawn_range)
            case 3:
                # Left
                pos.x = random.uniform(camera_window.left, camera_window.left - spawn_range)
                pos.y = random.uniform(camera_window.top, camera_window.bottom)
        #self._update_spawn_state()
        return pos

    def _update_spawn_state(self):
        self._spawn_state += 1
        if self._spawn_state > 3:
            self._spawn_state = 0


