Title: Merging Multiple PDF Files in Django using Modular Design

```python
# Install necessary package
# pip install PyPDF2

# Add PyPDF2 to your Django project settings in settings.py if you're using a virtual environment
# INSTALLED_APPS = [
#     ...
#     'PyPDF2',
# ]

# views.py
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from .pdf_utils import merge_pdfs

def merge_pdf_view(request):
    """
    Handle the PDF merging request and return the merged PDF response.
    """
    if request.method == 'POST' and request.FILES.getlist('pdf_files'):
        # Extract PDF files from the POST request
        pdf_files = request.FILES.getlist('pdf_files')
        
        # Merge the PDF files using the utility function
        merged_pdf_path = merge_pdfs(pdf_files, settings.MEDIA_ROOT)
        
        # Read the merged PDF and return as response
        with open(merged_pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="merged_document.pdf"'
            return response

    return render(request, 'merge_pdf.html')

# pdf_utils.py
import os
from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(pdf_files, output_dir):
    """
    Merge multiple PDF files into a single PDF file.

    Parameters:
    pdf_files (list): List of PDF files to be merged.
    output_dir (str): Directory where the merged PDF will be saved.

    Returns:
    str: Path to the merged PDF file.
    """
    pdf_writer = PdfWriter()
    
    # Iterate over the list of PDF files and add their content to the PdfWriter
    for pdf_file in pdf_files:
        pdf_reader = PdfReader(pdf_file)
        
        # Add each page of the current PDF to the writer
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.addPage(pdf_reader.pages[page_num])
    
    # Define output file path
    output_path = os.path.join(output_dir, 'merged_document.pdf')
    
    # Write the PDF content to a file
    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    
    return output_path

# merge_pdf.html
'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Merge PDF Files</title>
</head>
<body>
    <h1>Merge PDF Files</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <label for="pdf_files">Select PDF files to merge:</label>
        <input type="file" id="pdf_files" name="pdf_files" multiple required>
        <button type="submit">Merge PDFs</button>
    </form>
</body>
</html>
'''

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('merge-pdfs/', views.merge_pdf_view, name='merge_pdf_view'),
]
```

In this code, we implement a Django-based application that allows users to upload multiple PDF files and merge them into a single PDF document using the `PyPDF2` library. The solution emphasizes modular design by separating responsibilities across different components: the PDF merging logic resides in a utility module (`pdf_utils.py`), the request handling is in the view (`views.py`), and user interaction is defined in a simple HTML template (`merge_pdf.html`). This allows for clean and maintainable code.