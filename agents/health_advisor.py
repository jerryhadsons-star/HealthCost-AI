"""
Health Advisor Agent - Provides disease information and health tips
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict
import os


class HealthAdvisorAgent:
    def __init__(self, api_key: str = None):
        """
        Initialize Health Advisor Agent with Gemini LLM
        """
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.3,
        )

    def get_disease_info(self, disease_name: str) -> Dict:
        """
        Get detailed information about a disease
        """
        prompt = f"""
You are a medical information assistant.

Provide comprehensive information about the disease: {disease_name}

Answer in this structure:

1. Overview:
- 2–3 short sentences about what this disease is.

2. Common Symptoms:
- Bullet list of 5–7 common symptoms.

3. Risk Factors:
- Bullet list of important risk factors.

4. Prevention & Lifestyle Tips:
- 4–6 practical tips (diet, exercise, habits).

5. When to See a Doctor:
- Clear guidance when a patient should visit a doctor or emergency.

Keep the language simple and patient‑friendly.
Use Indian healthcare context where helpful.
Do NOT give medication names or prescriptions.
        """.strip()

        try:
            response = self.llm.invoke(prompt)
            return {
                "status": "success",
                "disease": disease_name,
                "information": response.content,
            }
        except Exception as e:
            return {
                "status": "error",
                "disease": disease_name,
                "error": str(e),
            }

    def get_health_tips(self, condition: str) -> Dict:
        """
        Provide simple daily health tips for a specific condition
        """
        prompt = f"""
You are a health coach.

Give 5 practical daily health tips for managing: {condition}

Each tip should be:
- Short title
- One line explanation

Cover:
- Diet
- Exercise
- Sleep
- Stress management
- Regular check‑ups

Do NOT mention medicines. Keep tone friendly and motivating.
        """.strip()

        try:
            response = self.llm.invoke(prompt)
            return {
                "status": "success",
                "condition": condition,
                "tips": response.content,
            }
        except Exception as e:
            return {
                "status": "error",
                "condition": condition,
                "error": str(e),
            }


# Quick manual test (optional, for local run only)
if __name__ == "__main__":
    agent = HealthAdvisorAgent()
    info = agent.get_disease_info("diabetes")
    print("=== Disease Info ===")
    print(info.get("information", ""))

    tips = agent.get_health_tips("hypertension")
    print("\n=== Health Tips ===")
    print(tips.get("tips", ""))
