from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge')
def merge():
    os.system('python pdfmerger.py')
    return redirect(url_for('index'))

@app.route('/crop')
def crop():
    os.system('python recortarpdf.py')
    return redirect(url_for('index'))

@app.route('/convert-to-images')
def convert_to_images():
    os.system('python PdfA3Fotos.py')
    return redirect(url_for('index'))

@app.route('/convert-to-pdf')
def convert_to_pdf():
    os.system('python imagestopdf.py')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
