import tkinter as tk
import ctypes

user32 = ctypes.windll.user32
GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004
SWP_FRAMECHANGED = 0x0020


def show_in_taskbar(hwnd: int) -> None:
    """Ensure the window appears in the taskbar by adjusting extended styles."""
    ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ex_style &= ~WS_EX_TOOLWINDOW
    ex_style |= WS_EX_APPWINDOW
    user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)
    user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                        SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)


root = tk.Tk()
# Remove default window decorations to use a custom title bar
root.overrideredirect(True)
# Apply the fix so the window still appears in the taskbar
show_in_taskbar(root.winfo_id())

# Simple custom title bar frame
title_bar = tk.Frame(root, bg="gray", relief="raised", bd=2)

def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

label = tk.Label(title_bar, text="Custom Title Bar", bg="gray")
close_btn = tk.Button(title_bar, text="X", command=root.destroy, bg="gray")

label.pack(side=tk.LEFT, padx=5)
close_btn.pack(side=tk.RIGHT)
title_bar.pack(fill=tk.X)

# Bind motion for dragging the window
title_bar.bind("<ButtonPress-1>", start_move)
title_bar.bind("<ButtonRelease-1>", stop_move)
title_bar.bind("<B1-Motion>", do_move)

# Main content area
main_frame = tk.Frame(root, bg="white", width=300, height=200)
main_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
