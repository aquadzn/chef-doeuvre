from datetime import datetime

import config
from main_gcp import User, db

from werkzeug.security import generate_password_hash


def main():

    db.drop_all()
    db.create_all()

    admin_user = User(
        username=config.ADMIN_USERNAME.lower(),
        email=config.ADMIN_MAIL.lower(),
        password=generate_password_hash(config.ADMIN_PWD, method="sha256"),
        created_at=datetime.now(),
    )
    db.session.add(admin_user)
    db.session.commit()


if __name__ == "__main__":
    main()
