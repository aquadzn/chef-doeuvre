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

    usernames = [
        "jean",
        "william",
        "sylvere",
    ]

    for i in range(len(usernames)):
        test_user = User(
            username=usernames[i].lower(),
            email=f"{usernames[i]}@mail.com".lower(),
            password=generate_password_hash("azerty", method="sha256"),
            created_at=datetime.now(),
        )
        print(f"Utilisateur '{usernames[i]}' crée.")
        print("Mot de passe: azerty")
        db.session.add(test_user)

    db.session.commit()


if __name__ == "__main__":
    main()
