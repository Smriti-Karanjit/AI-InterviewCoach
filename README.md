**AI Interview Coach
**
An interactive interview practice system built with Streamlit, NLP, and audio prosody analysis.
Users practice questions, record answers, and receive instant AI-powered feedback on clarity, confidence, fluency, and content quality.

🚀 Features

Role-based interview questions (Data Scientist, QA, SE, etc.)

Text + audio answer support

NLP-powered written answer feedback

Prosody-based voice analysis

Automatic scoring + strengths + improvements

Clean, modern UI with custom theme

Multi-step workflow (Role → Experience → Difficulty → Question → Feedback)

🏗 Tech Stack
Frontend

Streamlit

Custom HTML/CSS styling

Dynamic multi-page navigation

Backend

Python

Audio processing + prosody extraction

NLP evaluation

ML models for communication traits

SQLite database for saving results

ML / AI Components

Custom-trained prosody feature classifier

Text-feedback model using GPT API

Audio feature extraction pipeline

Data Handling

Role-based question loader

**Project Structure**
AI Interview Coach/
│
├── pages/
│   ├── Practice.py
│   ├── Practice_Question.py
│   ├── Practice_one.py
│   └── gpt_feedback.py
│
├── data/
│   ├── data_scientist.json
│   ├── qa_analyst.json
│   ├── software_engineer.json
│   └── ...
│
├── Theme.py
├── question_loader.py
├── model_loader.py
├── prosody_extractor.py
├── database.py
└── README.md

**📘 Example Workflow**

1️⃣ Choose a role
2️⃣ Select experience, difficulty, question mode
3️⃣ Pick a question
4️⃣ Type or record your answer
5️⃣ Get instant AI feedback:

GPT text evaluation

Prosody-based voice metrics

Strengths & improvements

Score out of 10
1GB original dataset split into multiple JSON chunks

Cached loading for performance

**🚧 Future Improvements**

Add mock interview mode with timed questions

Add performance history dashboard

Add comparisons vs average candidate performance

Support video-based feedback

Add more roles and question datasets
