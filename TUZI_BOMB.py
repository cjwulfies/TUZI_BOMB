#!/usr/bin/env python3
"""gifbomb - pop N windows all looping the same GIF. Esc closes a window, Ctrl+Q quits all."""
import argparse
import os
import random
import sys

import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

MIN_FRAME_MS = 20
BG = "#0b0b0b"


def resource_path(name):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(base, name), os.path.join(here, name)):
        if os.path.isfile(cand):
            return cand
    return None


class Window:
    def __init__(self, app, scale, x, y):
        self.app = app
        self.job = None
        self.alive = True
        w, h = app.size(scale)
        self.top = tk.Toplevel(app.root)
        self.top.title(app.title)
        self.top.configure(bg=BG)
        self.top.resizable(False, False)
        self.top.geometry(f"{w}x{h}+{x}+{y}")
        if app.topmost:
            self.top.attributes("-topmost", True)
        self.label = tk.Label(self.top, bg=BG, bd=0)
        self.label.pack(fill="both", expand=True)
        self.imgs = app.render(scale)
        self.i = random.randrange(len(self.imgs))
        self.top.bind("<Escape>", lambda e: self.close())
        self.top.bind("q", lambda e: self.close())
        self.top.protocol("WM_DELETE_WINDOW", self.close)
        self.top.after(random.randint(0, app.stagger), self.tick)

    def tick(self):
        if not self.alive:
            return
        self.label.configure(image=self.imgs[self.i])
        d = self.app.delays[self.i]
        self.i = (self.i + 1) % len(self.imgs)
        self.job = self.top.after(d, self.tick)

    def close(self):
        if not self.alive:
            return
        self.alive = False
        if self.job:
            self.top.after_cancel(self.job)
        self.top.destroy()
        self.app.forget(self)


class App:
    def __init__(self, args):
        gif = args.gif or resource_path("reaction.gif")
        if not gif:
            sys.exit("reaction.gif not found next to the executable.")
        self.base, self.delays = [], []
        for frame in ImageSequence.Iterator(Image.open(gif)):
            self.delays.append(max(MIN_FRAME_MS, int(frame.info.get("duration", 100) or 100)))
            self.base.append(frame.convert("RGBA"))
        if not self.base:
            sys.exit("That GIF has no frames.")

        self.title = args.title
        self.topmost = args.topmost
        self.stagger = args.stagger
        self.windows = []

        self.root = tk.Tk()
        self.root.withdraw()
        self.root.bind_all("<Control-q>", lambda e: self.root.destroy())

        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()

        count = max(1, args.count)
        cols = max(1, self.sw // 520)
        rows = max(1, self.sh // 320)
        cells = [(c, r) for r in range(rows) for c in range(cols)]
        random.shuffle(cells)

        for n in range(count):
            scale = random.uniform(args.min_scale, args.max_scale)
            w, h = self.size(scale)
            cx, cy = cells[n % len(cells)]
            x = min(max(0, cx * 520 + random.randint(-60, 60)), max(0, self.sw - w))
            y = min(max(0, cy * 320 + random.randint(-40, 40)), max(0, self.sh - h))
            self.windows.append(Window(self, scale, x, y))

        self.root.mainloop()

    def size(self, scale):
        w = int(self.base[0].width * scale)
        h = int(self.base[0].height * scale)
        return max(40, min(w, int(self.sw * 0.95))), max(40, min(h, int(self.sh * 0.95)))

    def render(self, scale):
        if abs(scale - 1.0) < 0.01:
            frames = self.base
        else:
            frames = [f.resize(self.size(scale), Image.LANCZOS) for f in self.base]
        return [ImageTk.PhotoImage(f) for f in frames]

    def forget(self, win):
        if win in self.windows:
            self.windows.remove(win)
        if not self.windows:
            self.root.destroy()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("count", nargs="?", type=int, default=7)
    p.add_argument("--gif", help="path to a .gif")
    p.add_argument("--min-scale", type=float, default=0.45)
    p.add_argument("--max-scale", type=float, default=1.0)
    p.add_argument("--stagger", type=int, default=900, help="max ms delay before a window starts")
    p.add_argument("--title", default="gifbomb")
    p.add_argument("--topmost", action="store_true")
    args = p.parse_args()

    if not os.environ.get("DISPLAY"):
        sys.exit("DISPLAY is not set. Reconnect with:  ssh -C -Y user@host   (and see README)")
    App(args)


main()
