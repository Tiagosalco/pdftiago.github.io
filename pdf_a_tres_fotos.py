import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import fitz  # PyMuPDF

class PDFToImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF a 3 Fotos")
        self.root.configure(bg="#2C2C2C")

        self.input_label = tk.Label(root, text="Seleccionar archivo PDF:", bg="#2C2C2C", fg="white")
        self.input_label.pack(pady=10)

        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.pack(pady=5)

        self.input_button = tk.Button(root, text="Buscar", command=self.browse_pdf, bg="#1E78FF", fg="white")
        self.input_button.pack(pady=5)

        self.output_label = tk.Label(root, text="Carpeta de salida:", bg="#2C2C2C", fg="white")
        self.output_label.pack(pady=10)

        self.output_entry = tk.Entry(root, width=50)
        self.output_entry.pack(pady=5)

        self.output_button = tk.Button(root, text="Buscar", command=self.browse_output_folder, bg="#1E78FF", fg="white")
        self.output_button.pack(pady=5)

        self.convert_button = tk.Button(root, text="Convertir a imágenes", command=self.convert_to_images, bg="#1E78FF", fg="white")
        self.convert_button.pack(pady=10)

    def browse_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder_path)

    def convert_to_images(self):
        input_pdf = self.input_entry.get()
        output_folder = self.output_entry.get()

        if not input_pdf or not output_folder:
            return

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        pdf_document = fitz.open(input_pdf)

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            pixmap = page.get_pixmap()

            # Convert Pixmap to PIL Image
            img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

            # Get image dimensions
            img_width = img.width
            img_height = img.height // 3  # Divide height into 3 equal parts

            for i in range(3):
                # Crop the image into three equal parts horizontally
                cropped_image = img.crop((0, i * img_height, img_width, (i + 1) * img_height))

                # Save the image
                image_path = os.path.join(output_folder, f"page_{page_number + 1}_part_{i + 1}.png")
                cropped_image.save(image_path)

        pdf_document.close()
        messagebox.showinfo("Conversión Completa", "¡PDF convertido a imágenes con éxito!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToImageConverter(root)
    root.mainloop()
