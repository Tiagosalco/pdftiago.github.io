import tkinter as tk
from tkinter import filedialog
import PyPDF2
import os
from PIL import Image, ImageTk

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.configure(bg="#2C2C2C") 

        self.file_list = []

        self.frame = tk.Frame(root, padx=10, pady=10, bg="#2C2C2C")  
        self.frame.pack()

        self.load_image()

        self.add_button = tk.Button(self.frame, text="Add PDFs", command=self.add_pdfs, bg="#1E78FF", fg="white")
        self.add_button.pack(pady=10, padx=20) 

        self.merge_button = tk.Button(self.frame, text="Merge PDFs", command=self.merge_pdfs, bg="#1E78FF", fg="white")
        self.merge_button.pack(pady=10, padx=20) 

    def load_image(self):
        image = Image.open("static/merge.webp")
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(self.frame, image=photo, bg="#2C2C2C")
        self.image_label.image = photo
        self.image_label.pack(pady=10)

    def add_pdfs(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if file_paths:
            self.file_list = list(file_paths)

    def merge_pdfs(self):
        if not self.file_list:
            return

        pdf_final = PyPDF2.PdfMerger()

        for file_path in self.file_list:
            pdf_final.append(file_path)

        output_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if output_filename:
            pdf_final.write(output_filename)
            pdf_final.close()
            self.file_list = []
            self.show_merge_success_message(output_filename)

    def show_merge_success_message(self, output_filename):
        success_label = tk.Label(self.frame, text=f"PDFs merged successfully!\nSaved as {os.path.basename(output_filename)}", bg="#2C2C2C", fg="white")  # Set background color
        success_label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
