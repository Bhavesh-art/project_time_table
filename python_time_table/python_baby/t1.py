import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

# Import year-related modules
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
        root.configure(bg="lightblue")
        ttk.Label(root, text="Welcome to the Timetable App!",
                  font=("Georgia", 20, "bold"), background="lightblue").grid(row=0, column=0, columnspan=2, pady=20)

        # Variables
        self.selected_year = tk.StringVar()
        self.selected_batch = tk.StringVar()
        self.batch_list = []
        style = ttk.Style()
        style.configure("TButton",
                        font=("Times New Roman", 14, "bold"),
                        padding=10,
                        background="lightblue",  # Background color
                        foreground="orange")  # Text color
        # Widgets for selecting year
        ttk.Label(root, text="Select Year/Semester:",font=("Georgia",14,"bold")).grid(row=1, column=0, padx=10, pady=10)
        self.year_combobox = ttk.Combobox(root, textvariable=self.selected_year, state="readonly")
        self.year_combobox['values'] = list(year_mapping.keys())
        self.year_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.year_combobox.bind("<<ComboboxSelected>>", self.load_batches)

        # Widgets for selecting batch
        ttk.Label(root, text="Select Batch:",font=("Georgia",14,"bold")).grid(row=2, column=0, padx=10, pady=10)
        self.batch_combobox = ttk.Combobox(root, textvariable=self.selected_batch, state="readonly")
        self.batch_combobox.grid(row=2, column=1, padx=10, pady=10)

        # Button to generate timetable


        # Create the ttk Button with a custom style
        self.show_button = ttk.Button(root, text="Show Timetable", style="TButton", command=self.show_timetable)
        self.show_button.grid(row=3, column=0, columnspan=2, pady=20)
    def load_batches(self, event):
        """Load batches dynamically based on selected year/semester."""
        year = self.selected_year.get()
        if year in year_mapping:
            batcher, _ = year_mapping[year]
            self.batch_list = batcher()
            self.batch_combobox['values'] = self.batch_list

    def show_timetable(self):
        """Display the timetable in a scrollable grid layout with dynamic column sizing and text wrapping."""
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
            timetable_window.geometry("2560x1400")  # Set initial window size
            ttk.Label(
                timetable_window,
                text=f"Timetable for {year} - {batch}",
                font=("Georgia", 18, "bold")
            ).grid(row=0, column=0, columnspan=len(time_slot) + 1, pady=20)
            # Create a frame with scrollbars
            canvas = tk.Canvas(timetable_window)
            scrollbar_y = tk.Scrollbar(timetable_window, orient="vertical", command=canvas.yview)
            scrollbar_x = tk.Scrollbar(timetable_window, orient="horizontal", command=canvas.xview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

            # Place the scrollbars and canvas in the window
            canvas.grid(row=0, column=0, sticky="nsew")
            scrollbar_y.grid(row=0, column=1, sticky="ns")
            scrollbar_x.grid(row=1, column=0, sticky="ew")

            # Configure the window to expand with content
            timetable_window.grid_rowconfigure(0, weight=1)
            timetable_window.grid_columnconfigure(0, weight=1)

            # Function to calculate text width dynamically
            def get_text_width(text, font):
                """Calculate the required width for a given text based on the font."""
                return Font(font=font).measure(text) // 10  # Divide by 10 for a Tkinter width unit

            # Determine maximum width for each column
            font = ("Arial", 10)


            for col_index, slot in enumerate(["DAY"] + time_slot):
                label = tk.Label(
                    scrollable_frame,
                    text=slot,
                    font=("Arial", 10, "bold"),
                    bg="red",
                    width=20,  # Add padding
                    height=2,
                    anchor='center', justify='center',
                    borderwidth=1,
                    relief="solid"
                )
                label.grid(row=0, column=col_index, sticky="nsew")

            # Data Rows
            for row_index, day in enumerate(date_mapping[:len(timetable_data)]):
                # Day label
                day_label = tk.Label(
                    scrollable_frame,
                    text=day,
                    font=("Arial", 10),
                    bg="orange",
                    anchor='center',justify='center',
                    width=20,  # Adjust width for "DAY" column
                    height=2,
                    borderwidth=1,
                    relief="solid"
                )
                day_label.grid(row=row_index + 1, column=0, sticky="nsew")

                # Time slots
                for col_index, slot in enumerate(timetable_data[row_index]):
                    # Use a Text widget to allow wrapping

                    cell_text = tk.Text(
                        scrollable_frame,
                        font=("Arial", 10),
                        wrap="word",  # Enable word wrapping
                        height=3,  # Adjust the height as needed
                        width=20,  # Adjust width for narrower columns
                        borderwidth=1,
                        relief="solid",
                        bg="lightblue"

                    )
                    cell_text.insert("1.0", slot)  # Insert the text
                    cell_text.tag_configure("center", justify="center")  # Configure center alignment
                    cell_text.tag_add("center", "1.0", "end")  # Apply the center tag to all text
                    cell_text.config(state="disabled")  # Make the Text widget read-only
                    cell_text.grid(row=row_index + 1, column=col_index + 1, sticky="nsew")


        except FileNotFoundError:
            messagebox.showerror("Error", "File not found. Please check the file path.")
        except ValueError:
            messagebox.showerror("Error", "Invalid sheet name. Please check the sheet names in the Excel file.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()
