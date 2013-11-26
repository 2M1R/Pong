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


def run():
    sdl2ext.init()
    window = sdl2ext.Window("Pong Game", size=(1280, 720))
    window.show()

    world = sdl2ext.World()

    spriterenderer = SoftwareRenderer(window)
    world.add_system(spriterenderer)

    factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
    sp_paddle1 = factory.from_color(WHITE, size=(20, 100))
    sp_paddle2 = factory.from_color(WHITE, size=(20, 100))

    player1 = Player(world, sp_paddle1, 0, 250)
    player2 = Player(world, sp_paddle2, 1255, 250)

    running = True
    while running:
        events = sdl2ext.get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
                break
        world.process()
    return 0


if __name__ == "__main__":
    sys.exit(run())

