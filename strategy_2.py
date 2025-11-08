import matplotlib.pyplot as plt
from typing import List, Dict, Optional

def input_patient_data() -> Dict[str, any]:
    """
    Collects clinical parameters of a single patient from user input,
    returning a structured dictionary based on evidence from base_paper.pdf.
    """
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
    # Validate critical inputs to align with base_paper.pdf recommendations
    valid_routes = ["orotracheal", "nasotracheal"]
    valid_antiseptics = ["chlorhexidine", "povidone-iodine", "none"]
    valid_booleans = ["yes", "no"]
    
    if patient_data["intubation_route"] not in valid_routes:
        raise ValueError("Intubation route must be 'orotracheal' or 'nasotracheal' (per base_paper.pdf)")
    if patient_data["oral_antiseptic"] not in valid_antiseptics:
        raise ValueError("Oral antiseptic must be 'chlorhexidine', 'povidone-iodine', or 'none' (per base_paper.pdf)")
    if patient_data["subglottic_drainage"] not in valid_booleans:
        raise ValueError("Subglottic drainage input must be 'yes' or 'no'")
    
    return patient_data

def calculate_vap_risk(patient_data: Dict[str, any]) -> int:
    """
    Calculates VAP risk score using evidence-based rules extracted from base_paper.pdf.
    Risk factors add points; protective factors subtract points. Score ranges from 0 to 20.
    """
    risk_score = 0

    # 1. Intubation route (base_paper.pdf recommends orotracheal to reduce VAP risk)
    if patient_data["intubation_route"] == "nasotracheal":
        risk_score += 3  # Nasotracheal intubation increases VAP risk
    elif patient_data["intubation_route"] == "orotracheal":
        risk_score -= 2  # Orotracheal intubation is protective

    # 2. Duration of mechanical ventilation (base_paper.pdf highlights >72h as high risk)
    if patient_data["ventilation_duration_h"] > 72:
        risk_score += 3  # Significant risk increase for prolonged ventilation
    elif 24 <= patient_data["ventilation_duration_h"] <= 72:
        risk_score += 1  # Moderate risk increase

    # 3. Subglottic secretion drainage (base_paper.pdf recommends for >72h ventilation)
    if patient_data["ventilation_duration_h"] > 72:
        if patient_data["subglottic_drainage"] == "yes":
            risk_score -= 2  # Protective when indicated
        else:
            risk_score += 2  # Risk increase if not used when needed

    # 4. Bed head elevation (base_paper.pdf recommends 45° to prevent VAP)
    if patient_data["bed_head_elevation_deg"] >= 45:
        risk_score -= 2  # Protective at recommended angle
    elif patient_data["bed_head_elevation_deg"] < 30:
        risk_score += 2  # High risk at low elevation

    # 5. Closed suction system (base_paper.pdf recommends closed systems for safety)
    if patient_data["closed_suction_system"] == "yes":
        risk_score -= 1  # Slight protective effect
    else:
        risk_score += 1  # Slight risk increase with open systems

    # 6. Oral antiseptics (base_paper.pdf suggests chlorhexidine/povidone-iodine for risk reduction)
    if patient_data["oral_antiseptic"] in ["chlorhexidine", "povidone-iodine"]:
        risk_score -= 1  # Protective effect of antiseptics

    # 7. Clinical signs of infection (consistent with VAP definition in base_paper.pdf)
    if patient_data["fever"] == "yes":
        risk_score += 2  # Fever is a key VAP indicator
    if patient_data["leukocytosis"] == "yes":
        risk_score += 2  # Leukocytosis is associated with VAP
    if patient_data["chest_radiograph"] == "yes":
        risk_score += 3  # New radiologic infiltrates are critical for VAP diagnosis

    # Constrain score to 0-20 range for practicality
    return max(0, min(risk_score, 20))

def determine_risk_level(risk_score: int) -> Dict[str, str]:
    """
    Maps risk score to risk level (Low/Medium/High) and provides evidence-based
    clinical recommendations from base_paper.pdf.
    """
    if risk_score < 5:
        return {
            "risk_level": "Low Risk",
            "recommendation": "Maintain standard VAP prevention measures (per base_paper.pdf): use orotracheal intubation if possible, keep bed head elevated ≥45°, and perform regular ventilator circuit checks (change only if soiled/damaged)."
        }
    elif 5 <= risk_score <= 12:
        return {
            "risk_level": "Medium Risk",
            "recommendation": "Intensify prevention (per base_paper.pdf): implement oral antiseptic rinses (chlorhexidine/povidone-iodine), ensure closed suction system use, and monitor for signs of sinusitis. Continue bed head elevation ≥45°."
        }
    else:
        return {
            "risk_level": "High Risk",
            "recommendation": "Urgent intervention (per base_paper.pdf): initiate subglottic secretion drainage (if ventilation >72h), optimize bed head elevation to 45°, use rotating beds if feasible, and closely monitor infection markers (fever, leukocytosis, chest radiographs). Avoid bacterial filters (not recommended in base_paper.pdf)."
        }

def generate_risk_report(patient_data: Dict[str, any], risk_score: int, risk_assessment: Dict[str, str]) -> None:
    """
    Generates a formatted VAP risk assessment report and visualizes the score.
    """
    # Print text report
    print("=" * 60)
    print("VENTILATOR-ASSOCIATED PNEUMONIA (VAP) RISK ASSESSMENT REPORT")
    print(f"Based on Evidence from: base_paper.pdf")
    print("=" * 60)
    print(f"Patient Age: {patient_data['age']} years")
    print(f"Intubation Route: {patient_data['intubation_route'].capitalize()}")
    print(f"Mechanical Ventilation Duration: {patient_data['ventilation_duration_h']} hours")
    print(f"Risk Score: {risk_score}/20")
    print(f"Risk Level: {risk_assessment['risk_level']}")
    print("\nClinical Recommendations:")
    print(f"- {risk_assessment['recommendation']}")
    print("=" * 60)

    # Visualize risk score
    plt.figure(figsize=(10, 4))
    # Create background bars for risk ranges
    bars = plt.bar(
        ["Low Risk (0-4)", "Medium Risk (5-12)", "High Risk (13-20)"],
        [4, 12, 20],
        color=["#2ecc71", "#f39c12", "#e74c3c"],
        alpha=0.3
    )
    # Plot patient's score as a marker
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
    # Customize plot
    plt.title("VAP Risk Score Distribution (Reference: base_paper.pdf)", fontsize=12)
    plt.ylabel("Risk Score", fontsize=10)
    plt.ylim(0, 22)
    plt.grid(axis="y", alpha=0.2)
    plt.legend()
    plt.tight_layout()
    plt.show()

def batch_process_patients(batch_data: List[Dict[str, any]]) -> List[Dict[str, any]]:
    """
    Processes a batch of patients, returning risk assessments for each.
    Designed for potential integration with EHR systems (per project goals).
    """
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
    """
    Main function to run the VAP risk prediction tool.
    Supports single-patient assessment or batch processing.
    """
    print("VENTILATOR-ASSOCIATED PNEUMONIA (VAP) RISK PREDICTOR")
    print("Source of Evidence: base_paper.pdf\n")
    
    mode = input("Select mode (single/batch): ").strip().lower()
    if mode == "single":
        try:
            patient_data = input_patient_data()
            risk_score = calculate_vap_risk(patient_data)
            risk_assessment = determine_risk_level(risk_score)
            generate_risk_report(patient_data, risk_score, risk_assessment)
        except ValueError as e:
            print(f"Error: {e}")
    elif mode == "batch":
        # Example batch data (can be replaced with EHR-derived data)
        sample_batch = [
            {
                "age": 68,
                "intubation_route": "nasotracheal",
                "ventilation_duration_h": 96,
                "subglottic_drainage": "no",
                "bed_head_elevation_deg": 25,
                "closed_suction_system": "no",
                "oral_antiseptic": "none",
                "fever": "yes",
                "leukocytosis": "yes",
                "chest_radiograph": "yes"
            },
            {
                "age": 52,
                "intubation_route": "orotracheal",
                "ventilation_duration_h": 48,
                "subglottic_drainage": "no",
                "bed_head_elevation_deg": 45,
                "closed_suction_system": "yes",
                "oral_antiseptic": "chlorhexidine",
                "fever": "no",
                "leukocytosis": "no",
                "chest_radiograph": "no"
            }
        ]
        print("\nProcessing batch of 2 sample patients...")
        batch_results = batch_process_patients(sample_batch)
        # Print batch results
        print("\nBatch Processing Results:")
        print("-" * 80)
        for result in batch_results:
            if "error" in result:
                print(f"Patient {result['patient_id']}: {result['error']}")
            else:
                print(f"Patient {result['patient_id']}:")
                print(f"  Age: {result['age']} | Ventilation Duration: {result['ventilation_duration_h']}h")
                print(f"  Risk Score: {result['risk_score']} | Risk Level: {result['risk_level']}")
                print(f"  Recommendation: {result['recommendation'][:100]}...")
                print("-" * 80)
    else:
        print("Invalid mode. Please select 'single' or 'batch'.")

if __name__ == "__main__":
    main()