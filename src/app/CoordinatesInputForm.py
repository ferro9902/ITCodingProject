import tkinter as tk
import app.DTOs.CoordinatesDTO as CoordinatesDTO


# User Input form to submit coordinates for the Path Finder

class CoordinatesInputForm:

    def __init__(self) -> None:
        self.start = None
        self.dest = None

# form creation method used to define all of the tkinter components and add them to the window
    def create_form(self):
        self.form = tk.Tk()
        self.form.title = "Coordinates input form"

        start_lbl = tk.Label(self.form, text="Partenza")
        start_latitude_lbl = tk.Label(self.form, text="Latitudine:")
        start_longitude_lbl = tk.Label(self.form, text="Longitudine:")
        destination_lbl = tk.Label(self.form, text="Destinazione")
        destination_latitude_lbl = tk.Label(self.form, text="Latitudine:")
        destination_longitude_lbl = tk.Label(self.form, text="Longitudine:")

        self.start_latitude_entry = tk.Entry(self.form)
        self.start_longitude_entry = tk.Entry(self.form)
        self.destination_latitude_entry = tk.Entry(self.form)
        self.destination_longitude_entry = tk.Entry(self.form)

        submit_btn = tk.Button(self.form, text="Invio",
                               command=self.submit_form)

        start_lbl.grid(row=0, column=0, padx=10, pady=5)
        start_latitude_lbl.grid(row=1, column=0, padx=10, pady=5)
        self.start_latitude_entry.grid(row=1, column=1, padx=10, pady=5)
        start_longitude_lbl.grid(row=2, column=0, padx=10, pady=5)
        self.start_longitude_entry.grid(row=2, column=1, padx=10, pady=5)
        destination_lbl.grid(row=0, column=2, padx=10, pady=5)
        destination_latitude_lbl.grid(row=1, column=2, padx=10, pady=5)
        self.destination_latitude_entry.grid(row=1, column=3, padx=10, pady=5)
        destination_longitude_lbl.grid(row=2, column=2, padx=10, pady=5)
        self.destination_longitude_entry.grid(row=2, column=3, padx=10, pady=5)
        submit_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # starting the mainloop to wait for the user submit (stopped in the method submit_dorm)
        self.form.mainloop()

# storing data that will later be accessed by the main method
    def submit_form(self):
        print("submit button pressed")

        self.start = CoordinatesDTO.CoordinatesDTO(
            self.start_latitude_entry.get().strip(), self.start_longitude_entry.get().strip())

        self.dest = CoordinatesDTO.CoordinatesDTO(
            self.destination_latitude_entry.get().strip(), self.destination_longitude_entry.get().strip())

        self.form.destroy()


# TEST
if __name__ == "__main__":
    cif = CoordinatesInputForm()
    cif.create_form()
