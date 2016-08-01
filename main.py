import pygame
import control


def main():
    pygame.init()

    controller = control.Control()
    controller.run( "/home/rob/Desktop/Bart_Simpson_200px.png" )


if __name__ == "__main__":
    main()