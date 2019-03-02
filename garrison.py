from app import create_app
from config import Config
from app import db

app = create_app(Config)

if app.config['FAKE_GPIO']:
    print("Faking GPIO interactions. User FAKE_GPIO=False env var to change.")
print("Garrison version: ", app.config['API_VERSION'])
print("Attempting to use db at: ", app.config['SQLALCHEMY_DATABASE_URI'])

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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
