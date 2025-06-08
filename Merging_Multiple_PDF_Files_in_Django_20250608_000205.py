Title: Merging Multiple PDF Files in Django

```python
# Import necessary Django libraries
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import io

# Importing PyPDF2 to handle PDF files
from PyPDF2 import PdfMerger

# Import settings to access file storage
from django.conf import settings
import os

# Form to upload PDF files
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

# Type hinting imports
from typing import List

# Define a form for uploading PDF files
class PDFUploadForm(forms.Form):
    pdf_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


# View to handle PDF merge requests
class PDFMergerView(View):
    # Handles GET request
    def get(self, request) -> HttpResponse:
        form = PDFUploadForm()
        return render(request, 'merge_pdfs.html', {'form': form})

    # Handles POST request
    def post(self, request) -> HttpResponse:
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract uploaded files
            files: List[InMemoryUploadedFile] = request.FILES.getlist('pdf_files')
            response = self.merge_pdfs(files)
            return response
        return render(request, 'merge_pdfs.html', {'form': form})

    # Merges the given PDF files into a single PDF
    def merge_pdfs(self, files: List[InMemoryUploadedFile]) -> HttpResponse:
        # Initialize a PdfMerger object
        pdf_merger = PdfMerger()
        
        # Append each file to the merger
        for pdf_file in files:
            # Convert each file to a binary stream (io.BytesIO)
            pdf_stream = io.BytesIO(pdf_file.read())
            pdf_merger.append(pdf_stream)
        
        # Create a binary stream to hold the merged PDF
        merged_pdf_stream = io.BytesIO()
        pdf_merger.write(merged_pdf_stream)
        pdf_merger.close()

        # Set the stream position to the beginning
        merged_pdf_stream.seek(0)

        # Create a response object with the merged PDF
        response = HttpResponse(merged_pdf_stream, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="merged_document.pdf"'
        return response

# Template for uploading PDF files
# Create a merge_pdfs.html file in the templates directory
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Merge PDF Files</title>
</head>
<body>
    <h1>Upload PDF Files to Merge</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form }}
        <button type="submit">Merge PDFs</button>
    </form>
</body>
</html>
"""

# In your Django project `urls.py`, include the view
# from django.urls import path
# from .views import PDFMergerView

# urlpatterns = [
#     path('merge-pdfs/', PDFMergerView.as_view(), name='merge_pdfs'),
# ]
```

This Django practice app uses class-based views and a form to allow users to upload multiple PDF files, which are then merged into a single PDF and returned as a downloadable file. The code includes type annotations for clarity and utilizes the PyPDF2 library to perform the PDF merging operation.