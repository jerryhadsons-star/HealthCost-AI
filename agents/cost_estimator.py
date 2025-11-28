"""
Cost Estimator Agent - Calculates healthcare expenses
"""
from typing import Dict


class CostEstimatorAgent:
    def __init__(self):
        """
        Initialize Cost Estimator with healthcare cost data (in INR)
        """

        # Approx room + OPD costs (India, rough ranges)
        self.room_costs = {
            "district": {"per_day": 350, "opd": 94},
            "tertiary": {"per_day": 600, "opd": 304},
            "private": {"per_day": 6000, "opd": 1251},
            "metro_private": {"per_day": 8000, "opd": 1500},
        }

        # Monthly medicine costs (approx) for chronic diseases
        self.medicine_costs = {
            "diabetes": {
                "insulin": 1500,
                "metformin": 200,
                "test_strips": 800,
                "monthly_total": 2500,
            },
            "hypertension": {
                "ace_inhibitor": 300,
                "beta_blocker": 250,
                "monthly_total": 550,
            },
            "asthma": {
                "inhaler": 600,
                "preventive": 400,
                "monthly_total": 1000,
            },
            "heart disease": {
                "statins": 500,
                "aspirin": 50,
                "beta_blocker": 300,
                "monthly_total": 850,
            },
        }

    def calculate_hospitalization_cost(
        self, hospital_type: str, days: int, procedure_cost: int = 0
    ) -> Dict:
        """
        Calculate total hospitalization cost for a given hospital type and stay duration.
        """

        cost_per_day = self.room_costs.get(hospital_type, {}).get("per_day", 1000)
        room_total = cost_per_day * max(days, 1)

        # Typical cost distribution (approx % of base room cost)
        medicines = room_total * 0.24  # 24%
        tests = room_total * 0.10  # 10%
        doctor_fees = room_total * 0.17  # 17%
        other = room_total * 0.39  # 39%

        total = room_total + medicines + tests + doctor_fees + other + procedure_cost

        return {
            "status": "success",
            "hospital_type": hospital_type,
            "days_admitted": days,
            "breakdown": {
                "room_charges": round(room_total, 2),
                "medicines": round(medicines, 2),
                "tests_diagnostics": round(tests, 2),
                "doctor_fees": round(doctor_fees, 2),
                "other_expenses": round(other, 2),
                "procedure_cost": procedure_cost,
            },
            "total_cost": round(total, 2),
            "average_per_day": round(total / max(days, 1), 2),
        }

    def calculate_annual_medicine_cost(self, disease: str) -> Dict:
        """
        Calculate annual medicine costs for chronic diseases.
        """
        key = disease.lower()
        monthly_meds = self.medicine_costs.get(key)

        if not monthly_meds:
            return {
                "status": "not_found",
                "error": f"Disease '{disease}' not found in medicine database.",
                "available_diseases": list(self.medicine_costs.keys()),
            }

        monthly_total = monthly_meds.get(
            "monthly_total",
            sum(v for k, v in monthly_meds.items() if k != "monthly_total"),
        )
        annual_total = monthly_total * 12

        breakdown = {k: v for k, v in monthly_meds.items() if k != "monthly_total"}

        return {
            "status": "success",
            "disease": disease,
            "medicine_breakdown": breakdown,
            "monthly_total": round(monthly_total, 2),
            "annual_total": round(annual_total, 2),
            "average_per_month": round(monthly_total, 2),
        }

    def estimate_total_healthcare_cost(
        self,
        disease: str,
        hospital_type: str = "private",
        hospital_days: int = 0,
        opd_visits_per_year: int = 12,
    ) -> Dict:
        """
        Estimate total annual healthcare cost:
        - Hospitalization (optional)
        - Medicines
        - OPD visits
        """

        # Hospitalization cost
        hosp_cost = 0
        hosp_details = {}
        if hospital_days > 0:
            hosp_result = self.calculate_hospitalization_cost(
                hospital_type=hospital_type,
                days=hospital_days,
            )
            hosp_cost = hosp_result["total_cost"]
            hosp_details = hosp_result

        # Medicine cost
        med_result = self.calculate_annual_medicine_cost(disease)
        annual_med_cost = (
            med_result.get("annual_total", 0) if med_result["status"] == "success" else 0
        )

        # OPD visits
        opd_per_visit = self.room_costs.get(hospital_type, {}).get("opd", 300)
        annual_opd_cost = opd_per_visit * opd_visits_per_year

        total = hosp_cost + annual_med_cost + annual_opd_cost

        return {
            "status": "success",
            "disease": disease,
            "summary": {
                "hospitalization": round(hosp_cost, 2),
                "annual_medicines": round(annual_med_cost, 2),
                "annual_opd_visits": round(annual_opd_cost, 2),
                "estimated_annual_total": round(total, 2),
            },
            "details": {
                "hospitalization_details": hosp_details,
                "medicine_details": med_result,
                "opd_cost_per_visit": opd_per_visit,
                "opd_visits_per_year": opd_visits_per_year,
            },
        }


# Quick manual test (for local run only)
if __name__ == "__main__":
    estimator = CostEstimatorAgent()

    hosp = estimator.calculate_hospitalization_cost("private", 3)
    print("=== Hospitalization ===")
    print(hosp)

    meds = estimator.calculate_annual_medicine_cost("diabetes")
    print("\n=== Medicines ===")
    print(meds)

    total = estimator.estimate_total_healthcare_cost(
        disease="diabetes",
        hospital_type="private",
        hospital_days=3,
        opd_visits_per_year=12,
    )
    print("\n=== Total Healthcare Cost ===")
    print(total)
