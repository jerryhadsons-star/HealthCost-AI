"""
Supervisor Agent - Routes queries to appropriate agents using a simple workflow
"""
from typing import Dict
from agents.health_advisor import HealthAdvisorAgent
from agents.hospital_finder import HospitalFinderAgent
from agents.cost_estimator import CostEstimatorAgent
from tools.medical_tools import MedicalTools


class SupervisorAgent:
    """
    Main controller that understands the user query
    and decides which agents to call (health, hospital, cost).
    """

    def __init__(self):
        self.health_advisor = HealthAdvisorAgent()
        self.hospital_finder = HospitalFinderAgent()
        self.cost_estimator = CostEstimatorAgent()
        self.tools = MedicalTools()

    def _needs_health_info(self, query: str) -> bool:
        keywords = ["what is", "symptom", "symptoms", "disease", "bimari", "health", "info"]
        q = query.lower()
        return any(k in q for k in keywords)

    def _needs_hospital(self, query: str) -> bool:
        keywords = ["hospital", "doctor", "where", "best hospital", "admit", "treatment"]
        q = query.lower()
        return any(k in q for k in keywords)

    def _needs_cost(self, query: str) -> bool:
        keywords = ["cost", "price", "kitna", "kharcha", "expense", "fees", "charges"]
        q = query.lower()
        return any(k in q for k in keywords)

    def process(self, query: str) -> str:
        """
        Main function: takes user query (string), returns combined response (string).
        """

        query = query.strip()
        if not query:
            return "Please enter a valid question."

        # Decide which info is needed
        wants_health = self._needs_health_info(query)
        wants_hospital = self._needs_hospital(query)
        wants_cost = self._needs_cost(query)

        # Try to guess disease + location from query
        disease = self.tools.extract_disease_from_query(query)
        location = self.tools.extract_location_from_query(query)

        parts: list[str] = []

        # 1) Health information
        if wants_health:
            disease_for_info = query if disease == "general" else disease
            info = self.health_advisor.get_disease_info(disease_for_info)
            if info["status"] == "success":
                parts.append("📋 HEALTH INFORMATION\n" + info["information"])
            else:
                parts.append("📋 HEALTH INFORMATION\nSorry, could not fetch disease information.")

        # 2) Hospital recommendations
        if wants_hospital:
            hospital_result = self.hospital_finder.find_hospitals(
                disease=None if disease == "general" else disease,
                location=location,
                hospital_type="Private",
                top_n=5,
            )
            if hospital_result["status"] == "success":
                hospitals_text = "🏥 HOSPITAL RECOMMENDATIONS\n"
                for i, hosp in enumerate(hospital_result["hospitals"], start=1):
                    hospitals_text += (
                        f"\n{i}. {hosp['name']} ({hosp['city']}, {hosp['state']})"
                        f"\n   Type: {hosp['type']}"
                        f"\n   Specialties: {hosp['specialties']}"
                        f"\n   Beds: {hosp['beds']}"
                        f"\n   Contact: {hosp['contact']}\n"
                    )
                parts.append(hospitals_text)
            else:
                parts.append("🏥 HOSPITAL RECOMMENDATIONS\nNo hospitals found for given criteria.")

        # 3) Cost estimation
        if wants_cost:
            cost_result = self.cost_estimator.estimate_total_healthcare_cost(
                disease=disease if disease != "general" else "diabetes",
                hospital_type="private",
                hospital_days=3,
                opd_visits_per_year=12,
            )
            if cost_result["status"] == "success":
                summary = cost_result["summary"]
                cost_text = (
                    "💰 COST ESTIMATES\n"
                    f"- Annual Medicines: ₹{summary['annual_medicines']}\n"
                    f"- Annual OPD Visits: ₹{summary['annual_opd_visits']}\n"
                    f"- Hospitalization (approx): ₹{summary['hospitalization']}\n"
                    f"- Estimated Annual Total: ₹{summary['estimated_annual_total']}\n"
                )
                parts.append(cost_text)
            else:
                parts.append("💰 COST ESTIMATES\nCould not calculate healthcare cost.")

        # If nothing detected, give a gentle message
        if not (wants_health or wants_hospital or wants_cost):
            return (
                "I could not understand what you need.\n\n"
                "You can ask things like:\n"
                "- 'What are symptoms of diabetes?'\n"
                "- 'Find hospitals in Delhi for heart treatment'\n"
                "- 'How much does diabetes treatment cost per year?'"
            )

        # Join all parts
        return "\n\n".join(parts)


# Quick manual test (for local run only)
if __name__ == "__main__":
    sup = SupervisorAgent()
    q1 = "I have diabetes, what are the symptoms and how much will treatment cost?"
    print("Query:", q1)
    print("=" * 80)
    print(sup.process(q1))
