🧠 Smart Health Advisor 💊

Smart Health Advisor is an AI-powered platform that assists users with medical consultation, mental health support, and affordable medicine recommendations. The goal is to make healthcare more **accessible**, **affordable**, and **personalized** through intelligent technology.

🌟 Key Features

🩺 1. Medicine Consultation  
Get quick, AI-based diagnosis suggestions based on symptoms entered by the user. Also receive treatment tips and health education.

🧠 2. Mental Health Support Chatbot  
A friendly and intelligent chatbot that listens to your thoughts, provides emotional support, stress-relief exercises, and connects you with resources.

💊 3. Generic Medicine Recommendation  
Suggests cost-effective generic alternatives to branded medications, saving money while ensuring effectiveness.

� 4. Cheaper / Good Alternate Medicines (new)

This project now includes a small feature on the chat page that lets users enter a medicine name and receive suggested alternatives. There are two modes:

- Local dataset fallback (default): The app uses `datasets/medications.csv` to suggest alternatives using substring and fuzzy matching. This requires no external API key and works out-of-the-box.
- External provider (optional): If you have a medicine-pricing or alternate-medicine API, set the `ALTERNATE_MEDICINE_API` key in your `.env` file (or use `.env.example` as a template). The app will call the provider and return priced alternatives when available.

How to enable provider-based results:

1. Copy `.env.example` to `.env` at the project root.
2. Edit `.env` and set `ALTERNATE_MEDICINE_API` with your API key.
3. (Optional) Set `ALTERNATE_MEDICINE_ENDPOINT` to the provider's search endpoint if it differs from the default placeholder.

Example `.env` (DO NOT commit your real `.env`):

```
ALTERNATE_MEDICINE_API=your_provider_api_key_here
ALTERNATE_MEDICINE_ENDPOINT=https://api.yourprovider.example/search
FLASK_SECRET_KEY=change_this_to_a_secret
```

Behavior when provider is not configured:

- The UI will still show suggested alternatives from the bundled dataset, but it won't include price or pharmacy links.


�🛠️ Tech Stack

| Layer      | Technologies Used                   |
|------------|--------------------------------------|
| Frontend   | HTML, CSS, JavaScript                |
| Backend    | Flask (Python)                       |
| Data       | CSV Files for symptoms, medicines, etc.|
