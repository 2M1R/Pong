import sys

try:
    import sdl2.ext as sdl2ext
except ImportError:
    import traceback

    traceback.print_exc()
    sys.exit(1)


def run():
    sdl2ext.init()
    window = sdl2ext.Window("Pong Game", size=(1280, 720))
    window.show()
    running = True
    while running:
        events = sdl2ext.get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
                break
        window.refresh()
    return 0


if __name__ == "__main__":
    sys.exit(run())

