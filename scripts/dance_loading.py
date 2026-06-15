import sys
import subprocess
import curses
import time
import os
import re
import select
from collections import deque
import threading
import signal

# ASCII Breakdancing Cat Frames (custom multi-frame animation)
CAT_FRAMES = [
    [
        r"      /\_/\     ",
        r"     ( o.o )    ",
        r"      > ^ <     ",
        r"     /  |  \    ",
        r"    / / | \ \   ",
        r"   (__)_|_(__)  "
    ],
    [
        r"      /\_/\     ",
        r"     ( -.- )    ",
        r"      > ^ <     ",
        r"    //  |  \\   ",
        r"   // / | \ \\  ",
        r"  (__/ _|_ \__) "
    ],
    [
        r"      /\_/\     ",
        r"     ( o.o )    ",
        r"     / > < \    ",
        r"    / / | \ \   ",
        r"    \ \ | / /   ",
        r"   __\_\|/_/__  "
    ],
    [
        r"      /\_/\     ",
        r"     ( >.< )    ",
        r"      > ^ <     ",
        r"     \  |  /    ",
        r"      \ | /     ",
        r"     (__|__)    "
    ],
    [
        r"  \    /\_/\  / ",
        r"   \  ( o.o )/  ",
        r"    \  > ^ </   ",
        r"     \__|_|__   ",
        r"       / | \    ",
        r"      (__|__)   "
    ]
]

# ANSI escape code parser
ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def strip_ansi(line: str) -> str:
    return ANSI_RE.sub('', line)

def parse_ansi_colors(line: str):
    """
    Given a string with ANSI color codes, returns a list of (color_code, text) tuples.
    Default color_code is 0.
    """
    parts = []
    current_color = 0 # Default curses pair

    # Simple mapping of ANSI color codes to curses colors
    # 31: red, 32: green, 33: yellow, 34: blue, 36: cyan, 0: default
    color_map = {
        '31': 1, # Red
        '32': 2, # Green
        '33': 3, # Yellow
        '34': 4, # Blue
        '36': 5, # Cyan
        '0': 0   # Default
    }

    idx = 0
    while idx < len(line):
        match = ANSI_RE.search(line, idx)
        if not match:
            parts.append((current_color, line[idx:]))
            break

        start, end = match.span()
        if start > idx:
            parts.append((current_color, line[idx:start]))

        code_str = match.group()[2:-1] # remove \x1b[ and m
        codes = code_str.split(';')
        for code in codes:
            if code in color_map:
                current_color = color_map[code]
            elif code.startswith('1;'):
                # Bold variants or something else, handle basically
                c = code.replace('1;', '')
                if c in color_map:
                    current_color = color_map[c]

        idx = end

    return parts

class DanceLoadingUI:
    def __init__(self, stdscr, bootstrap_args):
        self.stdscr = stdscr
        self.bootstrap_args = bootstrap_args
        self.lines = deque(maxlen=200) # Keep history of last 200 log lines
        self.running = True
        self.frame_idx = 0
        self.start_time = time.time()
        self.return_code = 0
        self.lock = threading.Lock()

        # Setup curses
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0) # Hide cursor
        self.stdscr.nodelay(1) # Non-blocking input

        # Initialize color pairs
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)
        curses.init_pair(5, curses.COLOR_CYAN, -1)
        curses.init_pair(6, curses.COLOR_WHITE, -1)

    def read_process_output(self, proc):
        # We need to read line by line without blocking the UI
        # Use selector or simply run in a thread
        for line in iter(proc.stdout.readline, b''):
            try:
                decoded = line.decode('utf-8').rstrip('\r\n')
                with self.lock:
                    self.lines.append(decoded)
            except Exception:
                pass

        proc.stdout.close()
        proc.wait()
        self.return_code = proc.returncode
        self.running = False

    def draw_cat(self, max_y, max_x):
        cat_art = CAT_FRAMES[self.frame_idx]
        cat_h = len(cat_art)
        cat_w = max(len(row) for row in cat_art)

        start_y = 2
        start_x = max(0, (max_x - cat_w) // 2)

        for i, row in enumerate(cat_art):
            if start_y + i < max_y:
                # Color the cat dynamically
                color = curses.color_pair( (self.frame_idx % 5) + 1 )
                try:
                    self.stdscr.addstr(start_y + i, start_x, row, color | curses.A_BOLD)
                except curses.error:
                    pass

    def draw_starwars_text(self, max_y, max_x):
        # Star wars perspective
        # The text is drawn from the bottom up, shrinking margins as it goes up.
        # We only draw text below the cat.

        cat_bottom_y = 2 + len(CAT_FRAMES[0]) + 2
        available_height = max_y - cat_bottom_y - 2

        if available_height <= 0:
            return

        with self.lock:
            # We want to animate the scrolling.
            # Base offset on time so it scrolls smoothly.
            elapsed = time.time() - self.start_time
            scroll_offset = elapsed * 5 # rows per second

            # Start from the latest lines and work backwards
            lines_to_draw = list(self.lines)

        if not lines_to_draw:
            return

        # Add some empty lines at the end to create the continuous scroll effect
        lines_to_draw = lines_to_draw + [""] * 10

        # Determine the subset of lines visible in the viewport
        # The bottom of the screen corresponds to the latest index + scroll fraction
        total_lines = len(lines_to_draw)

        # We'll calculate a virtual Y coordinate for each line
        # Virtual Y = 0 is the very bottom of the screen.
        for i in range(total_lines):
            line_idx = total_lines - 1 - i
            raw_line = lines_to_draw[line_idx]

            # Distance from the bottom of the visible stream
            # The newest line starts at bottom (y_offset = 0) and moves up
            # Actually, we want to see the latest line at the bottom, moving upwards.
            # Let's map i (distance from latest) and scroll_offset.
            y_pos_float = i - scroll_offset + len(lines_to_draw) # Adjust to make it scroll
            # Simplification: let's just make a smooth crawler of the last N lines

        # Simplified scroller:
        # We just take the last 'available_height' lines. To scroll, we can introduce a fraction offset.
        scroll_fraction = int(scroll_offset) % max(1, len(lines_to_draw))
        visible_lines = lines_to_draw[-available_height - scroll_fraction:] if len(lines_to_draw) > available_height else lines_to_draw

        # Actually, let's just draw the last N lines and let them natively push up as new logs come in.
        # For the star wars effect, we compress the width as we go up.

        draw_lines = lines_to_draw[-available_height:]

        for i, raw_line in enumerate(draw_lines):
            # i = 0 is top of the text area (furthest away), i = available_height-1 is bottom (closest)
            y = cat_bottom_y + i

            # Perspective effect: wider at bottom, narrower at top
            # Perspective ratio from 0.0 (top) to 1.0 (bottom)
            if available_height > 1:
                ratio = i / (available_height - 1)
            else:
                ratio = 1.0

            # Base width max at bottom, shrinks to maybe 50% at top
            # We pad the sides with spaces, essentially truncating the center string
            max_line_width = int(max_x * (0.4 + 0.6 * ratio))

            clean_text = strip_ansi(raw_line)
            if not clean_text:
                continue

            # Truncate if too long for perspective
            if len(clean_text) > max_line_width:
                # We need to truncate the ANSI-parsed components, which is tricky.
                # For simplicity, if it's too long, we just center the stripped text and color it default.
                # But we want to preserve colors! Let's do a best effort.
                pass

            parts = parse_ansi_colors(raw_line)

            # Calculate total length
            total_len = sum(len(text) for _, text in parts)

            # Center x
            start_x = max(0, (max_x - total_len) // 2)

            # Draw parts
            curr_x = start_x
            for color_idx, text in parts:
                if curr_x >= max_x:
                    break
                try:
                    # Don't draw past max_x
                    draw_text = text[:max_x - curr_x]
                    color_pair = curses.color_pair(color_idx)
                    if ratio < 0.3:
                        # Dim furthest text (using default or lower intensity if possible, we'll just drop bold)
                        attr = color_pair
                    else:
                        attr = color_pair | curses.A_BOLD
                    self.stdscr.addstr(y, curr_x, draw_text, attr)
                    curr_x += len(draw_text)
                except curses.error:
                    pass

    def run(self):
        # Start bootstrap.sh in the background
        cmd = ["bash", "bootstrap.sh"] + self.bootstrap_args

        # We set an env var so bootstrap.sh knows it's the child process
        env = os.environ.copy()
        env['BOOTSTRAP_IS_DANCING_CHILD'] = "1"

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env
        )

        # Start reading thread
        reader_thread = threading.Thread(target=self.read_process_output, args=(proc,))
        reader_thread.daemon = True
        reader_thread.start()

        # UI Loop
        fps = 10
        frame_time = 1.0 / fps

        while self.running:
            loop_start = time.time()

            # Check for quit
            c = self.stdscr.getch()
            if c == ord('q'):
                proc.terminate()
                break

            self.stdscr.clear()
            max_y, max_x = self.stdscr.getmaxyx()

            self.draw_cat(max_y, max_x)
            self.draw_starwars_text(max_y, max_x)

            # Add a title
            title = " BOOTSTRAPPING PIPECAT... "
            try:
                self.stdscr.addstr(0, max(0, (max_x - len(title)) // 2), title, curses.color_pair(3) | curses.A_BOLD)
            except curses.error:
                pass

            self.stdscr.refresh()

            # Advance frame every few loops to not make the cat too fast
            if int(time.time() * 5) % 2 == 0:
                 pass # slow down by relying on time for frame
            self.frame_idx = int(time.time() * 8) % len(CAT_FRAMES)

            # Sleep to maintain fps
            elapsed = time.time() - loop_start
            if elapsed < frame_time:
                time.sleep(frame_time - elapsed)

        proc.wait()
        return proc.returncode

def main(stdscr):
    args = sys.argv[1:]
    ui = DanceLoadingUI(stdscr, args)
    return ui.run()

if __name__ == "__main__":
    # Hide traceback if interrupted
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        ret = curses.wrapper(main)
        sys.exit(ret)
    except Exception as e:
        print(f"Dancing UI encountered an error: {e}")
        sys.exit(1)