import pygame as pg

from .encoder import generate_frames


def run():
    with open("poetry.lock", "rb") as file:
        data = file.read()

    frames = [pg.surfarray.make_surface(frame) for frame in generate_frames(data)]
    frame_width = frames[0].get_width()

    margin = 10
    top_margin = 20
    window_size = (
        2 * frame_width + 3 * margin,
        2 * frame_width + 3 * margin + top_margin,
    )

    frame_positions = [
        (margin, margin + top_margin),
        (frame_width + 2 * margin, frame_width + 2 * margin + top_margin),
        (margin, frame_width + 2 * margin + top_margin),
        (frame_width + 2 * margin, margin + top_margin),
    ]

    pg.init()
    display = pg.display.set_mode(window_size)
    pg.display.set_caption("QR Sender")

    font = pg.font.Font(pg.font.get_default_font(), 12)
    clock = pg.time.Clock()

    next_frame_event = pg.USEREVENT
    pg.time.set_timer(next_frame_event, 500)

    cursor = 0
    even = True

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            elif event.type == next_frame_event:
                cursor += 2
                cursor %= len(frames)
                even = not even

        display.fill(pg.Color("white"))

        fps = f"FPS: {str(int(clock.get_fps()))}"
        display.blit(font.render(fps, True, pg.Color("black")), (5, 5))

        for i in range(2):
            pos = i if even else i + 2
            display.blit(frames[cursor + i], frame_positions[pos])

        pg.display.flip()
        clock.tick(60)

    pg.quit()
