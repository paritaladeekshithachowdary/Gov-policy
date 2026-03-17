import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="GovPolicy AI Agent", page_icon="🏛️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .policy-card { 
        padding: 25px; 
        border-radius: 12px; 
        background-color: white; 
        border-left: 8px solid #007bff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
        margin-bottom: 20px; 
    }
    .tag {
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
        margin-right: 5px;
    }
    .tag-student { background-color: #e3f2fd; color: #1976d2; }
    .tag-pension { background-color: #fff3e0; color: #e65100; }
    .apply-btn {
        display: inline-block;
        margin-top: 15px;
        padding: 10px 20px;
        background-color: #28a745;
        color: white !important;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- EXPANDED POLICY DATABASE ---
POLICIES = [
    {
        "name": "Pragati Scholarship (AICTE)",
        "min_age": 16, "max_age": 25, "gender": "Female", "max_income": 800000, 
        "category": "Student", "type": "Scholarship",
        "desc": "₹50,000 per year for girls in technical degree/diploma courses.",
        "url": "https://www.myscheme.gov.in/schemes/psgs-deg"
    },
    {
        "name": "Central Sector Scholarship (CSSS)",
        "min_age": 18, "max_age": 25, "gender": "All", "max_income": 450000, 
        "category": "Student", "type": "Scholarship",
        "desc": "For students above 80th percentile in Class 12. Provides up to ₹20,000 annually.",
        "url": "https://scholarships.gov.in/"
    },
    {
        "name": "Post-Matric Scholarship for Minorities",
        "min_age": 15, "max_age": 30, "gender": "All", "max_income": 200000, 
        "category": "Student", "type": "Scholarship",
        "desc": "Financial support for higher education (Class 11 to PhD).",
        "url": "https://scholarships.gov.in/"
    },
    {
        "name": "Lakhpati Didi Scheme",
        "min_age": 18, "max_age": 50, "gender": "Female", "max_income": 300000, 
        "category": "General Public", "type": "Skill Training",
        "desc": "Financial literacy and skill training for women in SHGs to earn ₹1 Lakh/year.",
        "url": "https://lakhpatididi.gov.in/"
    },
    {
        "name": "Atal Pension Yojana (APY)",
        "min_age": 18, "max_age": 40, "gender": "All", "max_income": 9999999, 
        "category": "General Public", "type": "Pension",
        "desc": "Monthly pension for unorganized workers. Requires monthly contributions.",
        "url": "https://www.npscra.nsdl.co.in/scheme-details.php"
    }
]

# --- UI ---
st.title("🏛️ Verified Indian Gov Policy Agent")

with st.sidebar:
    st.header("👤 Your Details")
    age = st.number_input("Age", 1, 100, 20)
    gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    income = st.number_input("Annual Income (₹)", 0, 10000000, 0)
    user_status = st.selectbox("Current Status", ["Student", "Working", "Unemployed", "Business Owner"])
    find_btn = st.button("Analyze Policies")

# --- IMPROVED AI MATCHING LOGIC ---
def get_matches(u_age, u_gender, u_income, u_status):
    results = []
    for p in POLICIES:
        # 1. Eligibility Check
        if not (p["min_age"] <= u_age <= p["max_age"]): continue
        if p["gender"] != "All" and p["gender"] != u_gender: continue
        if u_income > p["max_income"]: continue
        
        # 2. Ranking Logic
        rank = 0
        if p["category"] == u_status:
            rank += 10  # Top priority for your current status
        if p["type"] == "Scholarship" and u_status == "Student":
            rank += 5   # Extra boost for scholarships if you're a student
        
        results.append({**p, "rank": rank})
    
    # Sort by rank (Highest first)
    return sorted(results, key=lambda x: x['rank'], reverse=True)

if find_btn:
    matches = get_matches(age, gender, income, user_status)
    
    if matches:
        st.subheader(f"Top Recommendations for a {age}yo {gender} {user_status}")
        for m in matches:
            tag_class = "tag-student" if m["type"] == "Scholarship" else "tag-pension"
            st.markdown(f"""
                <div class="policy-card">
                    <span class="tag {tag_class}">{m['type']}</span>
                    <h3>{m['name']}</h3>
                    <p>{m['desc']}</p>
                    <p><b>Income Limit:</b> Up to ₹{m['max_income']:,}</p>
                    <a href="{m['url']}" target="_blank" class="apply-btn">Apply on Official Portal ↗️</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No perfect matches found. Try broadening your criteria.")
else:
    st.info("← Enter your details to see verified scholarships and schemes.")
