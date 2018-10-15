from app import create_app
from config import Config
from app import db

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    """
    This is used by the `flask shell` command for easy debugging.
    The variables returned by this function will be available in the
    shell to avoid having to import/create them every time.
    """
    return {
            'db': db,
            }
