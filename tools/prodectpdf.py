import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pikepdf
import os

class PDFTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Encryption Tool")
        self.geometry("500x350")
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = ttk.Label(self, text="PDF Encryption Tool", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=20)

        # File Selection Frame
        self.file_frame = ttk.LabelFrame(self, text="Select PDF File")
        self.file_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.file_path_label = ttk.Label(self.file_frame, text="PDF File Path:")
        self.file_path_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.file_entry = ttk.Entry(self.file_frame, width=40)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.browse_button = ttk.Button(self.file_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        # Password Entry
        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()

        # Destination Folder Frame
        self.dest_frame = ttk.LabelFrame(self, text="Select Destination Folder")
        self.dest_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.dest_path_label = ttk.Label(self.dest_frame, text="Destination Folder:")
        self.dest_path_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.dest_entry = ttk.Entry(self.dest_frame, width=40)
        self.dest_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.dest_browse_button = ttk.Button(self.dest_frame, text="Browse", command=self.browse_dest_folder)
        self.dest_browse_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        # Encrypt Button
        self.encrypt_button = ttk.Button(self, text="Encrypt PDF", command=self.encrypt_pdf)
        self.encrypt_button.pack(pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def browse_dest_folder(self):
        dest_folder = filedialog.askdirectory()
        if dest_folder:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, dest_folder)

    def encrypt_pdf(self):
        file_path = self.file_entry.get()
        password = self.password_entry.get()
        dest_folder = self.dest_entry.get()

        if not file_path:
            messagebox.showerror("Error", "Please select a PDF file.")
            return
        if not password:
            messagebox.showerror("Error", "Please enter a password for encryption.")
            return
        if not dest_folder:
            messagebox.showerror("Error", "Please select a destination folder.")
            return

        try:
            # Ensure the destination folder exists
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            # Generate the path for the encrypted PDF file
            encrypted_file_path = os.path.join(dest_folder, "encrypted_pdf.pdf")

            # Encrypt and save the PDF file
            with pikepdf.open(file_path) as pdf:
                no_extract = pikepdf.Permissions(extract=False)
                pdf.save(encrypted_file_path, encryption=pikepdf.Encryption(user=password, owner=None, allow=no_extract))

            messagebox.showinfo("Success", f"PDF encrypted and saved to:\n{encrypted_file_path}")
        except pikepdf.PdfError as e:
            messagebox.showerror("Error", f"Failed to encrypt PDF:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")

if __name__ == "__main__":
    app = PDFTool()
    app.mainloop()
