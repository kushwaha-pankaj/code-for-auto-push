Title: Django Application to Merge Multiple PDF Files with Input Validation

```python
# Import necessary Django and Python libraries
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from PyPDF2 import PdfReader, PdfWriter
import os

# Create a form class to handle PDF uploads
class PDFMergeForm(forms.Form):
    pdf_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        label='Select PDF files to merge',
        validators=[],
    )

    # Validate that all files are indeed PDFs
    def clean_pdf_files(self):
        files = self.files.getlist('pdf_files')
        if len(files) < 2:
            raise ValidationError('Please upload at least two PDF files.')
        for file in files:
            if not file.name.endswith('.pdf'):
                raise ValidationError('File must be a PDF.')
        return files

# View function to handle the PDF merge process
def merge_pdfs(request):
    if request.method == 'POST':
        form = PDFMergeForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_files = request.FILES.getlist('pdf_files')
            # Create a PdfWriter object to amalgamate PDFs
            pdf_writer = PdfWriter()

            # Loop through each uploaded PDF and merge them together
            for pdf in pdf_files:
                pdf_reader = PdfReader(pdf)
                for page in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page])

            # Create the HttpResponse content type for PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="merged_document.pdf"'

            # Write the merged PDF into the response
            pdf_writer.write(response)
            return response
    else:
        form = PDFMergeForm()
    
    # Render the template with the form
    return render(request, 'merge_pdfs.html', {'form': form})

# Create a basic HTML template (merge_pdfs.html) in your templates directory
"""
<!DOCTYPE html>
<html>
<head>
    <title>PDF Merger</title>
</head>
<body>
    <h1>Merge PDF Files</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Merge PDFs</button>
    </form>
</body>
</html>
"""

# URL configuration to route views to the function
from django.urls import path

urlpatterns = [
    path('merge/', merge_pdfs, name='merge_pdfs'),
]

# Remember to add the PyPDF2 library to your project's requirements.txt file
# PyPDF2==3.0.0
```

This Django application provides a form for users to upload multiple PDF files. Upon submission, the application validates the input and merges the PDF files using the PyPDF2 library. The result is served as a downloadable merged PDF document.