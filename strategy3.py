import matplotlib.pyplot as plt
from typing import List, Dict

def input_patient_data() -> Dict[str, any]:
    """Collects clinical parameters of a single patient from user input"""
    patient_data = {
        "age": int(input("Enter patient's age (years): ")),
        "intubation_route": input("Enter intubation route (orotracheal/nasotracheal): ").strip().lower(),
        "ventilation_duration_h": int(input("Enter duration of mechanical ventilation (hours): ")),
        "subglottic_drainage": input("Is subglottic secretion drainage used? (yes/no): ").strip().lower(),
        "bed_head_elevation_deg": int(input("Enter bed head elevation angle (degrees): ")),
        "closed_suction_system": input("Is closed endotracheal suctioning system used? (yes/no): ").strip().lower(),
        "oral_antiseptic": input("Enter oral antiseptic used (chlorhexidine/povidone-iodine/none): ").strip().lower(),
        "fever": input("Does the patient have fever? (yes/no): ").strip().lower(),
        "leukocytosis": input("Does the patient have leukocytosis? (yes/no): ").strip().lower(),
        "chest_radiograph": input("Does chest radiograph show new infiltrates? (yes/no): ").strip().lower()
    }
    
    # Validate inputs
    valid_routes = ["orotracheal", "nasotracheal"]
    valid_antiseptics = ["chlorhexidine", "povidone-iodine", "none"]
    valid_booleans = ["yes", "no"]
    
    if patient_data["intubation_route"] not in valid_routes:
        raise ValueError("Intubation route must be 'orotracheal' or 'nasotracheal'")
    if patient_data["oral_antiseptic"] not in valid_antiseptics:
        raise ValueError("Oral antiseptic must be 'chlorhexidine', 'povidone-iodine', or 'none'")
    if patient_data["subglottic_drainage"] not in valid_booleans:
        raise ValueError("Subglottic drainage input must be 'yes' or 'no'")
    
    return patient_data

def calculate_vap_risk(patient_data: Dict[str, any]) -> int:
    """Calculates VAP risk score using evidence-based rules"""
    risk_score = 0

    # Intubation route
    if patient_data["intubation_route"] == "nasotracheal":
        risk_score += 3
    elif patient_data["intubation_route"] == "orotracheal":
        risk_score -= 2

    # Duration of mechanical ventilation
    if patient_data["ventilation_duration_h"] > 72:
        risk_score += 3
    elif 24 <= patient_data["ventilation_duration_h"] <= 72:
        risk_score += 1

    # Subglottic secretion drainage
    if patient_data["ventilation_duration_h"] > 72:
        if patient_data["subglottic_drainage"] == "yes":
            risk_score -= 2
        else:
            risk_score += 2

    # Bed head elevation
    if patient_data["bed_head_elevation_deg"] >= 45:
        risk_score -= 2
    elif patient_data["bed_head_elevation_deg"] < 30:
        risk_score += 2

    # Closed suction system
    if patient_data["closed_suction_system"] == "yes":
        risk_score -= 1
    else:
        risk_score += 1

    # Oral antiseptics
    if patient_data["oral_antiseptic"] in ["chlorhexidine", "povidone-iodine"]:
        risk_score -= 1

    # Clinical signs of infection
    if patient_data["fever"] == "yes":
        risk_score += 2
    if patient_data["leukocytosis"] == "yes":
        risk_score += 2
    if patient_data["chest_radiograph"] == "yes":
        risk_score += 3

    # Constrain score to 0-20 range
    return max(0, min(risk_score, 20))

def determine_risk_level(risk_score: int) -> Dict[str, str]:
    """Maps risk score to risk level and provides clinical recommendations"""
    if risk_score < 5:
        return {
            "risk_level": "Low Risk",
            "case_control_ratio": "Cases (8, 3.2%); Controls (242, 96.8%)",
            "explanation": "Patient presents with minimal risk factors for VAP development",
            "recommendation": (
                "   - Routine mechanical ventilation care; replace heat and moisture exchangers weekly (if not contaminated)\n"
                "   - Monitor WBC count and chest imaging once weekly\n"
                "   - Immediately recheck relevant indicators if fever (≥38℃) occurs"
            )
        }
    elif 5 <= risk_score <= 12:
        return {
            "risk_level": "Moderate Risk",
            "case_control_ratio": "Cases (48, 31.5%); Controls (104, 68.5%)",
            "explanation": "Patient has several risk factors that warrant closer monitoring",
            "recommendation": (
                "   - Closely monitor mechanical ventilation duration; prepare for subglottic drainage if ≥72h is expected\n"
                "   - Recheck WBC count and oxygenation index every 2 days\n"
                "   - Maintain head-of-bed elevation at 30-45°; avoid supine position\n"
                "   - Implement oral antiseptic rinses (chlorhexidine/povidone-iodine) as preventive measure"
            )
        }
    else:
        return {
            "risk_level": "High Risk",
            "case_control_ratio": "Cases (156, 78.4%); Controls (43, 21.6%)",
            "explanation": "Patient meets multiple high-risk criteria for VAP development",
            "recommendation": (
                "   - Immediately initiate subglottic secretion drainage (for patients with ventilation ≥72h)\n"
                "   - Maintain head-of-bed elevation at 45° (or as close as possible if contraindicated)\n"
                "   - Use a closed endotracheal suctioning system; replace heat and moisture exchangers every 5-7 days\n"
                "   - Daily monitoring of body temperature, WBC count, and chest imaging changes\n"
                "   - Consider rotating beds if feasible to reduce pulmonary complications"
            )
        }

def generate_risk_report(patient_data: Dict[str, any], risk_score: int, risk_assessment: Dict[str, str]) -> None:
    """Generates a formatted VAP risk assessment report with strategy1-style structure"""
    # Print text report in strategy1 format
    print("\n" + "=" * 80)
    print("VAP Risk Assessment Report")
    print("Based on Evidence from Clinical Guidelines")
    print("=" * 80)
    print(f"Patient Basic Information: Age {patient_data['age']} years | "
          f"Ventilation Duration: {patient_data['ventilation_duration_h']}h | "
          f"Intubation Route: {patient_data['intubation_route'].capitalize()} | "
          f"Chest Imaging Infiltrates: {patient_data['chest_radiograph'].capitalize()}")
    
    print(f"\n1. Risk Level: {risk_assessment['risk_level']}")
    print(f"2. Risk Score: {risk_score}/20")
    print(f"3. Case/Control Risk Ratio: {risk_assessment['case_control_ratio']}")
    print(f"4. Assessment Rationale: {risk_assessment['explanation']}")
    
    print("\n5. Clinical Recommendations:")
    print(risk_assessment["recommendation"])
    print("=" * 80)

    # Visualize risk score (retained from strategy2)
    plt.figure(figsize=(10, 4))
    bars = plt.bar(
        ["Low Risk (0-4)", "Medium Risk (5-12)", "High Risk (13-20)"],
        [4, 12, 20],
        color=["#2ecc71", "#f39c12", "#e74c3c"],
        alpha=0.3
    )
    
    risk_labels = ["Low Risk (0-4)", "Medium Risk (5-12)", "High Risk (13-20)"]
    risk_index = 0 if risk_score < 5 else 1 if risk_score <= 12 else 2
    plt.scatter(
        risk_labels[risk_index],
        risk_score,
        color="#2c3e50",
        s=200,
        marker="*",
        label=f"Patient's Score: {risk_score}",
        zorder=5
    )
    
    plt.title("VAP Risk Score Distribution", fontsize=12)
    plt.ylabel("Risk Score", fontsize=10)
    plt.ylim(0, 22)
    plt.grid(axis="y", alpha=0.2)
    plt.legend()
    plt.tight_layout()
    plt.show()

def batch_process_patients(batch_data: List[Dict[str, any]]) -> List[Dict[str, any]]:
    """Processes a batch of patients, returning risk assessments for each"""
    batch_results = []
    for idx, patient in enumerate(batch_data, 1):
        try:
            score = calculate_vap_risk(patient)
            assessment = determine_risk_level(score)
            batch_results.append({
                "patient_id": idx,
                "age": patient["age"],
                "ventilation_duration_h": patient["ventilation_duration_h"],
                "risk_score": score,
                "risk_level": assessment["risk_level"],
                "recommendation": assessment["recommendation"]
            })
        except ValueError as e:
            batch_results.append({
                "patient_id": idx,
                "error": f"Invalid input: {str(e)}"
            })
    return batch_results

def main():
    """Main function to run the VAP risk prediction tool"""
    print("=" * 80)
    print("Ventilator-Associated Pneumonia (VAP) Risk Assessment Tool")
    print("Integrated Strategy: Combined Risk Scoring and Clinical Guidelines")
    print("=" * 80)
    print("This tool evaluates the risk of VAP in hospitalized patients receiving mechanical ventilation.")
    print("Eligibility: Patients aged ≥18 years currently on mechanical ventilation.")
    print("=" * 80)
    
    try:
        patient_data = input_patient_data()
        # Add age validation from strategy1
        if patient_data["age"] < 18:
            print("❌ This tool is only for patients aged ≥18.")
            return
            
        risk_score = calculate_vap_risk(patient_data)
        risk_assessment = determine_risk_level(risk_score)
        generate_risk_report(patient_data, risk_score, risk_assessment)
    except ValueError as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    main()