import sys

try:
    from sdl2 import *
    import sdl2.ext as sdl2ext
except ImportError:
    import traceback

    traceback.print_exc()
    sys.exit(1)

WHITE = sdl2ext.Color(255, 255, 255)

class SoftwareRenderer(sdl2ext.SoftwareSpriteRenderer):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2ext.fill(self.surface, sdl2ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)

class Player(sdl2ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()


class MovementSystem(sdl2ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = (Velocity, sdl2ext.Sprite)
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            swidth, sheight = sprite.size
            sprite.x += velocity.vx
            sprite.y += velocity.vy

            sprite.x = max(self.minx, sprite.x)
            sprite.y = max(self.miny, sprite.y)

            pmaxx = sprite.x + swidth
            pmaxy = sprite.y + sheight
            if pmaxx > self.maxx:
                sprite.x = self.maxx - swidth
            if pmaxy > self.maxy:
                sprite.y = self.maxy - sheight


class CollisionSystem(sdl2ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(CollisionSystem, self).__init__()
        self.componenttypes = (Velocity, sdl2ext.Sprite)
        self.ball = None
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def _overlap(self, item):
        pos, sprite = item[0], item[1]
        if sprite == self.ball.sprite:
            return False

        left, top, right, bottom = sprite.area
        bleft, btop, bright, bbottom = self.ball.sprite.area

        return bleft < right and bright > left and \
               btop < bottom and bbottom > top

    def process(self, world, componentsets):
        collitems = [comp for comp in componentsets if self._overlap(comp)]
        if len(collitems) != 0:
            self.ball.velocity.vx = -self.ball.velocity.vx


class Velocity(object):
    def __init__(self):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0


class Ball(sdl2ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()


def run():
    sdl2ext.init()
    window = sdl2ext.Window("Pong Game", size=(1280, 720))
    window.show()

    world = sdl2ext.World()

    collision = CollisionSystem(0, 0, 1280, 720)
    movement = MovementSystem(0, 0, 1280, 720)
    spriterenderer = SoftwareRenderer(window)

    world.add_system(movement)
    world.add_system(collision)
    world.add_system(spriterenderer)

    factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
    sp_paddle1 = factory.from_color(WHITE, size=(20, 100))
    sp_paddle2 = factory.from_color(WHITE, size=(20, 100))
    sp_ball = factory.from_color(WHITE, size=(20, 20))

    player1 = Player(world, sp_paddle1, 0, 250)
    player2 = Player(world, sp_paddle2, 1255, 250)
    ball = Ball(world, sp_ball, 300, 290)
    collision.ball = ball
    ball.velocity.vx = -3

    running = True
    while running:
        events = sdl2ext.get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
                break
            if event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_UP:
                    player1.velocity.vy = -3
                elif event.key.keysym.sym == SDLK_DOWN:
                    player1.velocity.vy = 3
            elif event.type == SDL_KEYUP:
                if event.key.keysym.sym in (SDLK_UP, SDLK_DOWN):
                    player1.velocity.vy = 0
        SDL_Delay(10)
        world.process()
    return 0


if __name__ == "__main__":
    sys.exit(run())

