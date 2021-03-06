import os

# Hide pygame advertisement
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame as pg  # noqa: E402 isort:skip


class App:
    MARGIN = 10

    def __init__(self, frames, frequency=8):
        self.frames = [pg.surfarray.make_surface(frame) for frame in frames]
        self.count = len(self.frames)

        self.frequency = frequency

        frame_width = self.frames[0].get_width()

        self.window_size = (
            2 * frame_width + 3 * App.MARGIN,
            2 * frame_width + 4 * App.MARGIN,
        )

        self.positions = [
            (App.MARGIN, 2 * App.MARGIN),
            (frame_width + 2 * App.MARGIN, frame_width + 3 * App.MARGIN,),
            (App.MARGIN, frame_width + 3 * App.MARGIN),
            (frame_width + 2 * App.MARGIN, 2 * App.MARGIN),
        ]

        self.running = False

        self.cursor_a = 0
        self.cursor_b = 1

        self.even = True

        self.display = None
        self.font = None
        self.clock = None
        self.frame_event = pg.USEREVENT

    def run(self):
        pg.init()
        self.display = pg.display.set_mode(self.window_size)
        pg.display.set_caption("QR Sender")

        self.font = pg.font.Font(pg.font.get_default_font(), 12)
        self.clock = pg.time.Clock()

        if self.count > 2:
            pg.time.set_timer(self.frame_event, 1000 // self.frequency)

        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.type == self.frame_event:
                    self.cursor_a = (self.cursor_a + 2) % self.count
                    self.cursor_b = (self.cursor_b + 2) % self.count
                    self.even = not self.even

            self.display.fill((255, 255, 255))

            fps = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (0, 0, 0))
            self.display.blit(fps, (self.window_size[0] - 60, 5))

            info = self.font.render(
                f"QR: {self.cursor_a + 1}/{self.count}", True, (0, 0, 0),
            )
            self.display.blit(info, (5, 5))

            if self.cursor_a < self.count:
                self.display.blit(
                    self.frames[self.cursor_a], self.positions[0 if self.even else 2]
                )

            if self.cursor_b < self.count:
                self.display.blit(
                    self.frames[self.cursor_b], self.positions[1 if self.even else 3]
                )

            pg.display.flip()
            self.clock.tick(60)

        pg.quit()
