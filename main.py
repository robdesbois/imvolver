import pygame
import control


def main():
    pygame.init()

    controller = control.Control()
    controller.run()


if __name__ == "__main__":
    main()