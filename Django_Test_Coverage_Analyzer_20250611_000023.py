Title: Django Test Coverage Analyzer

```python
# Import necessary Django libraries for settings, and building models, views, and the Django ORM
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
import os

# Import coverage to analyze test coverage
import coverage

# Project-level Settings in settings.py
# Add 'coverage_analyzer' to INSTALLED_APPS in your Django project settings.

# Application-level Model in models.py
class TestResult(models.Model):
    # Model to store information about test coverage results
    module_name = models.CharField(max_length=255)
    statements = models.IntegerField()
    missed = models.IntegerField()
    coverage_percentage = models.FloatField()

    def __str__(self):
        return f"{self.module_name}: {self.coverage_percentage}%"

# Views in views.py
def calculate_coverage(request):
    # Initialize and run coverage analysis
    cov = coverage.Coverage()
    cov.start()

    # Simulate your test running process (Here you should put your test running logic)
    os.system('python manage.py test')

    # Stop coverage analysis after running tests
    cov.stop()
    cov.save()

    # Create coverage summary report
    report_data = []
    for module in cov.get_data().measured_files():
        analysis = cov.analysis(module)
        result = TestResult(
            module_name=analysis[0],
            statements=analysis[1],
            missed=analysis[2],
            coverage_percentage=(analysis[1] - analysis[2]) / analysis[1] * 100
        )
        result.save()
        report_data.append(result)

    # Pass results to template for display
    return render(request, 'coverage_report.html', {'results': report_data})

def coverage_report_view(request):
    # Fetch all test coverage results from the database
    results = TestResult.objects.all()
    return render(request, 'coverage_report.html', {'results': results})

# URL Configuration in urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('calculate_coverage/', views.calculate_coverage, name='calculate_coverage'),
    path('coverage_report/', views.coverage_report_view, name='coverage_report'),
]

# HTML Template for displaying results in coverage_report.html
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Coverage Report</title>
</head>
<body>
    <h1>Test Coverage Report</h1>
    <table border="1">
        <tr>
            <th>Module Name</th>
            <th>Statements</th>
            <th>Missed</th>
            <th>Coverage Percentage</th>
        </tr>
        {% for result in results %}
        <tr>
            <td>{{ result.module_name }}</td>
            <td>{{ result.statements }}</td>
            <td>{{ result.missed }}</td>
            <td>{{ result.coverage_percentage }}%</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Before running the project, ensure the following:
# 1. 'coverage' Python package is installed (use `pip install coverage`).
# 2. Django project is correctly set up and working.
# 3. The views and URLs are correctly mapped to run these functionalities.
```