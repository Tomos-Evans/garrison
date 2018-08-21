from app import create_app, db
from config import Config, DevelopmentConfig
from app.models import Drink, DrinkComponent, Ingredient

app = create_app(DevelopmentConfig)

@app.shell_context_processor
def make_shell_context():
    """
    This is used by the `flask shell` command for easy debugging.
    The variables returned by this function will be available in the
    shell to avoid having to import/create them every time.
    """
    return {
            'db': db,
            'Drink': Drink,
            'DrinkComponent': DrinkComponent,
            'Ingredient': Ingredient,
            }
