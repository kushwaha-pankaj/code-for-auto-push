Title: Merging Multiple PDF Files in Django

```python
# models.py

from django.db import models

class PDFFile(models.Model):
    """Model to upload and store PDF files."""
    file = models.FileField(upload_to='pdfs/')

# forms.py

from django import forms

class PDFMergeForm(forms.Form):
    """Form to handle PDF file uploads."""
    pdf_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)

# views.py

from typing import List
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from PyPDF2 import PdfReader, PdfWriter
from .forms import PDFMergeForm
from .models import PDFFile

class PDFMergeView(View):
    """View to handle merging of PDF files."""
    
    def get(self, request) -> HttpResponse:
        """Render a form to upload multiple PDF files."""
        form = PDFMergeForm()
        return render(request, 'merge_pdfs.html', {'form': form})
    
    def post(self, request) -> HttpResponse:
        """Merge uploaded PDF files and return a merged PDF."""
        form = PDFMergeForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_writer = PdfWriter()
            pdf_files: List = request.FILES.getlist('pdf_files')

            # Iterate over each uploaded PDF file
            for pdf_file in pdf_files:
                pdf_reader = PdfReader(pdf_file)
                
                # Add pages from each PDF to the writer
                for page in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page])

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="merged.pdf"'
            
            # Write merged PDF to response
            pdf_writer.write(response)
            
            return response
        return render(request, 'merge_pdfs.html', {'form': form})

# urls.py

from django.urls import path
from .views import PDFMergeView

urlpatterns = [
    path('merge_pdfs/', PDFMergeView.as_view(), name='merge_pdfs'),
]

# merge_pdfs.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Merge PDF Files</title>
</head>
<body>
    <h1>Merge PDF Files</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Merge</button>
    </form>
</body>
</html>
```

This Django practice illustrates a simple setup for merging multiple PDF files. It uses Django forms and views to create a web page that allows users to upload multiple PDFs and then merges them into a single file using the `PyPDF2` library. The implementation uses type-annotated code for better clarity and maintainability.