import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="GovPolicy AI Agent", page_icon="🏛️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .policy-card { 
        padding: 25px; border-radius: 12px; background-color: white; 
        border-left: 8px solid #007bff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
        margin-bottom: 20px; 
    }
    .tag { padding: 4px 12px; border-radius: 50px; font-size: 11px; font-weight: bold; margin-right: 5px; }
    .tag-scholarship { background-color: #e3f2fd; color: #1976d2; }
    .tag-farmer { background-color: #e8f5e9; color: #2e7d32; }
    .tag-it { background-color: #f3e5f5; color: #7b1fa2; }
    .tag-general { background-color: #fff3e0; color: #e65100; }
    .apply-btn {
        display: inline-block; margin-top: 15px; padding: 10px 20px;
        background-color: #28a745; color: white !important;
        text-decoration: none; border-radius: 5px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- THE 2026 POLICY DATABASE ---
POLICIES = [
    # --- STUDENT SCHOLARSHIPS ---
    {
        "name": "Pragati Scholarship for Girls",
        "category": "Student", "type": "Scholarship",
        "min_age": 16, "max_age": 25, "gender": "Female", "max_income": 800000, 
        "desc": "₹50,000 per annum for technical education.",
        "url": "https://www.myscheme.gov.in/schemes/psgs-deg"
    },
    {
        "name": "Post-Matric Scholarship (NSP)",
        "category": "Student", "type": "Scholarship",
        "min_age": 15, "max_age": 30, "gender": "All", "max_income": 250000, 
        "desc": "Financial support for higher education via National Scholarship Portal.",
        "url": "https://scholarships.gov.in/"
    },
    # --- FARMER SCHEMES ---
    {
        "name": "PM-Kisan Samman Nidhi",
        "category": "Farmer", "type": "Direct Benefit",
        "min_age": 18, "max_age": 100, "gender": "All", "max_income": 9999999, 
        "desc": "Direct income support of ₹6,000 per year in three 2,000 installments.",
        "url": "https://pmkisan.gov.in/"
    },
    {
        "name": "Kisan Credit Card (KCC)",
        "category": "Farmer", "type": "Loan/Credit",
        "min_age": 18, "max_age": 75, "gender": "All", "max_income": 9999999, 
        "desc": "Institutional credit at 4% effective interest for agricultural inputs.",
        "url": "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2238004"
    },
    # --- IT PROFESSIONAL SCHEMES ---
    {
        "name": "Skill India Digital (AI & Tech Courses)",
        "category": "IT Professional", "type": "Upskilling",
        "min_age": 18, "max_age": 60, "gender": "All", "max_income": 9999999, 
        "desc": "Free government-certified courses in AI, Cloud, and Cybersecurity.",
        "url": "https://www.skillindiadigital.gov.in/"
    },
    {
        "name": "India Semiconductor Mission (ISM) Incentives",
        "category": "IT Professional", "type": "Industry Benefit",
        "min_age": 21, "max_age": 60, "gender": "All", "max_income": 9999999, 
        "desc": "Specialized training and R&D grants for chip design and hardware professionals.",
        "url": "https://www.ism.gov.in/"
    },
    # --- GENERAL PUBLIC ---
    {
        "name": "Atal Pension Yojana (APY)",
        "category": "General Public", "type": "Pension",
        "min_age": 18, "max_age": 40, "gender": "All", "max_income": 9999999, 
        "desc": "Guaranteed monthly pension for unorganized sector workers.",
        "url": "https://www.npscra.nsdl.co.in/"
    }
]

# --- UI SETUP ---
st.title("🏛️ Intelligent Govt Policy Agent")

with st.sidebar:
    st.header("👤 Personal Profile")
    status = st.selectbox("Current Status", ["Student", "Farmer", "IT Professional", "Business Owner", "General Public"])
    age = st.number_input("Age", 1, 100, 20)
    gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    income = st.number_input("Annual Income (₹)", 0, 10000000, 0)
    find_btn = st.button("Find Best Policies")

# --- NON-HALLUCINATING LOGIC ---
def get_verified_recommendations(u_status, u_age, u_gender, u_income):
    matches = []
    for p in POLICIES:
        # STRICT FILTER 1: If user is Professional/Farmer, DO NOT show Scholarships
        if u_status in ["IT Professional", "Farmer", "Business Owner"] and p["type"] == "Scholarship":
            continue
            
        # STRICT FILTER 2: Status must match (or be General Public)
        if p["category"] != u_status and p["category"] != "General Public":
            continue
            
        # Basic Eligibility
        if not (p["min_age"] <= u_age <= p["max_age"]): continue
        if p["gender"] != "All" and p["gender"] != u_gender: continue
        if u_income > p["max_income"]: continue
        
        matches.append(p)
    return matches

if find_btn:
    results = get_verified_recommendations(status, age, gender, income)
    
    if results:
        st.subheader(f"Results for {status} ({age}yr, {gender})")
        for r in results:
            tag_type = r["type"].lower()
            color_class = f"tag-{status.lower().split()[0]}" if r["category"] != "General Public" else "tag-general"
            if r["type"] == "Scholarship": color_class = "tag-scholarship"

            st.markdown(f"""
                <div class="policy-card">
                    <span class="tag {color_class}">{r['type']}</span>
                    <h3>{r['name']}</h3>
                    <p>{r['desc']}</p>
                    <a href="{r['url']}" target="_blank" class="apply-btn">Visit Official Portal ↗️</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No specific government policies matched your current criteria.")
else:
    st.info("Please fill the sidebar and click 'Analyze Policies'.")
