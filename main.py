import curses
import os

def load_items(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    return []

def save_items(filename, items):
    with open(filename, 'w') as file:
        for item in items:
            file.write(item + '\n')

def main(stdscr):
    curses.use_default_colors()
    stdscr.border()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(200)
    
    items = load_items('items.txt')
    selected = 0
    completed = []
    completed_suffix = " (completed)"
    
    for item in items:
        if item.endswith(completed_suffix):
            items.remove(item)

    while True:
        stdscr.clear()
        stdscr.border()
        height, width = stdscr.getmaxyx()
        for idx, item in enumerate(items):
            x = width // 2 - len(item) // 2
            y = height // 2 - len(items) // 2 + (idx * 2)
            if idx == selected:
                stdscr.attron(curses.A_REVERSE)
            if item in completed:
                stdscr.attron(curses.A_DIM)
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.A_DIM)
            else:
                stdscr.addstr(y, x, item)
            if idx == selected:
                stdscr.attroff(curses.A_REVERSE)
        
        key = stdscr.getch()
        
        # Keybind q for quit
        if key == ord('q'):
            break

        # Keybind j for move down
        elif key == ord('j') and selected < len(items) - 1:
            selected += 1

        # Keybind k for move up
        elif key == ord('k') and selected > 0:
            selected -= 1

        # Keybind a for append new item
        elif key == ord('a'):
            new_item = ""
            while (len(new_item) < 1):
                curses.echo()
                stdscr.addstr(height - 2, 1, "Enter new item: ")
                stdscr.timeout(-1)
                new_item = stdscr.getstr(height - 2, 17, 100).decode('utf-8')
                items.append(new_item)
                curses.noecho()

        # Keybind s for subtract new item
        elif key == ord('s') and items:
            items.pop(selected)
            if selected >= len(items):
                selected = len(items) - 1

        # Keybind SPACE for toggle complete/incomplete
        elif key == ord(' '):
            if items[selected].endswith(completed_suffix):
                completed.remove(items[selected])
                items[selected] = items[selected].replace(completed_suffix, "")
                items.insert(0, items.pop(selected))
            else:
                items[selected] += completed_suffix
                completed.append(items[selected])
                items.append(items.pop(selected))
            if selected >= len(items):
                selected = len(items) - 1

        # Keybind h for move item up
        elif key == ord('h') and selected > 0:
            items[selected], items[selected - 1] = items[selected - 1], items[selected]
            selected -= 1

        # Keybind l for move item down
        elif key == ord('l') and selected < len(items) - 1:
            items[selected], items[selected + 1] = items[selected + 1], items[selected]
            selected += 1

        # Keybind r for replace
        elif key == ord('r'):
            curses.echo()
            stdscr.addstr(height - 2, 1, "Enter new name: ")
            stdscr.timeout(-1)
            new_name = stdscr.getstr(height - 2, 17, 100).decode('utf-8')
            items[selected] = new_name
            curses.noecho()

        save_items('items.txt', items)
        stdscr.refresh()

curses.wrapper(main)
