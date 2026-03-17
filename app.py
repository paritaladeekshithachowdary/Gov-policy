import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="GovPolicy AI Agent", page_icon="🏛️", layout="wide")

# --- CUSTOM CSS FOR BETTER UI ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    .policy-card { padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; background-color: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- POLICY KNOWLEDGE BASE ---
# In a real app, this could be a CSV or a Database
POLICIES = [
    {
        "name": "Pragati Scholarship Scheme",
        "min_age": 17, "max_age": 25, "gender": "Female", "max_income": 800000, 
        "category": "Student", "desc": "₹50,000 per annum for girls pursuing technical degrees."
    },
    {
        "name": "Post-Matric Scholarship for Minorities",
        "min_age": 15, "max_age": 30, "gender": "All", "max_income": 200000, 
        "category": "Student", "desc": "Financial assistance for higher education for economically weaker sections."
    },
    {
        "name": "PM Ujjwala Yojana",
        "min_age": 18, "max_age": 100, "gender": "Female", "max_income": 150000, 
        "category": "General Public", "desc": "Provides free LPG connections to women from BPL households."
    },
    {
        "name": "Mudra Loan (Shishu)",
        "min_age": 18, "max_age": 65, "gender": "All", "max_income": 9999999, 
        "category": "Business Owner", "desc": "Loans up to ₹50,000 for starting a small business without collateral."
    },
    {
        "name": "Atal Pension Yojana",
        "min_age": 18, "max_age": 40, "gender": "All", "max_income": 9999999, 
        "category": "General Public", "desc": "Guaranteed monthly pension after age 60 for unorganized sector workers."
    },
    {
        "name": "Lakhpati Didi Scheme",
        "min_age": 18, "max_age": 60, "gender": "Female", "max_income": 300000, 
        "category": "Farmer", "desc": "Empowers women in Self Help Groups to earn at least ₹1 Lakh per year through skill training."
    }
]

# --- APP HEADER ---
st.title("🏛️ Government Policy AI Agent")
st.write("Enter your details below, and my AI logic will find the best government schemes for you.")

# --- SIDEBAR: USER INFO ---
with st.sidebar:
    st.header("👤 Your Profile")
    age = st.number_input("Age", min_value=1, max_value=100, value=20)
    gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    income = st.number_input("Annual Income (in ₹)", min_value=0, value=0, step=10000)
    location = st.selectbox("Location Type", ["Urban", "Rural"])
    user_type = st.selectbox("Professional Status", ["Student", "Farmer", "IT Professional", "Business Owner", "General Public"])
    
    find_button = st.button("Find Best Policies")

# --- AI AGENT LOGIC ---
def get_recommendations(age, gender, income, user_type):
    matches = []
    for p in POLICIES:
        # Checking age eligibility
        if not (p["min_age"] <= age <= p["max_age"]):
            continue
        # Checking gender eligibility
        if p["gender"] != "All" and p["gender"] != gender:
            continue
        # Checking income eligibility
        if income > p["max_income"]:
            continue
        # Checking category (prioritize student if they are a student)
        score = 0
        if p["category"] == user_type:
            score += 2
        
        matches.append({"name": p["name"], "desc": p["desc"], "score": score})
    
    # Sort by relevance
    return sorted(matches, key=lambda x: x['score'], reverse=True)

# --- MAIN DISPLAY ---
if find_button:
    st.subheader(f"Results for {age}yo {gender} {user_type}")
    results = get_recommendations(age, gender, income, user_type)
    
    if not results:
        st.warning("No specific matches found for your criteria. Try adjusting your income or status.")
    else:
        st.success(f"Found {len(results)} matching policies!")
        for res in results:
            st.markdown(f"""
                <div class="policy-card">
                    <h3>✅ {res['name']}</h3>
                    <p>{res['desc']}</p>
                    <small>Relevance Score: {"High" if res['score'] > 0 else "Medium"}</small>
                </div>
            """, unsafe_allow_html=True)
else:
    # Welcome Screen / Instructions
    st.info("Please fill in your details on the left sidebar and click 'Find Best Policies'.")
    st.image("https://www.myscheme.gov.in/_next/image?url=%2Fimages%2Fhome%2Fhero-banner.png&w=1920&q=75", caption="Empowering Citizens through Technology")

# --- FOOTER ---
st.divider()
st.caption("Note: This AI agent uses a curated 2026 database. Always check the official 'myScheme' portal for final verification.")
