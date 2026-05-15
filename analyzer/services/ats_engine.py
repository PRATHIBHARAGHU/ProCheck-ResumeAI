import re
from .preprocess import NLPPreprocessingService
from .skill_extractor import SkillExtractorService
from .similarity_engine import TFIDFSimilarityEngine
from .semantic_engine import SemanticSimilarityEngine
from .suggestions_engine import AISuggestionsEngine

class ATSScoringEngine:
    def __init__(self):
        self.preprocessor = NLPPreprocessingService()
        self.skill_extractor = SkillExtractorService()
        self.semantic_engine = SemanticSimilarityEngine()

    def analyze(self, resume_text: str, jd_text: str) -> dict:
        # Preprocessing Pipelines
        clean_resume = self.preprocessor.clean_text(resume_text)
        clean_jd = self.preprocessor.clean_text(jd_text)
        
        # Skill Core Extractions
        resume_skills_dict = self.skill_extractor.extract_skills(resume_text)
        jd_skills_dict = self.skill_extractor.extract_skills(jd_text)
        
        # Flatten skills lists for structural intersections
        resume_skills_flat = [s for sublist in resume_skills_dict.values() for s in sublist]
        jd_skills_flat = [s for sublist in jd_skills_dict.values() for s in sublist]
        
        # 1. Keyword Score (30%)
        keyword_score = int(TFIDFSimilarityEngine.calculate_similarity(clean_resume, clean_jd) * 100)
        # Normalize baseline distribution ranges
        keyword_score = min(100, max(25, int(keyword_score * 1.4))) 
        
        # 2. Semantic Score (25%)
        semantic_score = int(self.semantic_engine.calculate_semantic_score(clean_resume, clean_jd) * 100)
        semantic_score = min(100, max(30, int(semantic_score * 1.2)))
        
        # 3. Skills Match Score (20%)
        matched_skills = []
        missing_skills = []
        for s in jd_skills_flat:
            if s in resume_skills_flat:
                matched_skills.append(s)
            else:
                missing_skills.append(s)
                
        if jd_skills_flat:
            skills_score = int((len(matched_skills) / len(jd_skills_flat)) * 100)
        else:
            skills_score = 100
            
        # 4. Resume Section Architecture Score (15%)
        section_score = 0
        sections = ['experience', 'education', 'skills', 'project', 'summary', 'certification']
        for sec in sections:
            if re.search(sec, resume_text.lower()):
                section_score += (100 / len(sections))
        section_score = min(100, int(section_score))
        
        # 5. Formatting & Readability Engine Profile (10%)
        formatting_score = 100
        # Check density parameters for anomalies
        if len(resume_text) < 500:
            formatting_score -= 30
        if re.search(r'[\u2022\u25CF\u25CB\u25AA]', resume_text): # Clean structural separators present
            formatting_score += 5
        formatting_score = min(100, max(40, formatting_score))
        
        # Balanced Macro Structural Formula calculation Architecture Setup
        final_ats_score = int(
            (keyword_score * 0.30) +
            (semantic_score * 0.25) +
            (skills_score * 0.20) +
            (section_score * 0.15) +
            (formatting_score * 0.10)
        )
        final_ats_score = min(100, max(10, final_ats_score))
        
        # Build Suggestions Engine
        suggestions = AISuggestionsEngine.generate_suggestions(
            keyword_score, skills_score, semantic_score, formatting_score, missing_skills
        )
        
        return {
            "final_score": final_ats_score,
            "keyword_score": keyword_score,
            "semantic_score": semantic_score,
            "skills_score": skills_score,
            "formatting_score": section_score, # Mapping structural layout parameters
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions,
            "categorized_resume_skills": resume_skills_dict
        }