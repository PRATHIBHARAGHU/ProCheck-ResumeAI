# ProCheck-ResumeAI: Smart Resume Analyzer

An advanced, production-grade **AI-driven ATS (Applicant Tracking System)** that evaluates resume compatibility against corporate Job Descriptions using multi-vector data pipelines and Semantic Analysis.

---

## Component Architecture

### 1. Multi-Vector Analytical Engine
The platform calculates a balanced compatibility score by compiling metrics across four distinct matrices:
* **Keyword Matching:** TF-IDF frequency analysis for industry-specific terminology.
* **Semantic Alignment:** Deep-learning-based meaning extraction (not just keyword counting).
* **Technical Skill Density:** Cross-referencing against a library of 200+ technology skills.
* **Structural Integrity:** Evaluation of document layout, sectioning, and formatting readability.

### 2. Advanced NLP Pipeline
The system utilizes a cascading processing layer to clear structural "noise" from documents:
* **Preprocessing:** Lemmatization and stop-word removal using `spaCy` and `NLTK`.
* **Tokenization:** Context-aware corpus splitting for precise vector mapping.
* **Vectorization:** Leveraging `scikit-learn` for mathematical text representation.

### 3. Contextual Semantic Matching
Integrates `sentence-transformers` (specifically the `all-MiniLM-L6-v2` model) to process deep conceptual structures. This allows the engine to understand that "Developing web apps" is semantically similar to "Full-stack software engineering."

### 4. Enterprise-Grade UI/UX
* **Modern Interface:** Built with **Tailwind CSS** featuring a minimalist, high-contrast Dark/Light mode.
* **Data Visualization:** Real-time interactive analytics and "ATS Gauges" powered by **Chart.js**.

---

##  Execution & Setup

Follow these directives to initialize the workspace local server environment:

### 1. Initialize & Activate Environment
python -m venv venv
for Windows:
venv\Scripts\activate
for macOS/Linux:
source venv/bin/activate

### 2. Install Dependency Stack
pip install -r requirements.txt
python -m spacy download en_core_web_sm

### 3. Database Initialization
python manage.py migrate
python manage.py createsuperuser

### 4. Launch Local Runtime
python manage.py runserver

## Future Roadmap
### LLM Integration: 
Implementing GPT-4/Llama-3 for personalized resume improvement suggestions.

### Multi-Format Export: 
Generating downloadable PDF reports for users.

### Recruiter Portal: 
Allowing HR teams to rank multiple resumes against a single job posting.

**Developed by Prathibha R** *AIML Undergraduate | Alva's Institute of Engineering and Technology (AIET)* [GitHub Profile](https://github.com/PRATHIBHARAGHU)