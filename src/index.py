from tkinter import Tk
from ui.ui import UI



def main():
    window = Tk()
    window.wm_geometry("640x480")
    window.configure(bg='white')
    window.title("My Weather Window")

    ui_view = UI(window)
    ui_view.start()

    window.mainloop()

if __name__ == "__main__":
    main()
