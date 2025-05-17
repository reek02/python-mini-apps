import qrcode
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image
from typing import Optional, Tuple

class QRCodeGeneratorApp:
    def __init__(self):
        self.logo_path: Optional[str] = None
        self.preview_label: Optional[ctk.CTkLabel] = None
        self.initialize_app()
        self.create_widgets()
        self.setup_layout()

    def initialize_app(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.window = ctk.CTk()
        self.window.title("Advanced QR Code Generator")
        self.window.geometry("1000x700")
        self.window.minsize(900, 650)

        # Configuration variables
        self.error_correction_map = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H
        }
        self.default_values = {
            "filename": "qr_code.png",
            "box_size": 10,
            "border": 4,
            "error_correction": "H",
            "fg_color": "#000000",
            "bg_color": "#FFFFFF"
        }

    def create_widgets(self):
        # Main frames
        self.input_frame = ctk.CTkFrame(self.window)
        self.settings_frame = ctk.CTkFrame(self.window)
        self.preview_frame = ctk.CTkFrame(self.window)
        self.control_frame = ctk.CTkFrame(self.window)

        # Input section
        self.create_input_section()
        
        # Settings section
        self.create_settings_section()
        
        # Preview section
        self.create_preview_section()
        
        # Control buttons
        self.create_control_buttons()

    def setup_layout(self):
        # Grid configuration
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)

        # Frame placement
        self.input_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.settings_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.preview_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=10, sticky="nsew")
        self.control_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        # Footer
        self.create_footer()

    def create_input_section(self):
        ctk.CTkLabel(self.input_frame, text="QR Code Generator Pro", 
                    font=("Arial", 22, "bold")).pack(pady=(10, 20))

        # Text input
        ctk.CTkLabel(self.input_frame, text="Enter Text/URL:").pack(pady=5)
        self.entry_text = ctk.CTkEntry(self.input_frame, width=400)
        self.entry_text.pack(pady=5)

        # Filename input
        ctk.CTkLabel(self.input_frame, text="File Name:").pack(pady=(15, 5))
        self.filename_entry = ctk.CTkEntry(self.input_frame, width=400)
        self.filename_entry.insert(0, self.default_values["filename"])
        self.filename_entry.pack(pady=5)

    def create_settings_section(self):
        # Color settings
        self.fg_color = ctk.StringVar(value=self.default_values["fg_color"])
        self.bg_color = ctk.StringVar(value=self.default_values["bg_color"])
        self.create_color_settings()

        # Logo settings
        self.create_logo_settings()

        # QR parameters
        self.create_qr_parameters()

    def create_color_settings(self):
        color_frame = ctk.CTkFrame(self.settings_frame)
        color_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(color_frame, text="Color Settings", font=("Arial", 14)).grid(row=0, columnspan=2, pady=5)
        ctk.CTkButton(color_frame, text="Foreground", command=self.choose_fg_color).grid(row=1, column=0, padx=5)
        ctk.CTkButton(color_frame, text="Background", command=self.choose_bg_color).grid(row=1, column=1, padx=5)

    def create_logo_settings(self):
        logo_frame = ctk.CTkFrame(self.settings_frame)
        logo_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(logo_frame, text="Logo Settings", font=("Arial", 14)).grid(row=0, columnspan=2, pady=5)
        ctk.CTkButton(logo_frame, text="Upload Logo", command=self.upload_logo).grid(row=1, column=0, padx=5)
        ctk.CTkButton(logo_frame, text="Clear Logo", command=self.clear_logo).grid(row=1, column=1, padx=5)
        self.logo_label = ctk.CTkLabel(logo_frame, text="No logo selected")
        self.logo_label.grid(row=2, columnspan=2, pady=5)

    def create_qr_parameters(self):
        params_frame = ctk.CTkFrame(self.settings_frame)
        params_frame.pack(fill="both", expand=True, pady=10)  # Modified line
        
        # Error correction
        self.error_correction_var = ctk.StringVar(value=self.default_values["error_correction"])
        ctk.CTkLabel(params_frame, text="Error Correction:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ec_combo = ctk.CTkComboBox(params_frame, variable=self.error_correction_var, 
                                values=["L", "M", "Q", "H"])
        ec_combo.grid(row=0, column=1, padx=10, pady=5)

        # Add vertical spacing
        params_frame.rowconfigure((0,1,2), weight=1)
        params_frame.columnconfigure((0,1), weight=1)

        # Box size
        ctk.CTkLabel(params_frame, text="Box Size:").grid(row=1, column=0, sticky="w", padx=10)
        self.box_size_entry = ctk.CTkEntry(params_frame)
        self.box_size_entry.insert(0, str(self.default_values["box_size"]))
        self.box_size_entry.grid(row=1, column=1, padx=5)

        # Border size
        ctk.CTkLabel(params_frame, text="Border Size:").grid(row=2, column=0, sticky="w", padx=10)
        self.border_entry = ctk.CTkEntry(params_frame)
        self.border_entry.insert(0, str(self.default_values["border"]))
        self.border_entry.grid(row=2, column=1, padx=5)

    def create_preview_section(self):
        ctk.CTkLabel(self.preview_frame, text="Live Preview", 
                    font=("Arial", 16)).pack(pady=10)
        self.preview_label = ctk.CTkLabel(self.preview_frame, text="Your QR code will appear here")
        self.preview_label.pack(expand=True, fill="both")

    def create_control_buttons(self):
        ctk.CTkButton(self.control_frame, text="Generate QR Code", 
                      command=self.generate_qr).pack(side="left", padx=10)
        ctk.CTkButton(self.control_frame, text="Toggle Theme", 
                      command=self.toggle_theme).pack(side="left", padx=10)
        ctk.CTkButton(self.control_frame, text="Exit", 
                      command=self.window.quit).pack(side="right", padx=10)

    def create_footer(self):
        footer = ctk.CTkLabel(self.window, 
                             text="Created with ❤️ by Reekparna Sen - QR Code Generator",
                             text_color="#666666")
        footer.grid(row=3, column=0, columnspan=2, pady=(5, 10))

    def generate_qr(self):
        # Validate inputs
        if not self.validate_inputs():
            return

        # Create QR code
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=self.error_correction_map[self.error_correction_var.get()],
                box_size=int(self.box_size_entry.get()),
                border=int(self.border_entry.get())
            )
            qr.add_data(self.entry_text.get())
            qr.make(fit=True)
            
            img = qr.make_image(
                fill_color=self.fg_color.get(),
                back_color=self.bg_color.get()
            ).convert('RGB')

            # Add logo if available
            if self.logo_path:
                self.add_logo_to_qr(img)

            # Save and update preview
            self.save_and_display_qr(img)

        except Exception as e:
            messagebox.showerror("Generation Error", f"Failed to generate QR code: {str(e)}")

    def validate_inputs(self) -> bool:
        if not self.entry_text.get().strip():
            messagebox.showwarning("Input Error", "Please enter text/URL")
            return False

        try:
            box_size = int(self.box_size_entry.get())
            border = int(self.border_entry.get())
            if box_size <= 0 or border < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Box size and border must be positive integers")
            return False

        return True

    def add_logo_to_qr(self, img: Image.Image):
        try:
            logo = Image.open(self.logo_path)
            qr_size = img.size[0]
            logo_size = int(qr_size * 0.2)
            
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            if logo.mode != 'RGBA':
                logo = logo.convert('RGBA')
            
            mask = logo.split()[3]
            position = ((qr_size - logo_size) // 2, (qr_size - logo_size) // 2)
            img.paste(logo, position, mask)
        except Exception as e:
            messagebox.showerror("Logo Error", f"Failed to add logo: {str(e)}")
            raise

    def save_and_display_qr(self, img: Image.Image):
        folder_path = filedialog.askdirectory(title="Select Save Folder")
        if not folder_path:
            return

        file_path = os.path.join(folder_path, self.filename_entry.get())
        img.save(file_path)
        self.update_preview(img)
        messagebox.showinfo("Success", f"QR Code saved at:\n{file_path}")

    def update_preview(self, img_pil: Image.Image):
        try:
            img_preview = img_pil.copy()
            img_preview.thumbnail((300, 300))
            
            ctk_image = ctk.CTkImage(
                light_image=img_preview,
                dark_image=img_preview,
                size=img_preview.size
            )
            
            self.preview_label.configure(image=ctk_image, text="")
            self.preview_label.image = ctk_image
        except Exception as e:
            messagebox.showerror("Preview Error", f"Cannot generate preview: {str(e)}")

    def choose_fg_color(self):
        if color := colorchooser.askcolor(title="Choose Foreground Color")[1]:
            self.fg_color.set(color)

    def choose_bg_color(self):
        if color := colorchooser.askcolor(title="Choose Background Color")[1]:
            self.bg_color.set(color)

    def upload_logo(self):
        if path := filedialog.askopenfilename(
            title="Select Logo",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")]
        ):
            self.logo_path = path
            self.logo_label.configure(text=os.path.basename(path))

    def clear_logo(self):
        self.logo_path = None
        self.logo_label.configure(text="No logo selected")

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = QRCodeGeneratorApp()
    app.run()