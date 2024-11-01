# examples/example_risk_assessment.py

from src.risk_assessment import RiskAssessment, InvalidDataError

def main():
    # Create an instance of RiskAssessment
    risk_assessment = RiskAssessment()

    # Example: Assessing Risk
    try:
        risk_data = {
            "credit_score": 650,
            "income": 50000,
            "debt": 15000,
            "employment_status": "employed"
        }
        risk_score = risk_assessment.assess_risk(risk_data)
        print(f"Risk Score: {risk_score}")

        # Example: Categorizing Risk
        risk_category = risk_assessment.categorize_risk(risk_score)
        print(f"Risk Category: {risk_category}")

    except InvalidDataError as e:
        print(f"Risk assessment failed: {e}")

if __name__ == "__main__":
    main()
