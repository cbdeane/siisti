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

        if key == ord('q'):
            break
        elif key == ord('j') and selected < len(items) - 1:
            selected += 1
        elif key == ord('k') and selected > 0:
            selected -= 1
        elif key == ord('a'):
            new_item = ""
            while (len(new_item) < 1):
                curses.echo()
                stdscr.addstr(height - 1, 0, "Enter new item: ")
                stdscr.timeout(-1)
                new_item = stdscr.getstr(height - 1, 15, 100).decode('utf-8')
                items.append(new_item)
                curses.noecho()
        elif key == ord('s') and items:
            items.pop(selected)
            if selected >= len(items):
                selected = len(items) - 1
        elif key == ord(' '):
            if items[selected].endswith(completed_suffix):
                completed.remove(items[selected])
                items[selected] = items[selected].replace(completed_suffix, "")
            else:
                items[selected] += completed_suffix
                completed.append(items[selected])
                items.append(items.pop(selected))
            if selected >= len(items):
                selected = len(items) - 1
        elif key == ord('h') and selected > 0:
            items[selected], items[selected - 1] = items[selected - 1], items[selected]
            selected -= 1
        elif key == ord('l') and selected < len(items) - 1:
            items[selected], items[selected + 1] = items[selected + 1], items[selected]
            selected += 1
        elif key == ord('e'):
            curses.echo()
            stdscr.addstr(height - 1, 0, "Enter new name: ")
            new_name = stdscr.getstr(height - 1, 15, 100).decode('utf-8')
            items[selected] = new_name
            curses.noecho()

        save_items('items.txt', items)
        stdscr.refresh()

curses.wrapper(main)