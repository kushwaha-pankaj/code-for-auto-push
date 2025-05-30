Title: Coffee Maker

```python
class CoffeeMaker:
    def __init__(self):
        self.water_level = 100  # percentage
        self.coffee_grounds = 100  # percentage
    
    def check_resources(self, water_needed, coffee_needed):
        if self.water_level < water_needed:
            return False, "Not enough water!"
        if self.coffee_grounds < coffee_needed:
            return False, "Not enough coffee grounds!"
        return True, "Resources are sufficient."
    
    def make_coffee(self, water_needed=20, coffee_needed=10):
        can_make, message = self.check_resources(water_needed, coffee_needed)
        
        if can_make:
            self.water_level -= water_needed
            self.coffee_grounds -= coffee_needed
            return "Coffee is ready!"
        else:
            return message

# Example usage
coffee_maker = CoffeeMaker()
print(coffee_maker.make_coffee())
```