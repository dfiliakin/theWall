# import pygame package
import pygame
import logging
from field.field import Field
from game.game import Game

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


def main():
    field = Field(w=10, h=10, cell_size=34)
    game = Game(field=field)

    pygame.init()

    window = pygame.display.set_mode(
        (field.w * field.cell_size, field.h * field.cell_size + 100)
    )
    window.fill("white")

    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    font = pygame.font.SysFont("Comic Sans MS", 30)

    # keep game running till running is true
    field.draw(surface=window)

    running = True
    while running:

        # Check for event if user has pushed
        # any event in queue
        for event in pygame.event.get():

            # if event is of type quit then set
            # running bool to false
            if event.type == pygame.QUIT:
                running = False

            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP and game.is_going:
                pos = pygame.mouse.get_pos()
                player_moved, x, y = game.move(pos)
                logging.info(f"Player{player_moved}: {x, y}")
                if player_moved:
                    sprite = game.player_sprites.get(player_moved)
                    window.blit(sprite, game.grid_to_pos(x, y))
                    winner = game.check_win_condition_around(x, y)
                    if winner:
                        text_surface = font.render(
                            f"Player{winner} won!", False, (0, 0, 0)
                        )
                        window.blit(text_surface, (10, field.h * field.cell_size + 10))

        # Update our window
        pygame.display.flip()


if __name__ == "__main__":
    main()
