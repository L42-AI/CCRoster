import customtkinter


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        # configure window
        self.title("Scheduly")
        self.geometry(f"{1100}x{580}")

        self.mainloop()