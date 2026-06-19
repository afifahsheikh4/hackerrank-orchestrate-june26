import pandas as pd

claims_file = "dataset/claims.csv"
history_file = "dataset/user_history.csv"
output_file = "dataset/output.csv"

claims_df = pd.read_csv(claims_file)
history_df = pd.read_csv(history_file)


def get_image_count(image_paths):
    if pd.isna(image_paths):
        return 0
    return len(str(image_paths).split(";"))


def get_user_risk(user_id):
    user = history_df[history_df["user_id"] == user_id]

    if user.empty:
        return "low"

    claim_count = user["past_claim_count"].values[0]

    if claim_count > 5:
        return "high"
    elif claim_count > 2:
        return "medium"

    return "low"


def evaluate_evidence(image_count):
    if image_count == 0:
        return False, "No images provided"
    if image_count == 1:
        return False, "Single image may be insufficient for reliable verification"
    return True, "Multiple images improve reliability"


def detect_issue_type(text):
    text = str(text).lower()

    if "dent" in text:
        return "dent"
    if "crack" in text:
        return "crack"
    if "broken" in text:
        return "broken"
    if "scratch" in text:
        return "scratch"
    if "damage" in text:
        return "damage"
    if "missing" in text:
        return "missing"
    if "stain" in text or "water" in text:
        return "liquid_damage"

    return "unknown"


def detect_object_part(text):
    text = str(text).lower()

    if "screen" in text:
        return "screen"
    if "keyboard" in text:
        return "keyboard"
    if "hinge" in text:
        return "hinge"
    if "trackpad" in text:
        return "trackpad"

    if "bumper" in text:
        return "bumper"
    if "door" in text:
        return "door"
    if "headlight" in text or "taillight" in text:
        return "light"
    if "mirror" in text:
        return "mirror"

    if "package" in text or "box" in text:
        return "package"
    if "corner" in text:
        return "corner"

    return "unknown"


def decide_claim_status(text, image_count):
    text = str(text).lower()

    if image_count == 0:
        return "not_enough_information"

    if any(word in text for word in ["not damaged", "no issue", "working fine"]):
        return "contradicted"

    if any(word in text for word in ["broken", "crack", "damage", "scratch", "dent"]):
        return "supported"

    return "not_enough_information"


def is_malicious(text):
    text = str(text).lower()
    return "ignore all previous instructions" in text or "approve immediately" in text


def calculate_severity(text):
    text = str(text).lower()

    if "missing" in text:
        return "high"
    if "completely broken" in text or "severe damage" in text:
        return "high"
    if "dent" in text or "large crack" in text:
        return "medium"
    if "small scratch" in text:
        return "low"
    
    return "unknown"


def main():
    print("🔥 Claim verification started...")

    results = []

    for _, row in claims_df.iterrows():
        user_id = row["user_id"]
        image_paths = row["image_paths"]
        claim_text = row["user_claim"]

        image_count = get_image_count(image_paths)

        evidence_standard_met, evidence_reason = evaluate_evidence(image_count)

        risk = get_user_risk(user_id)
        risk_flags = risk if risk != "low" else "none"

        issue_type = detect_issue_type(claim_text)
        object_part = detect_object_part(claim_text)

        claim_status = decide_claim_status(claim_text, image_count)

        # safety
        if is_malicious(claim_text):
            claim_status = "not_enough_information"

        if not evidence_standard_met:
          claim_status = "not_enough_information"    

        if issue_type == "unknown":
          claim_status = "not_enough_information"  

        if "no damage" in claim_text:
           claim_status = "contradicted"

         
        justification = f"Detected '{issue_type}' on '{object_part}' with {image_count} image(s), result: {claim_status}"

        supporting_ids = image_paths if claim_status == "supported" else "none"

        valid_image = image_count > 0

        severity = calculate_severity(claim_text)

        results.append({
            "evidence_standard_met": evidence_standard_met,
            "evidence_standard_met_reason": evidence_reason,
            "risk_flags": risk_flags,
            "issue_type": issue_type,
            "object_part": object_part,
            "claim_status": claim_status,
            "claim_status_justification": justification,
            "supporting_image_ids": supporting_ids,
            "valid_image": valid_image,
            "severity": severity
        })

    pd.DataFrame(results).to_csv(output_file, index=False)

    print("✅ Output saved to dataset/output.csv")


if __name__ == "__main__":
    main()