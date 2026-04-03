import time, sys, math, os, shutil, threading, termios, tty, textwrap, psutil
from beep import get_beep_reply, SYSTEM_INSTRUCTION, save_daily_chronicle

# --- КОНФИГУРАЦИЯ ---
ORANGE = "\033[38;5;208m"
WHITE = "\033[37m"
RESET = "\033[0m"
HOME = "\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR = "\033[2J"
ALT_SCREEN_ON = "\033[?1049h"
ALT_SCREEN_OFF = "\033[?1049l"

def mv(r, c): return f"\033[{r};{c}H"

# --- АРТЫ БИПА ---
BEEP_CLOSED_RAW = """
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣬⣭⣤⣤⣤⣴⣦⣤⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣀⠤⠒⣈⡥⠴⠶⠻⣿⡏⠀⠀⠀⠀⠀⠈⢹⡿⠀⠀⠀⠀⠀⠀
⢀⣠⡴⠞⢁⣴⡏⠁⠀⠀⠀⠀⢻⡇⠀⠀⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀
⣾⣏⣀⡴⠋⠙⢷⡄⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀
⠙⠟⠉⠀⠀⠀⠸⣿⠀⠀⠀⠰⠸⡄⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⠀⡀⢰⣿⣦⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣸⡏⠀⠀⠀⠀⢿⡟⠛⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡿⠁⠀⠀⠀⠀⠘⣷⡄⠀⠀⠀⠀⠀⠀⢸⢣⣀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⡇⠀⠀⡴⣋⠓⢦⠹⢗⣤⣤⢤⠀⣀⣀⣉⢸⣿⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠈⢷⡀⠀⡇⣿⡿⢀⠇⣸⡿⠟⠛⠛⠉⠁⠀⠈⠿⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢳⡀⠉⠢⠖⠋⠀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⠧⣁⣀⠀⠀⣠⠸⡀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢼⠱⣿⡀⠈⠉⠉⠙⠆⢻⣀⣀⣤⣀⣀⣼⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⡓⠈⠻⠦⣤⣤⣀⢸⡘⢋⣉⣉⣍⣉⠙⠇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢾⣿⡿⣰⠁⠀⠀⠈⠉⠁⠀⣾⠋⠉⠉⠛⡷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠁⠀⠹⡆⠀⠀⠀⠀⠀⠀⢻⣇⠀⠀⢀⠃⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠘⠿⠷⠮⠧⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡶⢶⣦⣄⡀⠀⣠⡗⠶⢀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⠀⢹⣿⣏⣍⣁⣒⠪⢀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠀⠈⣿⡿⠿⠛⠁⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠸⣿⣧⠀⠀⠀⠘⢠⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣿⣧⣄⡀⠹⣿⣧⡀⠀⠀⣤⡔⣄⠀⠀⠀⠀⠀
⠀⠠⠀⠀⣀⣠⣴⠟⠉⠀⠀⠙⠿⣿⣿⣿⣿⣷⣄⣾⡏⠁⠉⠙⠒⠆⠀⠀
⠀⠀⠠⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
"""
BEEP_OPEN_RAW = """
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣬⣭⣤⣤⣤⣴⣦⣤⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣀⠤⠒⣈⡥⠴⠶⠻⣿⡏⠀⠀⠀⠀⠀⠈⢹⡿⠀⠀⠀⠀⠀⠀
⢀⣠⡴⠞⢁⣴⡏⠁⠀⠀⠀⠀⢻⡇⠀⠀⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀
⣾⣏⣀⡴⠋⠙⢷⡄⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀
⠙⠟⠉⠀⠀⠀⠸⣿⠀⠀⠀⠰⠸⡄⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⠀⡀⢰⣿⣦⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣸⡏⠀⠀⠀⠀⢿⡟⠛⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡿⠁⠀⠀⠀⠀⠘⣷⡄⠀⠀⠀⠀⠀⠀⢸⢣⣀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⡇⠀⠀⡴⣋⠓⢦⠹⢗⣤⣤⢤⠀⣀⣀⣉⢸⣿⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠈⢷⡀⠀⡇⣿⡿⢀⠇⣸⡿⠟⠛⠛⠉⠁⠀⠈⠿⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢳⡀⠉⠢⠖⠋⠀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⠧⣁⣀⠀⠀⣠⠸⡀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢼⠱⣿⡀⠈⠉⠉⠙⠆⢻⣀⣀⣤⣀⣀⣼⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⡓⠈⠻⠦⣤⣤⣀⢸⡘⢋⣉⣉⣍⣉
       ⠙⣤  ⣤⣤⣤ ⣦    ⣦
⠀⠀⠀⠀⠀⢾⣿⡿⣰⠁⠀⠀⠈⠉⠁⠀⣾⠋⠉⠉⠛⡷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠁⠀⠹⡆⠀⠀⠀⠀⠀⠀⢻⣇⠀⠀⢀⠃⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠘⠿⠷⠮⠧⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡶⢶⣦⣄⡀⠀⣠⡗⠶⢀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⠀⢹⣿⣏⣍⣁⣒⠪⢀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠀⠈⣿⡿⠿⠛⠁⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠸⣿⣧⠀⠀⠀⠘⢠⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣿⣧⣄⡀⠹⣿⣧⡀⠀⠀⣤⡔⣄⠀⠀⠀⠀⠀
⠀⠠⠀⠀⣀⣠⣴⠟⠉⠀⠀⠙⠿⣿⣿⣿⣿⣷⣄⣾⡏⠁⠉⠙⠒⠆⠀⠀
⠀⠀⠠⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
"""

# АРТ В ПРАВОМ ВЕРХНЕМ УГЛУ
LANDSCAPE_ART = """
    ⠌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠸⡇⡇⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⢹⡇⢀⣯⡻⠀⠀⠀⠀⣤⠶⢂⠀⠀⠀⢻⣧⠀⠀⠀⠀⠀⡀⡰⠀⠀⠀⠄
    ⠀⠀⠀⠀⠈⡆⢳⠀⠀⠀⠀⠀⠨⠁⣼⡿⠁⠀⠀⠀⠀⢹⣇⠌⠀⠀⠀⢸⣿⠀⢰⠀⠀⠀⠐⡖⠀⠀⠀⠘
    ⠀⠀⠀⠀⠀⢣⣼⠀⠀⠀⠀⠀⠀⣺⠟⠀⠀⠀⠀⠀⠀⠀⢿⠀⠀⠀⠀⠀⡇⠀⠀⠄⠀⠀⠀⡇⠀⠀⠀⢰
    ⠀⠀⠀⠀⠀⠀⢻⠀⠀⠀⠀⠀⢠⡏⠀⠀⠀⠀⠀⠀⡀⠀⠘⡄⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠘
    ⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⢠⠿⠇⠀⠀⠀⠀⠰⣾⣿⣦⠀⠇⠀⠀⠀⢰⡇⠀⠀⢠⠆⠀⠀⡇⠀⠀⠀⠀
    ⡀⠀⠀⠀⠀⠀⢸⠀⠀⠀⣰⠣⢐⠀⠀⠀⠀⠀⡐⣸⣿⠁⠆⢸⡀⠀⠀⢸⣃⠀⠀⠈⠀⠀⢠⣧⠀⠀⠀⠀
⠿⠿⠿⢿⠿⠿⢿ ⣿⣷⡶⣶⣰⣤⣼⣶⣶⣶⢧⣧⢾⣗⣐⢀⣰⣖⣷⣿⣽⣧⣤⣿⠿⡦⢦⣼⢾⠦⠤⡾⠌⠤⠎⠉⣀⠀⢰⣶⠿⠿⠿⢿⠿⠿⠿⢿
⠿⠿⠿⢿⠿⠿⠿⢿⣿⠿⠿⠿⢛⣿⣷⡶⣢⣬⣭⣿⣿⣟⣛⣛⣫⣧⣽⣷⣸⣟⣻⡍⠉⠓⠒⣐⣒⡒⠀⠉⠁⠀⢀⠉⢩⣥⣶⣿⠿⠿⠿⢿⠿⠿⠿⢿
⠿⠿⠿⢿⠿⠿⠿⢿⣯⣭⡤⠤⠶⠶⠒⠛⠻⠿⠿⠷⠚⠓⠾⠷⠖⠒⠒⣿⣾⠶⠶⠛⠀⠀⠀⠋⠉⠉⠉⠉⠽⠟⠻⠿⠿⠿⠿⢿⠿⠿⠿⢿⠿⠿⠿⢿
"""

# Подготовка данных
beep_closed = [l for l in BEEP_CLOSED_RAW.splitlines() if l.strip()]
beep_open = [l for l in BEEP_OPEN_RAW.splitlines() if l.strip()]
landscape = [l for l in LANDSCAPE_ART.splitlines() if l.strip()]

# Глобальное состояние
chat_history = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
displayed_messages = []
user_input_buffer = ""
is_talking = False
is_jumping = False
beep_mood = "НЕЙТРАЛЬНЫЙ"
current_action = "СЛУШАЕТ"

def draw_tile_lines(r, c, w, h, title):
    res = []
    res.append(mv(r, c) + ORANGE + "╭" + (f" {title} ").center(w-2, "─") + "╮")
    for i in range(1, h-1):
        res.append(mv(r + i, c) + "│" + (" " * (w-2)) + "│")
    res.append(mv(r + h - 1, c) + "╰" + ("─" * (w-2)) + "╯" + RESET)
    return res

def draw_frame(lines, scale, flip, max_w):
    if not lines: return []
    h, w = len(lines), max(len(l) for l in lines)
    tw = max(2, int(w * scale))
    cx = w / 2
    out = []
    for row in lines:
        row = row.ljust(w)
        line = "".join(row[int(cx + (j - tw/2) / scale + 0.5)] if 0 <= int(cx + (j - tw/2) / scale + 0.5) < w else " " for j in range(tw))
        if flip: line = line[::-1]
        out.append(line.center(max_w)[:max_w])
    return out

def render_ui():
    global is_talking, user_input_buffer, displayed_messages, is_jumping, beep_mood, current_action
    sys.stdout.write(ALT_SCREEN_ON + HIDE_CURSOR + CLEAR)

    while True:
        cols, rows = shutil.get_terminal_size()
        buffer = []

        left_w = int(cols * 0.5)
        right_w = cols - left_w
        art_h = len(landscape) + 2
        # СТАТУС БАР
        status_bar_h = 3
        input_h = 5
        main_h = rows - input_h
        chat_h = main_h - art_h - status_bar_h

        buffer.extend(draw_tile_lines(1, 1, left_w, main_h, "BEEP-UNIT"))
        buffer.extend(draw_tile_lines(1, left_w + 1, right_w, art_h, "STATION-VIEW"))

        if status_bar_h > 0:
            buffer.extend(draw_tile_lines(art_h + 1, left_w + 1, right_w, status_bar_h, "BEEP-STATUS"))

        buffer.extend(draw_tile_lines(art_h + status_bar_h + 1, left_w + 1, right_w, chat_h, "LOG-STREAM"))
        buffer.extend(draw_tile_lines(main_h + 1, 1, cols, input_h, "COMM-LINK"))

        t = time.time() * 20 if is_jumping else 0
        scale, flip = (0.8 + 0.2 * abs(math.cos(t)), math.cos(t) < 0) if is_jumping else (1.0, False)
        current_source = beep_open if is_talking else beep_closed
        animated_beep = draw_frame(current_source, scale, flip, left_w - 6)
        for i, line in enumerate(animated_beep):
            if i < main_h - 4:
                buffer.append(mv(i + 3, 3) + ORANGE + line)

        for i, line in enumerate(landscape):
            buffer.append(mv(2 + i, left_w + 3) + ORANGE + line[:right_w-4])

        # --- СТАТУС БЕЗ СТИКЕРОВ ---
        if status_bar_h > 0:
            mem = psutil.virtual_memory()
            hp_percent = mem.available * 100 // mem.total
            hp_bar = f"{'#' * (hp_percent // 20)}{'_' * (5 - hp_percent // 20)}"
            status_line = f"MOOD: {beep_mood} | STATUS: {current_action} | VITAL: {hp_bar}"
            buffer.append(mv(art_h + 2, left_w + 3) + ORANGE + status_line[:right_w-6])

        chat_box_h = chat_h - 2
        visible_msgs = displayed_messages[-chat_box_h:]
        for i, msg in enumerate(visible_msgs):
            clean_msg = msg[:right_w-6].ljust(right_w-6)
            buffer.append(mv(art_h + status_bar_h + 2 + i, left_w + 3) + WHITE + clean_msg)

        input_str = f">>> {user_input_buffer}_"
        buffer.append(mv(main_h + 3, 4) + WHITE + input_str.ljust(cols-8))

        sys.stdout.write(HOME + "".join(buffer))
        sys.stdout.flush()
        time.sleep(0.04)

def handle_input():
    global user_input_buffer, is_talking, displayed_messages, chat_history, is_jumping, beep_mood, current_action

    while True:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if ch == '\r': # Enter
            if user_input_buffer.strip():
                msg = user_input_buffer
                user_input_buffer = ""

                is_jumping = "!" in msg

                # --- ИСПРАВЛЕНИЕ ПЕРЕНОСА ДЛЯ ПОЛЬЗОВАТЕЛЯ ---
                cols, _ = shutil.get_terminal_size()
                right_w = (cols - int(cols * 0.5)) - 7

                # Разбиваем длинный текст пользователя на строки
                user_wrapped = textwrap.wrap(f"USER: {msg}", width=right_w - 6)
                for line in user_wrapped:
                    displayed_messages.append(line)
                # --------------------------------------------

                is_talking, current_action = True, "ДУМАЕТ..."
                # ... дальше идет логика настроения и ответа Бипа ...

                is_talking, current_action = True, "ДУМАЕТ..."
                lower_msg = msg.lower()
                if any(w in lower_msg for w in ["круто", "хорош", "лучший", "рад"]): beep_mood = "РАДОСТНЫЙ"
                elif any(w in lower_msg for w in ["плохо", "тупой", "враг", "умри"]): beep_mood = "ЗЛОЙ"
                else: beep_mood = "БОЕВОЙ"

                full_reply, chat_index = "", len(displayed_messages)
                displayed_messages.append("Бип: ...")
                cols, _ = shutil.get_terminal_size()
                right_w = (cols - int(cols * 0.5)) - 7

                try:
                    for chunk in get_beep_reply(msg, chat_history):
                        full_reply += chunk
                        if "!" in chunk: is_jumping = True
                        wrapped = textwrap.wrap(full_reply, width=right_w - 6)
                        if wrapped:
                            while len(displayed_messages) > chat_index: displayed_messages.pop()
                            displayed_messages.append(f"Бип: {wrapped[0]}")
                            for line in wrapped[1:]: displayed_messages.append(f"     {line}")
                except: displayed_messages.append("Бип: Ошибка связи.")

                chat_history.append({"role": "user", "content": msg})
                chat_history.append({"role": "assistant", "content": full_reply})
                is_talking, current_action, is_jumping = False, "СЛУШАЕТ", False

        elif ord(ch) in [8, 127]:
            user_input_buffer = user_input_buffer[:-1]

        elif ord(ch) == 19: # Ctrl+S
            sys.stdout.write(SHOW_CURSOR + ALT_SCREEN_OFF + CLEAR + HOME)
            print(ORANGE + "Бип записывает всё в хроники... БИП!" + RESET)
            save_daily_chronicle(chat_history)
            os._exit(0)

        elif ord(ch) == 3: # Ctrl+C
            sys.stdout.write(SHOW_CURSOR + ALT_SCREEN_OFF + CLEAR + HOME)
            os._exit(0)

        else:
            if ord(ch) >= 32: user_input_buffer += ch

if __name__ == "__main__":
    threading.Thread(target=render_ui, daemon=True).start()
    handle_input()
