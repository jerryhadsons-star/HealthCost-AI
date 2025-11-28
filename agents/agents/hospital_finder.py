"""
Hospital Finder Agent - Recommends hospitals based on criteria
"""
import pandas as pd
from typing import List, Dict, Optional
import os


class HospitalFinderAgent:
    def __init__(self, hospital_csv_path: str = "data/hospitals_sample.csv"):
        """
        Initialize Hospital Finder with dataset.
        If CSV not found, uses small built‑in sample data.
        """
        self.csv_path = hospital_csv_path

        if os.path.exists(hospital_csv_path):
            self.hospitals_df = pd.read_csv(hospital_csv_path)
        else:
            self.hospitals_df = self._create_sample_data()

    def _create_sample_data(self) -> pd.DataFrame:
        """
        Create small sample hospital data for testing.
        This will be used if real CSV is missing.
        """
        data = {
            "Hospital_Name": [
                "Apollo Hospitals",
                "Max Healthcare",
                "Fortis Healthcare",
                "AIIMS Delhi",
                "Lilavati Hospital",
                "Hinduja Hospital",
            ],
            "City": ["Delhi", "Delhi", "Mumbai", "Delhi", "Mumbai", "Mumbai"],
            "State": [
                "Delhi",
                "Delhi",
                "Maharashtra",
                "Delhi",
                "Maharashtra",
                "Maharashtra",
            ],
            "Hospital_Type": [
                "Private",
                "Private",
                "Private",
                "Government",
                "Private",
                "Private",
            ],
            "Specialties": [
                "Cardiology, Oncology, Neurology, Endocrinology",
                "Cardiology, Orthopedics, Pediatrics, General Medicine",
                "General, Trauma, Surgery, Orthopedics",
                "Teaching Hospital, All Specialties",
                "Cardiology, Gastroenterology, Nephrology",
                "Cardiology, Urology, Neurology, Oncology",
            ],
            "Beds": [500, 450, 350, 1600, 600, 700],
            "Contact": [
                "+91-11-47444444",
                "+91-11-45018000",
                "+91-22-67676767",
                "+91-11-26165050",
                "+91-22-68644444",
                "+91-22-67888888",
            ],
        }
        return pd.DataFrame(data)

    def find_hospitals(
        self,
        disease: Optional[str] = None,
        location: Optional[str] = None,
        hospital_type: Optional[str] = None,
        top_n: int = 5,
    ) -> Dict:
        """
        Find suitable hospitals based on:
        - disease (optional, used to match specialties)
        - location (city name)
        - hospital_type (Private / Government etc.)
        """
        df = self.hospitals_df.copy()

        # Filter by city / location
        if location:
            df = df[df["City"].str.contains(location, case=False, na=False)]

        # Filter by hospital type
        if hospital_type:
            df = df[
                df["Hospital_Type"].str.contains(hospital_type, case=False, na=False)
            ]

        # Filter by disease specialties (very simple matching)
        if disease:
            df = df[
                df["Specialties"].str.contains(disease, case=False, na=False)
                | df["Hospital_Type"].str.contains("Private", case=False, na=False)
            ]

        if df.empty:
            return {
                "status": "not_found",
                "message": "No hospitals found for given criteria.",
                "criteria": {
                    "disease": disease,
                    "location": location,
                    "hospital_type": hospital_type,
                },
            }

        results: List[Dict] = []
        for _, row in df.head(top_n).iterrows():
            results.append(
                {
                    "name": row.get("Hospital_Name", "N/A"),
                    "city": row.get("City", "N/A"),
                    "state": row.get("State", "N/A"),
                    "type": row.get("Hospital_Type", "N/A"),
                    "specialties": row.get("Specialties", "N/A"),
                    "beds": int(row.get("Beds", 0)),
                    "contact": row.get("Contact", "N/A"),
                }
            )

        return {
            "status": "success",
            "found_count": len(results),
            "hospitals": results,
            "criteria": {
                "disease": disease,
                "location": location,
                "hospital_type": hospital_type,
            },
        }


# Quick manual test (for local run only)
if __name__ == "__main__":
    finder = HospitalFinderAgent()
    out = finder.find_hospitals(
        disease="Cardiology",
        location="Delhi",
        hospital_type="Private",
        top_n=3,
    )
    print(out)
