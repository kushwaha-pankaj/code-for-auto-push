Title: Django Dice Rolling Game with Logging

```python
# Import necessary libraries and modules
import random
import logging
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.conf import settings

# Configure logging settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the DiceRollingGame view
class DiceRollingGame(View):
    """
    A Django view to simulate a dice rolling game.
    Rolling a six-sided dice and returning the result.
    """

    def get(self, request, *args, **kwargs):
        """Handle GET requests to roll the dice."""
        dice_roll = random.randint(1, 6)  # Simulate rolling a six-sided dice
        logger.info(f"Dice rolled: {dice_roll}")  # Log the result of the dice roll

        # Return the result as JSON response
        return JsonResponse({"dice_roll": dice_roll})


# Define the URL configuration for the app
urlpatterns = [
    path('roll/', DiceRollingGame.as_view(), name='roll_dice'),
]

# Define Django settings required to run the standalone app
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,  # Use this module as the URL configuration module
    SECRET_KEY='a_random_secret_key',
    ALLOWED_HOSTS=['*'],  # Allow all hosts for simplicity
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
    ],
)

# Run the Django development server if this script is executed directly
if __name__ == "__main__":
    import sys
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
```

To use this code:

1. Ensure you have Django installed in your environment (`pip install django`).
2. Save the code to a file, `dice_game.py`.
3. Run the script by executing `python dice_game.py runserver`.
4. Open your web browser and go to `http://127.0.0.1:8000/roll/` to simulate a dice roll.

This simple Django application simulates rolling a six-sided dice each time the `/roll/` URL is accessed, and it logs each roll's result using Python's `logging` module.