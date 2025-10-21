from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'selenium_testing_demo_professional_2025'

# Enhanced user database with roles and metadata
users_db = {
    'admin': {
        'password': 'password123',
        'role': 'Administrator',
        'name': 'System Admin',
        'email': 'admin@testingdemo.com',
        'last_login': None
    },
    'student': {
        'password': 'student123',
        'role': 'Student',
        'name': 'Test Student',
        'email': 'student@university.edu',
        'last_login': None
    },
    'test_user': {
        'password': 'test123',
        'role': 'Test User',
        'name': 'Demo User',
        'email': 'demo@testing.com',
        'last_login': None
    },
    'qa_tester': {
        'password': 'qa123',
        'role': 'QA Tester',
        'name': 'Quality Assurance',
        'email': 'qa@company.com',
        'last_login': None
    }
}

# Store contact messages
contact_messages = []

@app.route('/')
def index():
    """Enhanced home page with better UX"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Enhanced login with better validation and user experience"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Enhanced validation
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')
        
        # Check credentials
        if username in users_db and users_db[username]['password'] == password:
            # Update last login
            users_db[username]['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Set session
            session['username'] = username
            session['user_role'] = users_db[username]['role']
            session['user_name'] = users_db[username]['name']
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            flash(f'Welcome back, {users_db[username]["name"]}! Login successful.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please check your credentials and try again.', 'error')
            # Add small delay for security
            import time
            time.sleep(1)
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Enhanced dashboard with user analytics"""
    if 'username' not in session:
        flash('Please login to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = users_db[username]
    
    # Dashboard analytics
    dashboard_data = {
        'total_users': len(users_db),
        'user_role': session.get('user_role', 'User'),
        'login_time': session.get('login_time', 'Unknown'),
        'last_login': user_data.get('last_login', 'First login'),
        'session_duration': 'Active'
    }
    
    return render_template('dashboard.html', 
                         username=session['username'],
                         user_data=user_data,
                         dashboard_data=dashboard_data)

@app.route('/logout')
def logout():
    """Enhanced logout with session cleanup"""
    username = session.get('username', 'User')
    user_name = session.get('user_name', username)
    
    # Clear session
    session.clear()
    
    flash(f'Goodbye {user_name}! You have been securely logged out. Thank you for using our platform.', 'info')
    return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Enhanced contact form with better validation"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Enhanced validation
        errors = []
        
        if not name or len(name) < 2:
            errors.append('Name must be at least 2 characters long.')
        
        if not email:
            errors.append('Email address is required.')
        elif '@' not in email or '.' not in email.split('@')[-1]:
            errors.append('Please enter a valid email address.')
        elif len(email.split('@')[0]) < 1 or len(email.split('@')[1]) < 4:
            errors.append('Please enter a valid email address.')
        
        if not subject or len(subject) < 5:
            errors.append('Subject must be at least 5 characters long.')
        
        if not message or len(message) < 10:
            errors.append('Message must be at least 10 characters long.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            # Save message
            message_data = {
                'id': len(contact_messages) + 1,
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'user': session.get('username', 'Anonymous')
            }
            contact_messages.append(message_data)
            
            flash(f'Thank you {name}! Your message "{subject}" has been sent successfully. We will respond within 24 hours.', 'success')
            return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/about')
def about():
    """Enhanced about page with more details"""
    return render_template('about.html')

@app.route('/features')
def features():
    """New features showcase page"""
    return render_template('features.html')

@app.route('/api/health')
def api_health():
    """API endpoint for testing"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'users_online': len([u for u in users_db if users_db[u].get('last_login')])
    })

@app.route('/profile')
def profile():
    """User profile page"""
    if 'username' not in session:
        flash('Please login to view your profile.', 'warning')
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = users_db[username]
    
    return render_template('profile.html', 
                         username=username, 
                         user_data=user_data)

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error page"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Custom 500 error page"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🌐 PROFESSIONAL SELENIUM TESTING DEMO")
    print("=" * 50)
    print("📍 URL: http://localhost:5000")
    print("🔐 Enhanced Authentication System")
    print("👥 Test User Accounts:")
    print("   • admin / password123 (Administrator)")
    print("   • student / student123 (Student)")
    print("   • test_user / test123 (Test User)")
    print("   • qa_tester / qa123 (QA Tester)")
    print("🚀 Professional Features:")
    print("   • Enhanced UI/UX Design")
    print("   • Role-based Access Control")
    print("   • Session Management")
    print("   • Contact Form with Validation")
    print("   • User Profiles & Analytics")
    print("   • API Endpoints")
    print("   • Error Handling")
    print("🧪 Ready for comprehensive Selenium testing!")
    print("=" * 50)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
