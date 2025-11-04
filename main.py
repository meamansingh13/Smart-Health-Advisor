from flask import Flask, request, render_template, jsonify, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash
import numpy as np
import pandas as pd
import pickle
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')

# Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')  # Needed for session handling

# Load datasets
df_symptoms = pd.read_csv("datasets/symtoms_df.csv")
precautions = pd.read_csv("datasets/precautions_df.csv")
workout = pd.read_csv("datasets/workout_df.csv")
description = pd.read_csv("datasets/description.csv")
medications = pd.read_csv('datasets/medications.csv')
diets = pd.read_csv("datasets/diets.csv")

# Load model
svc = pickle.load(open('models/svc.pkl', 'rb'))

# In-memory user store (for demonstration)
users = {}

# Helper function
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis]['workout']
    return desc, pre, med, die, wrkout

# Symptoms and diseases
symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}

def get_predicted_value(patient_symptoms):
    try:
        input_vector = np.zeros(len(symptoms_dict))
        for item in patient_symptoms:
            if item in symptoms_dict:
                input_vector[symptoms_dict[item]] = 1
        pred_index = svc.predict([input_vector])[0]
        # map predicted index to disease name; if missing, return informative string
        return diseases_list.get(pred_index, f'Unknown disease (code {pred_index})')
    except Exception as e:
        # log server side for debugging and re-raise so caller can handle
        print('Error in get_predicted_value:', repr(e))
        raise

# Routes
@app.route("/")
def index():
    user = session.get('user')
    return render_template("index.html", user=user)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            symptoms = request.form.get('symptoms')
            if symptoms == "Symptoms" or not symptoms:
                message = "Please enter your symptoms (comma separated) or correct any misspelling."
                # If this is an AJAX request, return JSON with error
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'error': message}), 400
                return render_template('index.html', message=message, user=session.get('user'))

            user_symptoms = [s.strip("[]' ") for s in symptoms.split(',')]
            predicted_disease = get_predicted_value(user_symptoms)
            dis_des, pre, med, diet, wrkout = helper(predicted_disease)

            # normalize results to plain Python types for JSON
            my_precautions = []
            try:
                for i in pre[0]:
                    if pd.isna(i):
                        continue
                    my_precautions.append(str(i))
            except Exception:
                # Fallback in case pre is not indexable
                if isinstance(pre, (list, tuple)):
                    for item in pre:
                        if item:
                            my_precautions.append(str(item))

            # Convert medications, diet, workout to lists of strings
            def to_str_list(x):
                try:
                    return [str(v) for v in list(x)]
                except Exception:
                    return [str(x)] if x is not None else []

            med_list = to_str_list(med)
            diet_list = to_str_list(diet)
            workout_list = to_str_list(wrkout)

            # If this is an AJAX request, return JSON so frontend can re-render in-place
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'predicted_disease': str(predicted_disease),
                    'description': str(dis_des),
                    'precautions': my_precautions,
                    'medications': med_list,
                    'diet': diet_list,
                    'workout': workout_list
                })

            return render_template('index.html', predicted_disease=predicted_disease, dis_des=dis_des,
                                   my_precautions=my_precautions, medications=med_list, my_diet=diet_list,
                                   workout=workout_list, user=session.get('user'))
        except Exception as e:
            # Log exception server-side and return a helpful JSON error for AJAX clients
            print('Error in /predict:', repr(e))
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': str(e)}), 500
            # For non-AJAX, show a flash message and render
            flash('An error occurred while processing your request: ' + str(e))
            return render_template('index.html', user=session.get('user'))

    return render_template('index.html', user=session.get('user'))

@app.route('/about')
def about():
    return render_template("about.html", user=session.get('user'))

@app.route('/contact')
def contact():
    return render_template("contact.html", user=session.get('user'))

@app.route('/blog')
def blog():
    return render_template("blog.html", user=session.get('user'))


# ----------------- Emotional Health Chatbot -----------------
def emotional_bot_response(message_text):
    """Return an appropriate bot response for an emotional support chat using Gemini AI.
    Types: 'crisis', 'support', 'info', 'referral'
    """
    if not message_text:
        return {"reply": "I'm here to listen. Tell me a little about how you're feeling.", "type": "support"}

    text = message_text.lower()

    # Crisis keywords that require immediate intervention
    crisis_keywords = ["suicide", "kill myself", "end my life", "hurt myself", "i want to die", 
                      "self harm", "self-harm", "hang myself", "kill me"]
    
    if any(kw in text for kw in crisis_keywords):
        reply = (
            "I'm really sorry you're feeling this way. If you're thinking about hurting yourself or ending your life, "
            "please consider contacting local emergency services or a crisis hotline right now. "
            "If you are in the United States you can call or text 988 to reach the Suicide & Crisis Lifeline. "
            "If you're elsewhere, please contact local emergency services or a trusted person immediately. "
            "If you'd like, I can provide coping suggestions and resources or connect you with helplines in your country."
        )
        return {"reply": reply, "type": "crisis"}

    try:
        # Prepare prompt for Gemini AI with safety guidelines
        prompt = f"""You are an empathetic emotional support chatbot. The user has said: "{message_text}"

        Please provide a caring, supportive response while:
        1. Never providing medical advice or diagnosis
        2. Always encouraging professional help for serious issues
        3. Focusing on emotional support and active listening
        4. Suggesting healthy coping strategies when appropriate
        5. Being mindful of cultural sensitivity
        6. Maintaining appropriate boundaries

        Keep the response conversational and under 150 words.
        """

        # Get response from Gemini
        response = model.generate_content(prompt)
        reply = response.text.strip()

        # Determine response type based on content
        resp_type = "support"  # default type
        if "professional" in reply.lower() or "therapist" in reply.lower():
            resp_type = "referral"
        elif "cope" in reply.lower() or "strategy" in reply.lower():
            resp_type = "info"

        return {"reply": reply, "type": resp_type}

    except Exception as e:
        print(f"Error using Gemini AI: {str(e)}")
        # Fallback response if AI fails
        return {
            "reply": "I'm here to listen and support you. Would you like to tell me more about what's troubling you?",
            "type": "support"
        }


@app.route('/chat')
def chat():
    """Render the emotional support chat page."""
    return render_template('chat.html', user=session.get('user'))


@app.route('/chat_api', methods=['POST'])
def chat_api():
    """Simple API endpoint for chatbot. Accepts JSON {message: '...'} and returns JSON reply."""
    try:
        data = request.get_json() or {}
        message = data.get('message', '')
        resp = emotional_bot_response(message)
        return jsonify(resp)
    except Exception as e:
        print('Error in /chat_api:', repr(e))
        return jsonify({'reply': 'Sorry — an error occurred while processing your message.', 'type': 'error'}), 500

# -----------------------------------------------------------

# ---------- Authentication Routes ----------

users = {
    'test@example.com': {'password': '12345', 'username': 'Aman'},
    'alice@example.com': {'password': 'alice123', 'username': 'Alice'},
    'bob@example.com': {'password': 'bob321', 'username': 'Bob'},
    'charlie@example.com': {'password': 'charlie@2024', 'username': 'Charlie'},
    'dave@example.com': {'password': 'davepass', 'username': 'Dave'},
    'eve@example.com': {'password': 'evepass123', 'username': 'Eve'},
    'frank@example.com': {'password': 'frank007', 'username': 'Frank'},
    'grace@example.com': {'password': 'gracepass', 'username': 'Grace'},
    'harry@example.com': {'password': 'harrypotter', 'username': 'Harry'},
    'ivy@example.com': {'password': 'ivypass', 'username': 'Ivy'}
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = users.get(email)
        if user and user['password'] == password:
            session['user'] = user['username']
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password!')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if email in users:
            flash("Email already registered.")
            return redirect(url_for("signup"))
        else:
            users[email] = {
                "name": name,
                "password": generate_password_hash(password)
            }
            session["user"] = name
            flash("Signed up successfully!")
            return redirect(url_for("index"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.")
    return redirect(url_for("index"))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
