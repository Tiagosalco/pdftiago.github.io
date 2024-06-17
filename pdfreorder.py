import sys
import PyPDF2
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import os

class PDFPageReorderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Page Reorder")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.pdf_file_path = None
        self.page_order = []

        self.file_list_widget = QListWidget()
        self.file_list_widget.setDragDropMode(QListWidget.InternalMove)
        self.layout.addWidget(self.file_list_widget)

        self.open_button = QPushButton("Open PDF")
        self.open_button.clicked.connect(self.open_pdf)
        self.layout.addWidget(self.open_button)

        self.preview_label = QLabel()
        self.layout.addWidget(self.preview_label)

        self.reorder_button = QPushButton("Reorder Pages")
        self.reorder_button.clicked.connect(self.reorder_pages)
        self.layout.addWidget(self.reorder_button)

    def open_pdf(self):
        file_dialog = QFileDialog()
        self.pdf_file_path, _ = file_dialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")

        if self.pdf_file_path:
            self.load_pdf_pages()

    def load_pdf_pages(self):
        self.file_list_widget.clear()
        self.page_order = []

        pdf_document = PyPDF2.PdfFileReader(self.pdf_file_path)

        for page_num in range(pdf_document.getNumPages()):
            item = QListWidgetItem(f"Page {page_num + 1}")
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled)
            self.file_list_widget.addItem(item)
            self.page_order.append(page_num)

    def reorder_pages(self):
        if not self.pdf_file_path or not self.page_order:
            return

        pdf_document = PyPDF2.PdfFileReader(self.pdf_file_path)
        pdf_writer = PyPDF2.PdfFileWriter()

        for page_num in self.page_order:
            pdf_writer.addPage(pdf_document.getPage(page_num))

        with open("temp_reorder.pdf", "wb") as output_file:
            pdf_writer.write(output_file)

        # Rename the temporary file to the desired output filename
        output_filename = f"ReOrdered_{os.path.basename(self.pdf_file_path)}"
        os.rename("temp_reorder.pdf", output_filename)

        self.load_pdf_pages()

    def display_preview(self, page_num):
        if not self.pdf_file_path:
            return

        pdf_document = PyPDF2.PdfFileReader(self.pdf_file_path)
        page = pdf_document.getPage(page_num)
        xObject = page['/Resources']['/XObject'].get_object()
        img = xObject.get_object()
        pixmap = QPixmap.fromImage(QImage(img.data, img.width, img.height, img.stride, QImage.Format_RGB888))
        self.preview_label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFPageReorderApp()
    window.show()
    sys.exit(app.exec_())
