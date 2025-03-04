import json


class AnalysisReport:
    """
    A class that represents the analysis report for a CV and job description match.

    Attributes:
        match_score (int): A score (0-100) indicating the match between the CV and job description.
        skill_gaps (list): A list of skill gaps identified in the CV.
        recommendations (list): A list of recommendations for the candidate.

    Methods:
        to_json(): Converts the analysis report into a well-formatted JSON string.
    """

    def __init__(self, analysis_data):
        """
        Initializes the AnalysisReport with the provided analysis data.

        Parameters:
            analysis_data (dict): The analysis results that include match score, skill gaps, and recommendations.
        """
        self.match_score = analysis_data.get("match_score", 0)
        self.skill_gaps = analysis_data.get("skill_gaps", [])
        self.recommendations = analysis_data.get("recommendations", [])

    def to_json(self):
        """
        Converts the analysis results into a JSON string.

        Returns:
            str: A JSON string representation of the analysis results, formatted with indentation.
        """
        return json.dumps({
            "match_score": self.match_score,
            "skill_gaps": self.skill_gaps,
            "recommendations": self.recommendations
        }, indent=4, ensure_ascii=False)  # Ensuring non-ASCII characters are not escaped
