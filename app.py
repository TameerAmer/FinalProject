from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify,make_response
from DB_connection import ConnectDatabase

app = Flask(__name__)
app.secret_key = 'OptiVision_Tameer_Redan'  

db = ConnectDatabase()

@app.route('/')
def login():
    if 'user_name' in session:
        session.clear()  # Clear any existing session
    response = make_response(render_template('login.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/login', methods=['POST'])
def login_process():
    email = request.form['email']
    password = request.form['password']
    
    result = db.login(email, password)
    
    if result == "True details":
        user_id = db.get_user_id(email)  # Get the user ID from the database
        session['user_id'] = user_id  # Store the user ID in the session
        session['user_name'] = db.get_user_name(email)  # Optionally store the username
        return redirect(url_for('dashboard'))
    elif result == "Email does not exist":
        flash('Email does not exist', 'error')
    else:
        flash('Incorrect password', 'error')
    
    return redirect(url_for('login'))


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_process():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('register'))
    
    result = db.register(name, email, password)
    
    if result == "success":
        flash('Successfully Registered!', 'success')
        return redirect(url_for('login'))
    elif result == "Email already exists":
        flash('Email already exists', 'error')
    else:
        flash(f'Registration failed: {result}', 'error')
    
    return redirect(url_for('register'))


@app.route('/dashboard')
def dashboard():
    if 'user_name' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user_name = session['user_name']
    
    # Get test counts for the user
    total_tests = db.get_total_tests_count(user_id)
    
    # Prevent caching of the dashboard page
    response = make_response(render_template('dashboard.html', 
        user_name=user_name, 
        total_tests=total_tests
    ))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    return response
 

@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session', '', expires=0)  # Expire the session cookie
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response



@app.route('/allTests')
def allTests():
    if 'user_name' not in session:
        return redirect(url_for('login'))  
    user_name = session['user_name']  # Get user name from session
    response = make_response(render_template('allTests.html', user_name=user_name))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    return response

@app.route('/VisualAcuityTest')
def VisualAcuityTest():
    if 'user_name' not in session:
        return redirect(url_for('login'))  
    user_name = session['user_name']  # Get user name from session
    return render_template('VisualAcuityTest.html', user_name=user_name)

@app.route('/ColorVisionTest')
def ColorVisionTest():
    if 'user_name' not in session:
        return redirect(url_for('login'))  
    user_name = session['user_name']  # Get user name from session
    return render_template('ColorVisionTest.html', user_name=user_name)

@app.route('/ContrastVisionTest')
def ContrastVisionTest():
    if 'user_name' not in session:
        return redirect(url_for('login'))  
    user_name = session['user_name']  # Get user name from session
    return render_template('ContrastVisionTest.html', user_name=user_name)

@app.route('/BlurCheckTest')
def BlurCheckTest():
    if 'user_name' not in session:
        return redirect(url_for('login'))  
    user_name = session['user_name']  # Get user name from session
    return render_template('BlurCheckTest.html', user_name=user_name)

@app.route('/VWatchTheDotTest')
def WatchTheDotTest():
    if 'user_name' not in session:
        return redirect(url_for('login'))  
    user_name = session['user_name']  # Get user name from session
    return render_template('WatchTheDotTest.html', user_name=user_name)

@app.route('/save-results', methods=['POST'])
def save_results():
    # Get the JSON data from the frontend
    data = request.get_json()
    left_eye_level = data.get('leftEyeLevel')
    right_eye_level = data.get('rightEyeLevel')
    incorrect_answers = data.get('incorrectAnswers')
    highest_level_passed = data.get('highestLevelPassed')
    left_eye_incorrect = data.get('leftEyeIncorrect')
    right_eye_incorrect = data.get('rightEyeIncorrect')
    feedback=data.get('feedBack')

    # Get the user ID from the session (ensure the user is logged in)
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401
    
    user_id = session['user_id']  # Get the current logged-in user's ID from session
    
    # Call the function to save the results to the database
    success = db.save_test_result(user_id, right_eye_level,right_eye_incorrect,left_eye_level,left_eye_incorrect,feedback)
    
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'Failed to save results'}), 500

@app.route('/TestsSection')
def TestsSection():
    if 'user_name' not in session:
        return redirect(url_for('login'))  
    response = make_response(render_template('TestsSection.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    return response

@app.route('/reports')
def reports():
    if 'user_name' not in session:
        return redirect(url_for('login'))  
    response = make_response(render_template('Reports.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    return response

if __name__ == '__main__':
    app.run(debug=True)