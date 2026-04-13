# AI Medical_diagnosis Assistant 

An intelligent, AI-powered medical assistant designed to provide **symptom-based disease prediction**, basic medical guidance, and personalized recommendations through an interactive web interface. This system aims to make **initial healthcare guidance accessible, fast, and user-friendly**, especially for early-stage diagnosis support.

---

##  Features  

* **AI-Based Symptom Analysis** – Predicts possible diseases based on user-selected symptoms  
* **Interactive User Interface** – Clean and simple UI for easy data input  
* **Multi-Step Health Input** – Collects detailed patient data (age, gender, vitals, etc.)  
* **Symptom Severity & Location Selection** – Improves prediction accuracy  
* **Disease Prediction Engine** – Uses AI model / Gemini API  
* **Medical Suggestions** – Provides basic precautions and guidance  
* **Real-Time Results** – Instant output generation  
* **Scalable System** – Can be upgraded with custom ML models  

---

##  System Workflow  

1. Enter personal details (Name, Age, Gender, etc.)  
2. Select symptoms  
3. Provide severity and symptom details  
4. AI processes the data  
5. Displays predicted diseases and suggestions  

---

##  Demo  


### 🔹 User Input Interface  
https://youtu.be/M6h3VSc9Vno?si=FTlLcAKxIODtMHNI

### 🔹 Hardware Setup  
https://youtu.be/SGx74WeUJbQ?si=P-UDxM6Ws-1VZ5T1 


### 🔹 Patient Record Output  

```plaintext
View Record

Original Index: 7  
Date: 2025-02-01  
Time: 20:45:43  

Username: chandru  

Vitals:
- Temperature: 97.58 °F  
- Weight: 3700.47 g  
- Oxygen Level: 96%  
- Pulse Rate: 76 bpm  

Symptoms:
- Headache: Mild  
- Nausea: Occasional  
- Cough: Dry  
- Fatigue: Mild  
- Cold Symptoms: Sneezing, Congestion  
- Stomach Pain: Moderate  
- Other: None  

 AI Prediction:
Possible Conditions:
- Common Cold  
- Gastroenteritis (Stomach Flu)  
- Flu (Influenza)
```

---

##  Sample Output Explanation  

This output shows how the system:
- Collects **patient health data**
- Analyzes **symptoms using AI**
- Predicts **possible diseases**
- Presents results in a **clear structured format**

---

##  Tech Stack  

* **Frontend:** HTML, CSS, JavaScript  
* **Backend:** Python  
* **AI Integration:** Gemini API / ML Model  
* **Tools:** Google Colab, VS Code  

---

##  Project Structure  

```bash
AI-Physician-Assistant/
│── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│
│── backend/
│   ├── app.py
│   ├── model.py
│
│── dataset/
│   ├── symptoms_dataset.csv
│
│── README.md
```

---

##  Installation  

1. Clone the repository  
```bash
git clone https://github.com/your-username/ai-physician-assistant.git
```

2. Navigate to the project  
```bash
cd ai-physician-assistant
```

3. Install dependencies  
```bash
pip install -r requirements.txt
```

4. Run the backend  
```bash
python app.py
```

5. Open frontend  
- Run `index.html` in your browser  

---

##  Future Enhancements  

* Custom ML model training  
* Voice-based symptom input  
* Mobile app version  
* Doctor consultation integration  
* Multi-language support  

---

## Disclaimer  

This project is for **educational purposes only**.  
It is **not a substitute for professional medical advice**.  

Always consult a doctor for medical concerns.
