import pygame
import game_config as g_c
from random import randint

# Raised when an attempt is made to modify a frozen dict.
class FrozenDictError(KeyError): pass


class FrozenDict(dict):

    def __setitem__(self, key, value):
        raise FrozenDictError(f'cannot assign to key {key!r}')

    def update(self, *args, **kwargs):
        raise FrozenDictError(f'cannot assign to {self!r}')


class Spaceship():
    
    _velocity = g_c.CHAR_VEL
    _max_bullets = g_c.CHAR_MAX_BULLETS
    _max_health = g_c.CHAR_MAX_HEALTH
    _players = 0
    
    def __init__(
            self,
            image_dir: str,
            image_transform_attr: dict,
            territory: str
    ):
        Spaceship.set_player_num(Spaceship._players + 1)
        self.image_dir = image_dir
        self._image_transform_attr = FrozenDict({})
        self.image_transform_attr = image_transform_attr
        self._territory = ""
        self.territory = territory
        self._health = Spaceship._max_health
        self._bullets = []
        
        rendered_char = self._init_pos()
        self._pos_x = rendered_char.x
        self._pos_y = rendered_char.y

        return
    
    @classmethod
    def set_player_num(cls, value):
        if value <= 2:
            cls._players = value
        return
    
    @property
    def image_transform_attr(self) -> FrozenDict:
        return self._image_transform_attr
    
    @image_transform_attr.setter
    def image_transform_attr(self, value: dict):
        if type(value) == dict:
            for attr in ["width", "height", "rotation"]:
                if attr not in list(value.keys()):
                    raise AttributeError("Cannot transform spaceship image due to missing attribute/s.")
            
            try:

                self._image_transform_attr = FrozenDict(
                    {
                        "width": int(value["width"]),
                        "height": int(value["height"]),
                        "rotation": int(value["rotation"])
                    }
                )

            except:
                raise TypeError("Could not convert spaceship image transformation attribute/s to an integer.")

            if self._image_transform_attr["rotation"] < 0 or self._image_transform_attr["rotation"] > 360:
                raise ValueError("Image transformation rotation attribute needs to be an integer between 0 and 360.")

        else:
            raise AttributeError("The 'image_transform_attr' attribute needs to be a dictionary.")
        
        return
    
    @property
    def territory(self) -> str:
        return self._territory
    
    @territory.setter
    def territory(self, value):
        if type(value) == str:
            if value.lower() not in ["left", "right"]:
                raise ValueError("The 'territory' attribute needs to be 'left' or 'right'.")
            else:
                self._territory = value
        else:
            raise TypeError("The 'territory' attribute needs to be a string type.")
        return
    
    @property
    def key_controls(self) -> FrozenDict:
        if self.territory.lower() == "left":
            return FrozenDict(
                {
                    "left-key": pygame.K_a,
                    "right-key": pygame.K_d,
                    "up-key": pygame.K_w,
                    "down-key": pygame.K_s,
                    "fire-key": pygame.K_q
                }
            )
        elif self.territory.lower() == "right":
            return FrozenDict(
                {
                    "left-key": pygame.K_LEFT,
                    "right-key": pygame.K_RIGHT,
                    "up-key": pygame.K_UP,
                    "down-key": pygame.K_DOWN,
                    "fire-key": pygame.K_BACKSLASH
                }
            )

    @key_controls.setter
    def key_controls(self, value):
        raise ValueError("Cannot update player controls.")
        return
    
    def _init_pos(self) -> pygame.rect.Rect:
        if self.territory.lower() == "left":
            game_char = pygame.Rect(
                randint(0, g_c.BORDER["x_pos"] - self.image_transform_attr["width"]),
                randint(0, g_c.GAME_HEIGHT - self.image_transform_attr["height"]),
                self.image_transform_attr["width"], 
                self.image_transform_attr["height"]
            )

        elif self.territory.lower() == "right":
            game_char = pygame.Rect(
                randint(g_c.BORDER["x_pos"] + g_c.BORDER["width"], g_c.GAME_WIDTH - self.image_transform_attr["width"]),
                randint(0, g_c.GAME_HEIGHT - self.image_transform_attr["height"]),
                self.image_transform_attr["width"], 
                self.image_transform_attr["height"]
            )
        return game_char

    @property
    def pos_x(self) -> int:
        return self._pos_x

    @pos_x.setter
    def pos_x(self, value):
        if self.territory.lower() == "left":
            if 0 <= value <= g_c.BORDER["x_pos"] - self.image_transform_attr["width"]:
                self._pos_x = value
            elif value < 0:
                self._pos_x = 0
            else:
                self._pos_x = g_c.BORDER["x_pos"] - self.image_transform_attr["width"]

        elif self.territory.lower() == "right":
            if g_c.BORDER["x_pos"] + g_c.BORDER["width"] <= value <= g_c.GAME_WIDTH - self.image_transform_attr["width"]:
                self._pos_x = value
            elif value < g_c.BORDER["x_pos"] + g_c.BORDER["width"]:
                self._pos_x = g_c.BORDER["x_pos"] + g_c.BORDER["width"]
            else:
                self._pos_x = g_c.GAME_WIDTH - self.image_transform_attr["width"]

    @property
    def pos_y(self) -> int:
        return self._pos_y

    @pos_y.setter
    def pos_y(self, value):
        if 0 <= value <= g_c.GAME_HEIGHT - self.image_transform_attr["height"] - 15:
            self._pos_y = value
        elif value < 0:
            self._pos_y = 0
        else:
            self._pos_y = g_c.GAME_HEIGHT - self.image_transform_attr["height"] - 15

    
    def move(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[self.key_controls["up-key"]]:
            self.pos_y -= Spaceship._velocity
        elif keys_pressed[self.key_controls["down-key"]]:
            self.pos_y += Spaceship._velocity
        elif keys_pressed[self.key_controls["left-key"]]:
            self.pos_x -= Spaceship._velocity
        elif keys_pressed[self.key_controls["right-key"]]:
            self.pos_x += Spaceship._velocity
        
        return
    
    def load_image(self):
        spaceship_img = pygame.image.load(self.image_dir)
        trans_spaceship_img = pygame.transform.rotate(
            pygame.transform.scale(
                spaceship_img,
                (self.image_transform_attr["width"], self.image_transform_attr["height"])
            ), 
            self.image_transform_attr["rotation"]
        )
        
        return trans_spaceship_img
    
    @property
    def bullets(self):
        return self._bullets
    
    @bullets.setter
    def bullets(self, value):
        if len(value) > Spaceship._max_bullets:
            self._bullets = value[0 : Spaceship._max_bullets]
        return
    
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        if value > Spaceship._max_health:
            self._health = Spaceship._max_health
        elif value < 0:
            self._health = 0
        else:
            self._health = value
    
    def fire_bullets(self, pygame_event, bullet_fire_sound):

        if pygame_event.key == self.key_controls["fire-key"]:
            if self.territory.lower() == "left":
                bullet = pygame.Rect(
                    self.pos_x + self.image_transform_attr["width"],
                    self.pos_y + self.image_transform_attr["height"] // 2 - 2,
                    10,
                    5
                )
            elif self.territory.lower() == "right":
                bullet = pygame.Rect(
                    self.pos_x,
                    self.pos_y + self.image_transform_attr["height"] // 2 - 2,
                    10,
                    5
                )
            self.bullets += [bullet]
            bullet_fire_sound.play()
        return
    
    def handle_bullets(self, opponent, bullet_hit_sound):
        for bullet in opponent.bullets:
            if pygame.Rect(
                    self.pos_x,
                    self.pos_y,
                    self.image_transform_attr["width"], 
                    self.image_transform_attr["height"]
            ).colliderect(bullet):
                bullet_hit_sound.play()
                opponent.bullets.remove(bullet)
                self.health -= 1
            if self.territory.lower() == "right":
                bullet.x += g_c.BULLET_VEL
                if bullet.x > g_c.GAME_WIDTH:
                    opponent.bullets.remove(bullet)
            elif self.territory.lower() == "left":
                bullet.x -= g_c.BULLET_VEL
                if bullet.x < 0:
                    opponent.bullets.remove(bullet)
        return