```python
# Title: Python Django Test Coverage Analyzer

import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Analyze test coverage for a Django application.'

    def handle(self, *args, **options):
        """
        Entry point for the command.
        Executes the test coverage analysis.
        """
        self.stdout.write(self.style.SUCCESS('Starting test coverage analysis...'))
        
        # Step 1: Run tests with coverage
        self.run_tests_with_coverage()
        
        # Step 2: Generate coverage report
        self.generate_coverage_report()
        
        # Step 3: Display summary
        self.display_coverage_summary()

    def run_tests_with_coverage(self):
        """
        Runs tests and collects coverage data.
        """
        self.stdout.write('Running tests with coverage...')
        os.system('coverage run --source="." manage.py test')

    def generate_coverage_report(self):
        """
        Generates a detailed HTML report of the coverage data.
        """
        self.stdout.write('Generating HTML report...')
        os.system('coverage html')

    def display_coverage_summary(self):
        """
        Displays the coverage report summary.
        """
        self.stdout.write('Test Coverage Summary:')
        
        # Using subprocess.run for better performance and output capture
        result = subprocess.run(['coverage', 'report'], text=True, capture_output=True)
        
        if result.returncode == 0:
            self.stdout.write(self.style.SUCCESS(result.stdout))
        else:
            self.stderr.write(self.style.ERROR('Error in generating coverage summary.'))
            self.stderr.write(self.style.ERROR(result.stderr))

# Usage:
# Add this command in one of the Django app's management/commands directory.
# Execute the command through: python manage.py [command_name]

```

Note:
- This practice Django management command focuses on generating test coverage analysis reports.
- It uses `os.system` for simplicity in running shell commands but improves performance in capturing and displaying output using `subprocess.run`.
- The command can be parts of an app's `management/commands` folder within a Django project for integration.
- It assumes `coverage.py` is already installed and available in the environment.