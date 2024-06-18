import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.root.configure(bg="#2C2C2C")

        self.image_list = []

        self.frame = tk.Frame(root, padx=10, pady=10, bg="#2C2C2C")
        self.frame.pack()

        self.load_image()

        self.add_button = tk.Button(self.frame, text="Add Images", command=self.add_images, bg="#1E78FF", fg="white")
        self.add_button.pack(pady=10, padx=20)

        self.convert_button = tk.Button(self.frame, text="Convert to PDF", command=self.convert_to_pdf, bg="#1E78FF", fg="white")
        self.convert_button.pack(pady=10, padx=20)

    def load_image(self):
        image = Image.open("static/images_to_pdf.webp")
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(self.frame, image=photo, bg="#2C2C2C")
        self.image_label.image = photo
        self.image_label.pack(pady=10)

    def add_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        if file_paths:
            self.image_list = list(file_paths)

    def convert_to_pdf(self):
        if not self.image_list:
            return

        output_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if output_filename:
            c = canvas.Canvas(output_filename, pagesize=letter)

            for image_path in self.image_list:
                image = Image.open(image_path)
                img_width, img_height = image.size

                c.setPageSize((img_width, img_height))
                c.drawImage(image_path, 0, 0, img_width, img_height)
                c.showPage()

            c.save()
            self.image_list = []
            self.show_conversion_success_message(output_filename)

    def show_conversion_success_message(self, output_filename):
        success_label = tk.Label(self.frame, text=f"Images converted to PDF successfully!\nSaved as {output_filename}", bg="#2C2C2C", fg="white")
        success_label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToPDFConverter(root)
    root.mainloop()
