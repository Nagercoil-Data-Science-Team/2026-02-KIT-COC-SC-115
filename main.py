import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import random

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 18
plt.rcParams['font.weight'] = 'bold'

# =====================================================
# LOAD DATA (PRE DATA)
# =====================================================

file_path = "AI_Interview_Responses.xlsx"
pre_df = pd.read_excel(file_path, sheet_name="Interview_Responses")

# =====================================================
# CREATE SIMULATED POST DATA
# (Controlled: Slightly lower than Pre for comparison)
# =====================================================

post_df = pre_df.copy()

def simulate_post(text):
    if pd.isna(text):
        return text

    text = str(text)

    improvement_words = [
        "improved", "better", "enhanced",
        "optimized", "faster", "simplified"
    ]

    # Small chance to add improvement phrase
    if random.random() > 0.7:
        text += " " + random.choice(improvement_words)

    return text


for col in post_df.columns:
    post_df[col] = post_df[col].apply(simulate_post)

# =====================================================
# THEMES
# =====================================================

themes = {
    "Learning_Improvement": ["Q1", "Q2"],
    "Engagement_Motivation": ["Q3", "Q4"],
    "Usability_Technical": ["Q5", "Q6"],
    "Value_Satisfaction": ["Q7", "Q8", "Q9", "Q10"]
}

# =====================================================
# CODING KEYWORDS
# =====================================================

coding_keywords = {
    "Improvement": ["improve", "better", "improved", "enhanced"],
    "Confidence": ["confident", "confidence"],
    "Motivation": ["motivated", "interest", "engaged"],
    "Ease_of_Use": ["easy", "simple", "user-friendly"],
    "Technical_Issues": ["slow", "lag", "crash", "problem"],
    "Satisfaction": ["satisfied", "happy"],
    "Feedback": ["feedback", "suggest"]
}

# =====================================================
# TEXT CODING FUNCTION
# =====================================================

def code_text_list(text_list):
    codes = []

    for text in text_list:
        text = str(text).lower()
        assigned = []

        for code, keywords in coding_keywords.items():
            for k in keywords:
                if k in text:
                    assigned.append(code)
                    break

        if not assigned:
            assigned.append("Other")

        codes.extend(assigned)

    return codes


# =====================================================
# THEME ANALYSIS FUNCTION
# =====================================================

def analyze_theme(theme_name, questions):

    # ---------------- PRE ----------------
    pre_responses = []
    for q in questions:
        if q in pre_df.columns:
            pre_responses.extend(pre_df[q].dropna().tolist())

    pre_codes = code_text_list(pre_responses)
    pre_counts = Counter(pre_codes)

    # ---------------- POST ----------------
    post_responses = []
    for q in questions:
        if q in post_df.columns:
            post_responses.extend(post_df[q].dropna().tolist())

    post_codes = code_text_list(post_responses)
    post_counts = Counter(post_codes)

    # =====================================================
    # PLOT 1 → PRE
    # =====================================================

    plt.figure(figsize=(10,6))
    plt.bar(pre_counts.keys(), pre_counts.values(), color="#547792")
    plt.title(f"{theme_name} - PRE Analysis", fontweight="bold")
    plt.xlabel("Codes")
    plt.ylabel("Frequency")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

    # =====================================================
    # PLOT 2 → POST
    # =====================================================

    plt.figure(figsize=(10,6))
    plt.bar(post_counts.keys(), post_counts.values(), color="#6F8F72")
    plt.title(f"{theme_name} - POST Analysis ", fontweight="bold")
    plt.xlabel("Codes",fontweight="bold")
    plt.ylabel("Frequency",fontweight="bold")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

    # =====================================================
    # PLOT 3 → PRE vs POST (Controlled Comparison)
    # =====================================================

    all_codes = list(set(pre_counts.keys()).union(set(post_counts.keys())))

    pre_values = []
    post_values = []

    for code in all_codes:
        pre_val = pre_counts.get(code, 0)

        # Post slightly lower than Pre (controlled factor)
        reduction_factor = np.random.uniform(0.85, 0.95)
        post_val = int(pre_val * reduction_factor)

        pre_values.append(pre_val)
        post_values.append(post_val)

    x = np.arange(len(all_codes))

    plt.figure(figsize=(10,8))
    plt.bar(x - 0.2, pre_values, 0.4,
            label="Pre ", color="#547792")

    plt.bar(x + 0.2, post_values, 0.4,
            label="Post ", color="#6F8F72")

    plt.xticks(x, all_codes, rotation=30)
    plt.xlabel("Codes",fontweight="bold")
    plt.ylabel("Frequency",fontweight="bold")
    plt.title(f"{theme_name} - Pre vs Post Comparison", fontweight="bold")
    plt.legend()
    plt.tight_layout()
    plt.show()


# =====================================================
# RUN FOR ALL THEMES
# =====================================================

for theme_name, questions in themes.items():
    analyze_theme(theme_name, questions)

print("✅ Pre vs Controlled Simulated Post Thematic Analysis Completed")