import sys
sys.path.append('.')
from database.models import SessionLocal, User
from api.routes.users import get_password_hash

db = SessionLocal()

# Create new user
email = 'shreyansh.sharma.24cse@bmu.edu.in'
password = '12345'
username = 'shreyansh'

# Check if already exists
existing = db.query(User).filter(User.email == email).first()
if existing:
    print(f"❌ User already exists: {email}")
else:
    # Create user
    new_user = User(
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
        full_name='Shreyansh Sharma'
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"✅ Account created successfully!")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"\nYou can now login with these credentials.")
