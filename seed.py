from faker import Faker
from datetime import datetime

from app.database import SessionLocal
from app.models import User, Role, Post

fake = Faker()

db = SessionLocal()

# Seed Roles

roles = ["Admin", "Manager", "User"]

for role_name in roles:

    existing_role = (
        db.query(Role)
        .filter(Role.role_name == role_name)
        .first()
    )

    if not existing_role:
        db.add(Role(role_name=role_name))

db.commit()

# Seed Users

if db.query(User).count() == 0:

    for _ in range(10):

        user = User(
            name=fake.name(),
            email=fake.unique.email(),
            phone_number=fake.phone_number(),
            created_at=datetime.utcnow()
        )

        db.add(user)

    db.commit()

    print("10 users inserted")

else:
    print("Users already exist. Skipping users seeding.")

# Seed Posts

if db.query(Post).count() == 0:

    users = db.query(User).all()

    for _ in range(20):

        post = Post(
            title=fake.sentence(nb_words=5),
            user_id=fake.random_element(users).id
        )

        db.add(post)

    db.commit()

    print("20 posts inserted")

else:
    print("Posts already exist. Skipping posts seeding.")

db.close()

print("Database seeded successfully!")