import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox



import st_year
import nd_year
import rd_year
import th_year
import st_myear
import nd_myear


year_mapping = {
    "BTECH 1 SEM": (st_year.batcher, "BTECH 1 SEM"),
    "BTECH 3 SEM": (nd_year.batcher, "BTECH 3 SEM"),
    "BTECH 5 SEM": (rd_year.batcher, "BTECH 5 SEM"),
    "BTECH 7 SEM": (th_year.batcher, "BTECH 7 SEM"),
    "MTECH-MSc 1 SEM": (st_myear.batcher, "MTECH-MSc 1 SEM"),
    "MTECH-MSc 3 SEM": (nd_myear.batcher, "MTECH-MSc 3 SEM"),
}

# Time and day constants
time_slot = [
    '09:00 AM - 09:55 AM',
    '10:00 AM - 10:55 AM',
    '11:00 AM - 11:55 AM',
    '12:00 PM - 12:55 PM',
    '01:00 PM - 01:55 PM',
    '02:00 PM - 02:55 PM',
    '03:00 PM - 03:55 PM',
    '04:00 PM - 04:55 PM'
]
date_mapping = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]

# Tkinter App
class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("University Timetable Generator")


        # Variables
        self.selected_year = tk.StringVar()
        self.selected_batch = tk.StringVar()
        self.batch_list = []

        # Widgets for selecting year
        ttk.Label(root, text="Select Year/Semester:").grid(row=0, column=0, padx=10, pady=10)
        self.year_combobox = ttk.Combobox(root, textvariable=self.selected_year, state="readonly")
        self.year_combobox['values'] = list(year_mapping.keys())
        self.year_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.year_combobox.bind("<<ComboboxSelected>>", self.load_batches)

        # Widgets for selecting batch
        ttk.Label(root, text="Select Batch:").grid(row=1, column=0, padx=10, pady=10)
        self.batch_combobox = ttk.Combobox(root, textvariable=self.selected_batch, state="readonly")
        self.batch_combobox.grid(row=1, column=1, padx=10, pady=10)

        # Button to generate timetable
        ttk.Button(root, text="Show Timetable", command=self.show_timetable).grid(row=2, column=0, columnspan=2, pady=20)

    def load_batches(self, event):
        """Load batches dynamically based on selected year/semester."""
        year = self.selected_year.get()
        if year in year_mapping:
            batcher, _ = year_mapping[year]
            self.batch_list = batcher()
            self.batch_combobox['values'] = self.batch_list

    def show_timetable(self):
        """Display the timetable in a grid layout."""
        year = self.selected_year.get()
        batch = self.selected_batch.get()

        if not year or not batch:
            messagebox.showwarning("Missing Information", "Please select both a year and a batch.")
            return

        try:
            # Load the Excel sheet
            _, sheet_identifier = year_mapping[year]
            excel = pd.read_excel("C:/Users/thaku/Downloads/ODDSEM2024.xls", sheet_name=sheet_identifier)

            # Generate timetable data
            x = [1, 17, 33, 49, 65, 81, 97]
            y = list(range(1, 9))
            timetable_data = []

            for day_index in range(len(x) - 1):
                row = []
                for slot in y:
                    class_found = False
                    for row_index in range(x[day_index], x[day_index + 1]):
                        if isinstance(excel.iloc[row_index, slot], str) and batch in excel.iloc[row_index, slot]:
                            row.append(excel.iloc[row_index, slot])
                            class_found = True
                            break
                    if not class_found:
                        row.append("No class")
                timetable_data.append(row)

            # Create a new window to display the timetable
            timetable_window = tk.Toplevel(self.root)
            timetable_window.title(f"Timetable for {batch}")
            timetable_window.geometry("2560x1400")

            # Create a grid to display the timetable
            # Header Row
            for col_index, slot in enumerate(["DAY"] + time_slot):
                label = tk.Label(
                    timetable_window,
                    text=slot,
                    font=("Arial", 10, "bold"),
                    bg="lightgray",
                    width=20,  # Increased width for each column
                    height=2,  # Adjusted height for better spacing
                    borderwidth=1,
                    relief="solid",
                    padx=10,  # Increased padding inside the cells
                    pady=10  # Increased padding inside the cells
                )
                label.grid(row=0, column=col_index, sticky="nsew")

            # Data Rows
            for row_index, day in enumerate(date_mapping[:len(timetable_data)]):
                # Day label
                day_label = tk.Label(
                    timetable_window,
                    text=day,
                    font=("Arial", 10),
                    bg="white",
                    width=20,
                    height=2,
                    borderwidth=1,
                    relief="solid",
                    padx=10,
                    pady=10
                )
                day_label.grid(row=row_index + 1, column=0, sticky="nsew")

                # Time slots
                for col_index, slot in enumerate(timetable_data[row_index]):
                    cell_label = tk.Label(
                        timetable_window,
                        text=slot,
                        font=("Arial", 10),
                        bg="white",


                        width=20,  # Increased width for each column
                        height=2,  # Adjusted height for better spacing
                        borderwidth=1,
                        relief="solid",
                        padx=10,  # Increased padding inside the cells
                        pady=10  # Increased padding inside the cells
                    )
                    cell_label.grid(row=row_index + 1, column=col_index + 1, sticky="nsew")

        except FileNotFoundError:
            messagebox.showerror("Error", "File not found. Please check the file path.")
        except ValueError:
            messagebox.showerror("Error", "Invalid sheet name. Please check the sheet names in the Excel file.")


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()
