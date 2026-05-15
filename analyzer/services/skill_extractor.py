import os
import json
import re
from django.conf import settings

class SkillExtractorService:
    def __init__(self):
        self.dataset_path = os.path.join(settings.BASE_DIR, 'data', 'skills_dataset.json')
        self.skills_matrix = self._load_dataset()

    def _load_dataset(self) -> dict:
        try:
            with open(self.dataset_path, 'r') as f:
                return json.load(f)
        except Exception:
            # Failsafe in case structural setup missing file execution
            return {
                "languages": ["python", "javascript", "java", "c++", "ruby", "sql", "html", "css"],
                "frameworks": ["django", "flask", "react", "vue", "angular", "bootstrap"],
                "tools": ["git", "docker", "kubernetes", "jenkins", "postman"],
                "databases": ["postgresql", "mysql", "sqlite", "mongodb", "redis"],
                "cloud": ["aws", "azure", "gcp"],
                "ai_ml": ["scikit-learn", "tensorflow", "pytorch", "pandas", "numpy"],
                "soft_skills": ["communication", "leadership", "teamwork", "agile", "scrum"]
            }

    def extract_skills(self, text: str) -> dict:
        """
        Applies a word-boundary token matching sequence across data vectors to map present tokens 
        by specific categorizations. Returns categorized listings.
        """
        extracted = {}
        cleaned_text = f" {text.lower()} "
        # Handle structural characters for specific edge cases like C++ / C# / .NET / Next.js
        cleaned_text = re.sub(r'[\s,.:;]', ' ', cleaned_text)
        
        for category, skill_list in self.skills_matrix.items():
            extracted[category] = []
            for skill in skill_list:
                # Safely escape programming chars
                escaped_skill = re.escape(skill)
                pattern = r'(?<= )' + escaped_skill + r'(?= )'
                if re.search(pattern, cleaned_text, re.IGNORECASE):
                    if skill not in extracted[category]:
                        extracted[category].append(skill)
        return extracted