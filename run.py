from web_app import create_app
from shared.db import db
from shared.migration import run_migration
from shared.seed import Seed

app = create_app()

def init_app():
    with app.app_context():
        run_migration(app)
        seed = Seed(db.session)
        seed.start()

if __name__ == '__main__':
    init_app()
    app.run(use_reloader=False)
