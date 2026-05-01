#!/usr/bin/env python3
"""
Script to reset admin password
"""

import os
import sys
from flask import Flask
from models import db, User
from werkzeug.security import generate_password_hash

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def reset_admin_password():
    """Reset admin password to a known value"""
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///umukozi.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        try:
            # Find admin user
            admin_user = User.query.filter_by(user_type='admin').first()
            
            if admin_user:
                # Set new password
                new_password = "admin123"
                hashed_password = generate_password_hash(new_password)
                admin_user.password = hashed_password
                db.session.commit()
                
                print(f'✅ Admin password reset successfully!')
                print(f'   Email: {admin_user.email}')
                print(f'   Name: {admin_user.full_name}')
                print(f'   New Password: {new_password}')
                print(f'\n🔐 You can now log in with these credentials.')
                return True
            else:
                print('❌ No admin user found in database')
                return False
                
        except Exception as e:
            print(f'❌ Error resetting admin password: {e}')
            db.session.rollback()
            return False

if __name__ == '__main__':
    print('🔧 Resetting admin password...')
    success = reset_admin_password()
    if success:
        print('🎉 Admin password reset completed!')
    else:
        print('💥 Failed to reset admin password.')
        sys.exit(1)
