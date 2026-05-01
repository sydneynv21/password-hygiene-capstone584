# password-hygiene-capstone584

# Project Overview
This project is an AI-powered password hygiene coaching application I built for my masters capstone course in Spring 2026. The tool was designed to provide tailored and actionable guidance adapted to the user's password strength metrics and their level of technical expertise. It analyzes passwords based on multiple security criteria and generates personalized recommendations using an AI model to improve password quality and user understanding of security principles.

<img width="1074" height="969" alt="Screenshot 2026-04-19 223208" src="https://github.com/user-attachments/assets/32c3108d-b2b4-4f50-812d-fd9c59d5c653" />

# Purpose
The project addresses both user and design limitations in current password security solutions with the integration of AI generated feedback tailored to the user. By presenting recommendations in a way that is comprehensible and actionable, cognitive barriers and ineffective design choices that lead to neglect can be mitigated. 
Furthermore, the project was designed with the intent to make cybersecurity more achievable to the broader population of technology users, not just those who are technically experienced. 

# Project Methodology
<img width="874" height="219" alt="Screenshot 2026-04-30 210458" src="https://github.com/user-attachments/assets/8fdcab28-7805-4d61-b62a-2effa6384bb4" />

1. The user inputs a password into the interface
2. Local analysis of password occurs using multiple metrics (length and character diversity, presence of common dictionary words, comparison against exposed password dataset)
3. Strength score and risk classification summary generated from metrics
4. Metrics summary and user's technical experience level sent to locally hosted Ollama LLM through currated prompt
5. Model responds with targeted recommendations for improvement, providing user-friendly guidance through interface

# Code Structure
<img width="1069" height="270" alt="Screenshot 2026-04-19 221631" src="https://github.com/user-attachments/assets/d7c678d7-848e-4d97-845f-7dc70a302f95" />

# How to Run Project Yourself
1. Clone the repository
2. Download and install Ollama from https://ollama.com/ 
3. Install the required model:
`ollama pull llama3.1:8b`
4. Create and activate a virtual environment (optional):
`python -m venv venv`
`venv\Scripts\activate`
5. Install required dependencies:
`pip install -r requirements.txt`
6. Run the application:
`python main.py`
7. To run the included test cases:
`python test_runner.py`

# Important Notes
- This project includes a trimmed version of the RockYou dataset from https://github.com/josuamarcelc/common-password-list
- This tool is an educational prototype and was designed to run locally
- User passwords are not stored nor are they shared with the LLM




