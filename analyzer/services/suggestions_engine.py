class AISuggestionsEngine:
    @staticmethod
    def generate_suggestions(
        keyword_score: int, 
        skills_score: int, 
        semantic_score: int, 
        formatting_score: int, 
        missing_skills: list
    ) -> list:
        """
        Heuristic AI Expert Framework execution system mapping diagnostic criteria vectors 
        into optimization workflows.
        """
        suggestions = []
        
        if keyword_score < 70:
            suggestions.append("Align your vocabulary closer to the target job description. Rephrase structural task summaries to echo key phrases explicitly mentioned in the description.")
            
        if missing_skills:
            top_missing = missing_skills[:4]
            suggestions.append(f"Crucial Core Competency Gap Detected: Integrate explicit evidence detailing your operational exposure to: {', '.join(top_missing).upper()}.")
            
        if semantic_score < 65:
            suggestions.append("Enhance Contextual Relevance: The system registers a low semantic density profile. Convert high-level general statements into specific architectural project breakdowns matching the role's scope.")
            
        if skills_score < 60:
            suggestions.append("Structure a dedicated, distinct 'Technical Skills Inventory' section divided by tech stacks (e.g., Languages, Frameworks, Infrastructure) to improve parsing readability.")
            
        if formatting_score < 80:
            suggestions.append("Eliminate complex UI visual blocks: Avoid graphical multi-column components, nested database tables, or vector shape elements. Stick to clean, simple markdown flows for ATS parsers.")
            
        # Default portfolio enhancement strings if score profile is solid
        if len(suggestions) < 3:
            suggestions.append("Implement Metric Quantization: Ensure all major architectural contributions explicitly state key business outcomes using precise percentages, scale numbers, or performance index gains.")
            suggestions.append("Strengthen Action Orientation: Start every core execution bullet point with powerful industry action verbs such as 'Architected', 'Engineered', 'Optimized', or 'Orchestrated'.")
            
        return suggestions