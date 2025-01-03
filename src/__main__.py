from src.app import get_app
from src.pkg.settings import Settings


if __name__ == "__main__":
    get_app().run(port=Settings.APP_PORT, debug=Settings.APP_DEBUG)
