# AI Interview Coach

An interactive interview practice system built with Streamlit, NLP, and audio prosody analysis.
Users practice questions, record answers, and receive instant AI-powered feedback on clarity, confidence, fluency, and content quality.

## 🚀 Features

* Role-based interview questions (Data Scientist, QA, SE, etc.)

* Text + audio answer support

* NLP-powered written answer feedback

* Prosody-based voice analysis

* Automatic scoring + strengths + improvements

* Clean, modern UI with custom theme

* Multi-step workflow (Role → Experience → Difficulty → Question → Feedback)

## 🏗 Tech Stack

**Frontend**

* Streamlit

* Custom HTML/CSS styling

* Dynamic multi-page navigation

**Backend**

* Python

* Audio processing + prosody extraction

* NLP evaluation

* ML models for communication traits

* SQLite database for saving results

***ML / AI Components***

* Custom-trained prosody feature classifier

* Text-feedback model using GPT API

* Audio feature extraction pipeline

* Data Handling

* Role-based question loader

## Project Structure<br>
AI Interview Coach/ <br>
│<br>
├── pages/<br>
│   ├── Practice.py<br>
│   ├── Practice_Question.py<br>
│   ├── Practice_one.py<br>
│   └── gpt_feedback.py<br>
│<br>
├── data/<br>
│   ├── data_scientist.json<br>
│   ├── qa_analyst.json<br>
│   ├── software_engineer.json<br>
│   └── ...<br>
│<br>
├── Theme.py<br>
├── question_loader.py<br>
├── model_loader.py<br>
├── prosody_extractor.py<br>
├── database.py<br>
└── README.md<br>

## 📘 Example Workflow <br>

1️⃣ Choose a role <br>
2️⃣ Select experience, difficulty, question mode<br>
3️⃣ Pick a question<br>
4️⃣ Type or record your answer<br>
5️⃣ Get instant AI feedback:<br>
   * GPT text evaluation<br>
   * Prosody-based voice metrics<br>
   * Strengths & improvements <br>
   * Score out of 10<br>
   * 1GB original dataset split into multiple JSON chunks<br>
   * Cached loading for performance

## Snapshot of UI
<img src="Climate Change Dashboard/assets/screenshots/Screenshot 2024-11-18 153514.png" width="600">
<br><br>

## 🚧 Future Improvements<br>

* Add mock interview mode with timed questions
* Add performance history dashboard
* Add comparisons vs average candidate performance
* Support video-based feedback
* Add more roles and question datasets
