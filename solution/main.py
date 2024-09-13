import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from openrpa.conversion import (
    parse_monitoring_result,
    bpmn_to_xaml_openrpa,
    insert_xaml_into_openrpa_template,
    generate_executable_process,
)


class ScriptGenerationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automatic script generation for RPA")
        self.geometry("500x300")

        # Container for frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # Initialize all three screens
        for F in (InputScreen, GenerationScreen, DownloadScreen):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start on InputScreen
        self.show_frame(InputScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class InputScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        content_frame = tk.Frame(self)
        content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Input File Selection
        self.input_file_path = tk.StringVar()

        label = tk.Label(content_frame, text="Select Input File:")
        label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.input_file_button = tk.Button(
            content_frame, text="Browse", command=self.browse_input_file
        )
        self.input_file_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.input_file_entry = tk.Entry(
            content_frame, textvariable=self.input_file_path, width=40
        )
        self.input_file_entry.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        platform_frame = tk.Frame(self)
        platform_frame.grid(row=1, column=0, padx=20, pady=20, sticky="w")

        # RPA Platform Selection
        label_platform = tk.Label(platform_frame, text="Select RPA Platform:")
        label_platform.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.rpa_platform = tk.StringVar(value="UiPath")
        self.platform_choices = ["UiPath", "OpenRPA"]
        self.platform_dropdown = ttk.Combobox(
            platform_frame,
            textvariable=self.rpa_platform,
            values=self.platform_choices,
            state="readonly",
        )
        self.platform_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.platform_dropdown.current(0)

        # Generate Button
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, padx=20, pady=20)

        self.generate_button = tk.Button(
            button_frame, text="Generate", command=self.start_generation
        )
        self.generate_button.grid(row=0, column=0, padx=10, pady=5)

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(title="Select input file")
        if file_path:
            self.input_file_path.set(file_path)

    def start_generation(self):
        input_file = self.input_file_path.get()
        platform = self.rpa_platform.get()

        if not input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return

        # Save the input file and platform in the controller
        self.controller.input_file = input_file
        self.controller.platform = platform

        # Show the generation screen
        self.controller.show_frame(GenerationScreen)
        self.controller.frames[GenerationScreen].start_progress()


class GenerationScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Generating...")
        label.pack(pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=300, mode="determinate"
        )
        self.progress.pack(pady=20)

    def start_progress(self):
        self.progress["value"] = 0
        self.max_value = 100

        self.update_progress()

    def update_progress(self):
        if self.progress["value"] < self.max_value:
            self.progress["value"] += 10  # Increment progress
            self.after(500, self.update_progress)  # Simulate time delay
        else:
            self.complete_generation()

    def complete_generation(self):
        # Simulate file conversion based on input file and RPA platform
        input_file = self.controller.input_file
        platform = self.controller.platform

        # Automatically generate output file path
        file_directory = os.path.dirname(input_file)
        file_name, file_ext = os.path.splitext(os.path.basename(input_file))
        output_file = os.path.join(
            file_directory, f"executable_process_{platform}{file_ext}"
        )  # CAMBIAR POR OUTPUT FILE DE LA FUNCION

        if platform == "UiPath":
            self.convert_file_uipath(input_file, output_file)
        elif platform == "OpenRPA":
            self.convert_file_openrpa(input_file, output_file)

        # After conversion is complete, move to the download screen
        self.controller.show_frame(DownloadScreen)

    def convert_file_uipath(self, input_file, output_file):
        # Simulated conversion function for UiPath
        # Here you can call a real function for UiPath conversion
        print(f"Converting {input_file} to UiPath format...")
        with open(output_file, "w") as f:
            f.write(f"Converted {input_file} to UiPath executable process")

    def convert_file_openrpa(self, input_file, output_file):
        # Simulated conversion function for OpenRPA
        # Here you can call a real function for OpenRPA conversion
        print(f"Converting {input_file} to OpenRPA format...")
        with open(output_file, "w") as f:
            f.write(f"Converted {input_file} to OpenRPA executable process")


class DownloadScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Conversion Complete!")
        label.pack(pady=10)

        self.download_button = tk.Button(
            self, text="Download Executable Process", command=self.save_file
        )
        self.download_button.pack(pady=20)

    def save_file(self):
        # Let the user choose where to save the converted file
        output_path = filedialog.asksaveasfilename(
            title="Save converted file as", defaultextension=".xaml"
        )
        if output_path:
            try:
                # Move the converted file to the selected location
                os.rename(self.controller.converted_file, output_path)
                messagebox.showinfo("Success", f"File saved at {output_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save the file: {e}")


if __name__ == "__main__":
    app = ScriptGenerationApp()
    app.mainloop()
