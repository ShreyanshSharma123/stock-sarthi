import sys
sys.path.append('.')
from database.models import SessionLocal, User

db = SessionLocal()

# Check the email from screenshot
email = 'shreyansh.sharma.24cse@bmu.edu.in'
user = db.query(User).filter(User.email == email).first()

if user:
    print(f"✅ User EXISTS: {email}")
    print(f"   ID: {user.id}")
    print(f"   Username: {user.username}")
    print(f"   Password hash exists: {bool(user.hashed_password)}")
else:
    print(f"❌ User NOT FOUND: {email}")
    print("\nAll users in database:")
    all_users = db.query(User).all()
    for u in all_users:
        print(f"  - {u.email}")
