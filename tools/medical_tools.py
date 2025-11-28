"""
Medical helper tools and utilities
"""
from typing import List, Dict, Optional


class MedicalTools:
    """
    Collection of helper functions to extract disease/location from query
    and format information nicely.
    """

    DISEASE_SYMPTOMS = {
        "diabetes": [
            "increased thirst",
            "frequent urination",
            "fatigue",
            "blurred vision",
            "slow wound healing",
        ],
        "hypertension": [
            "headaches",
            "shortness of breath",
            "nosebleeds",
            "fatigue",
            "chest pain",
        ],
        "asthma": [
            "shortness of breath",
            "chest tightness",
            "wheezing",
            "coughing",
            "difficulty sleeping",
        ],
        "heart disease": [
            "chest pain",
            "shortness of breath",
            "irregular heartbeat",
            "fatigue",
            "dizziness",
        ],
    }

    @staticmethod
    def extract_location_from_query(query: str) -> Optional[str]:
        """
        Very simple location detection from query text.
        """
        cities = {
            "delhi": "Delhi",
            "mumbai": "Mumbai",
            "bombay": "Mumbai",
            "bangalore": "Bangalore",
            "bengaluru": "Bangalore",
            "hyderabad": "Hyderabad",
            "pune": "Pune",
            "kolkata": "Kolkata",
            "chennai": "Chennai",
            "ncr": "Delhi",
        }

        q = query.lower()
        for key, city in cities.items():
            if key in q:
                return city
        return None

    @staticmethod
    def extract_disease_from_query(query: str) -> str:
        """
        Try to detect disease name from query text.
        Defaults to 'general' if nothing matched.
        """
        diseases = [
            "diabetes",
            "hypertension",
            "asthma",
            "heart disease",
            "cancer",
            "kidney disease",
            "liver disease",
            "arthritis",
            "thyroid",
        ]
        q = query.lower()
        for d in diseases:
            if d in q:
                return d
        return "general"

    @staticmethod
    def get_disease_symptoms(disease: str) -> List[str]:
        """
        Return sample symptoms list for a disease (if available).
        """
        return MedicalTools.DISEASE_SYMPTOMS.get(disease.lower(), [])


# Quick manual test
if __name__ == "__main__":
    tools = MedicalTools()
    print(tools.extract_location_from_query("Best hospital in Delhi for heart"))
    print(tools.extract_disease_from_query("I have diabetes and chest pain"))
