def main():
    # ------------------- Step 1: Program Introduction and Initialization -------------------
    print("=" * 80)
    print("Ventilator-Associated Pneumonia (VAP) Risk Assessment Tool")
    print("Based on Evidence from 'Journal of Critical Care' 2008 Clinical Guidelines")
    print("=" * 80)
    print("This tool evaluates the risk of VAP in hospitalized patients receiving mechanical ventilation.")
    print("Eligibility: Patients aged ≥18 years currently on mechanical ventilation.")
    print("Instructions: Answer all questions with 'yes' or 'no' (case-insensitive). For numerical questions, enter digits as prompted.")
    print("=" * 80)

    # Main program loop (supports re-running for multiple patients)
    while True:
        # ------------------- Step 2: Collect Core Parameters (Layered Questions) -------------------
        # 2.1 Basic Parameter: Patient Age (Eligibility Screening)
        while True:
            age_input = input("\n1. What is the patient's age (in years)? ").strip()
            if age_input.isdigit():
                age = int(age_input)
                if age >= 18:
                    break
                else:
                    print("❌ This tool is only for patients aged ≥18. Please re-enter.")
            else:
                print("❌ Invalid input. Please enter age as a numeric value.")

        # 2.2 Core Parameter 1: Duration of Mechanical Ventilation (Key Risk Factor)
        while True:
            ventilation_input = input("2. Is the duration of mechanical ventilation ≥72 hours? (yes/no): ").strip().lower()
            if ventilation_input in ["yes", "no"]:
                ventilation_ge72 = ventilation_input == "yes"
                break
            else:
                print("❌ Invalid input. Please enter 'yes' or 'no'.")

        # 2.3 Core Parameter 2: Chest Imaging Result (Core Diagnostic Indicator)
        while True:
            imaging_input = input("3. Does chest imaging show new or persistent infiltrates? (yes/no): ").strip().lower()
            if imaging_input in ["yes", "no"]:
                chest_imaging = imaging_input == "yes"
                break
            else:
                print("❌ Invalid input. Please enter 'yes' or 'no'.")

        # ------------------- Step 3: Layered Decision-Making (Evidence-Based Logic) -------------------
        # First Layer: Chest Imaging (No infiltrates = Extremely Low VAP Risk)
        if not chest_imaging:
            risk_result = {
                "risk_level": "Low Risk",
                "case_control_ratio": "Cases (8, 3.2%); Controls (242, 96.8%)",
                "explanation": "No chest imaging infiltrates, which does not meet the core diagnostic criteria for VAP."
            }
        else:
            # Second Layer: Duration of Mechanical Ventilation (≥72h = High-Risk Threshold)
            if ventilation_ge72:
                # 3.1 Ventilation ≥72h: Further Inquiry About Key Symptoms (Fever + WBC Abnormality)
                while True:
                    fever_input = input("4. Does the patient have a fever (body temperature ≥38℃)? (yes/no): ").strip().lower()
                    if fever_input in ["yes", "no"]:
                        fever = fever_input == "yes"
                        break
                    else:
                        print("❌ Invalid input. Please enter 'yes' or 'no'.")

                while True:
                    wbc_input = input("5. Is the white blood cell (WBC) count abnormal (<4 or >12 ×10⁹/L)? (yes/no): ").strip().lower()
                    if wbc_input in ["yes", "no"]:
                        wbc_abnormal = wbc_input == "yes"
                        break
                    else:
                        print("❌ Invalid input. Please enter 'yes' or 'no'.")

                # Third Layer: Symptom Combination (VAP Diagnosis = Imaging + At Least 1 Symptom)
                if fever or wbc_abnormal:
                    risk_result = {
                        "risk_level": "High Risk",
                        "case_control_ratio": "Cases (156, 78.4%); Controls (43, 21.6%)",
                        "explanation": "Chest imaging infiltrates + mechanical ventilation ≥72h + fever/WBC abnormality, meeting VAP diagnostic criteria."
                    }
                else:
                    # Supplementary Inquiry: Oxygenation Index (Indirect Associated Indicator)
                    while True:
                        oxygen_input = input("6. Is the oxygenation index (PaO₂/FiO₂) ≤300? (yes/no): ").strip().lower()
                        if oxygen_input in ["yes", "no"]:
                            oxygen_abnormal = oxygen_input == "yes"
                            break
                        else:
                            print("❌ Invalid input. Please enter 'yes' or 'no'.")

                    if oxygen_abnormal:
                        risk_result = {
                            "risk_level": "Moderate-High Risk",
                            "case_control_ratio": "Cases (72, 54.2%); Controls (61, 45.8%)",
                            "explanation": "Chest imaging infiltrates + mechanical ventilation ≥72h + abnormal oxygenation, indicating high VAP risk."
                        }
                    else:
                        risk_result = {
                            "risk_level": "Moderate Risk",
                            "case_control_ratio": "Cases (35, 27.1%); Controls (94, 72.9%)",
                            "explanation": "Chest imaging infiltrates + mechanical ventilation ≥72h, but no other symptoms; close monitoring required."
                        }
            else:
                # 3.2 Ventilation <72h: Inquiry About Age + Comorbidities (Clinical Supplementary Logic)
                while True:
                    age_ge65_input = input("4. Is the patient aged ≥65 years? (yes/no): ").strip().lower()
                    if age_ge65_input in ["yes", "no"]:
                        age_ge65 = age_ge65_input == "yes"
                        break
                    else:
                        print("❌ Invalid input. Please enter 'yes' or 'no'.")

                while True:
                    complication_input = input("5. Does the patient have underlying comorbidities (e.g., diabetes, chronic lung disease)? (yes/no): ").strip().lower()
                    if complication_input in ["yes", "no"]:
                        has_complication = complication_input == "yes"
                        break
                    else:
                        print("❌ Invalid input. Please enter 'yes' or 'no'.")

                if age_ge65 or has_complication:
                    risk_result = {
                        "risk_level": "Moderate Risk",
                        "case_control_ratio": "Cases (48, 31.5%); Controls (104, 68.5%)",
                        "explanation": "Chest imaging infiltrates + elderly/comorbidities; even with ventilation <72h, VAP vigilance is needed."
                    }
                else:
                    risk_result = {
                        "risk_level": "Low-Moderate Risk",
                        "case_control_ratio": "Cases (22, 14.3%); Controls (132, 85.7%)",
                        "explanation": "Chest imaging infiltrates, but ventilation <72h + no elderly/comorbidities; low VAP risk."
                    }

        # ------------------- Step 4: Output Results (Aligned with Example Format) -------------------
        print("\n" + "=" * 80)
        print("VAP Risk Assessment Report")
        print("=" * 80)
        print(f"Patient Basic Information: Age {age} years | Ventilation ≥72h: {'Yes' if ventilation_ge72 else 'No'} | Chest Imaging Infiltrates: {'Yes' if chest_imaging else 'No'}")
        print(f"\n1. Risk Level: {risk_result['risk_level']}")
        print(f"2. Case/Control Risk Ratio: {risk_result['case_control_ratio']}")
        print(f"3. Assessment Rationale: {risk_result['explanation']}")
        print("\n4. Clinical Recommendations:")
        if risk_result["risk_level"] in ["High Risk", "Moderate-High Risk"]:
            print("   - Immediately initiate subglottic secretion drainage (for patients with ventilation ≥72h)")
            print("   - Maintain head-of-bed elevation at 45° (or as close as possible if contraindicated)")
            print("   - Use a closed endotracheal suctioning system; replace heat and moisture exchangers every 5-7 days")
            print("   - Daily monitoring of body temperature, WBC count, and chest imaging changes")
        elif risk_result["risk_level"] == "Moderate Risk":
            print("   - Closely monitor mechanical ventilation duration; prepare for subglottic drainage if ≥72h is expected")
            print("   - Recheck WBC count and oxygenation index every 2 days")
            print("   - Maintain head-of-bed elevation at 30-45°; avoid supine position")
        else:
            print("   - Routine mechanical ventilation care; replace heat and moisture exchangers weekly (if not contaminated)")
            print("   - Monitor WBC count and chest imaging once weekly")
            print("   - Immediately recheck relevant indicators if fever (≥38℃) occurs")
        print("=" * 80)

        # ------------------- Step 5: Re-run or Exit -------------------
        while True:
            restart_input = input("\nWould you like to assess another patient? (yes/no): ").strip().lower()
            if restart_input in ["yes", "no"]:
                if restart_input == "no":
                    print("\nThank you for using the VAP Risk Assessment Tool! Best regards for your work!")
                    return
                else:
                    print("\n" + "=" * 80)
                    print("Restarting for a new patient assessment...")
                    print("=" * 80)
                    break
            else:
                print("❌ Invalid input. Please enter 'yes' or 'no'.")

# Launch the program
if __name__ == "__main__":
    main()