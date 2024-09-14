import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from uipath.conversion import convert_bpmn_to_uipath_xaml
from openrpa.conversion import convert_bpmn_to_openrpa_xaml


class ScriptGenerationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automatic script generation for RPA")
        self.geometry("500x300")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (InputScreen, GenerationScreen, DownloadScreen):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

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

        self.controller.input_file = input_file
        self.controller.platform = platform

        self.controller.show_frame(GenerationScreen)
        self.controller.frames[GenerationScreen].start_progress()


class GenerationScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Generating...")
        label.pack(pady=10)

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
            self.progress["value"] += 20
            self.after(200, self.update_progress)
        else:
            self.complete_generation()

    def complete_generation(self):
        self.controller.show_frame(DownloadScreen)


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

        self.back_button = tk.Button(
            self, text="Back to Start", command=self.go_back_to_start
        )
        self.back_button.pack(pady=10)

    def save_file(self):
        output_path = filedialog.asksaveasfilename(
            title="Save converted file as", defaultextension=".xaml"
        )
        if output_path:
            try:
                input_file = self.controller.input_file
                platform = self.controller.platform

                if platform == "UiPath":
                    self.convert_file_uipath(input_file, output_path)
                elif platform == "OpenRPA":
                    self.convert_file_openrpa(input_file, output_path)

                messagebox.showinfo("Success", f"File saved at {output_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save the file: {e}")

    def go_back_to_start(self):
        self.controller.input_file = None
        self.controller.platform = None
        self.controller.frames[InputScreen].input_file_path.set("")
        self.controller.show_frame(InputScreen)

    def convert_file_uipath(self, input_file, output_file):
        print(f"Converting {input_file} to UiPath format...")
        convert_bpmn_to_uipath_xaml(input_file, output_file)

    def convert_file_openrpa(self, input_file, output_file):
        print(f"Converting {input_file} to OpenRPA format...")
        convert_bpmn_to_openrpa_xaml(input_file, output_file)


if __name__ == "__main__":
    app = ScriptGenerationApp()
    app.mainloop()
