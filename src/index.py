from tkinter import Tk
from ui.ui import UI


def main():
    window = Tk()
    window.wm_geometry("640x480")
    window.title("My Weather Window")
    window.configure(background="LightBlue1")

    ui_view = UI(window)
    ui_view.start()

    window.mainloop()


print("MAIN\n")

if __name__ == "__main__":
    main()
