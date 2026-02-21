import streamlit as st
from openai import OpenAI

# ================= CONFIG =================
st.set_page_config(
    page_title="AgroNova",
    page_icon="🌾",
    layout="wide"
)

# ================= GROQ SETUP =================
GROQ_API_KEY = "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"  # must start with gsk_

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# ================= UI STYLE =================
st.markdown("""
<style>

/* Black main background */
[data-testid="stAppViewContainer"] {
    background-color: #000000 !important;
}

/* White text everywhere */
html, body, p, h1, h2, h3, h4, h5, h6, span, label, div {
    color: #ffffff !important;
}

/* Green sidebar */
section[data-testid="stSidebar"] {
    background-color: #14532d !important;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Buttons */
.stButton>button {
    background-color: #1f7a5c !important;
    color: white !important;
    border-radius: 6px;
}
.stButton>button:hover {
    background-color: #0f5132 !important;
}

</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "queries" not in st.session_state:
    st.session_state.queries = 0

# ================= SIDEBAR =================
st.sidebar.title("🌾 AgroNova")

country = st.sidebar.selectbox("Select Country", ["India", "Canada"])

page = st.sidebar.radio(
    "Navigate",
    ["Home", "AI Assistant", "Crop Calendar", "Alerts", "Feedback"]
)

# ================= HOME =================
if page == "Home":
    st.title("AgroNova Smart Farming")
    st.write("AI-powered crop advisory system.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total AI Queries", st.session_state.queries)
    col2.metric("AI Availability", "24/7")
    col3.metric("Coverage", "Multi-Crop")

    st.markdown("### Platform Features")
    st.write("• AI Crop Recommendation")
    st.write("• Seasonal Crop Calendar")
    st.write("• Risk & Safety Alerts")
    st.write("• Farmer Feedback System")

# ================= AI ASSISTANT =================
elif page == "AI Assistant":

    st.header("Ask AgroNova AI")

    question = st.text_area("Describe your farming condition")

    if st.button("Generate Recommendation"):
        if question.strip() != "":
            try:
                with st.spinner("Generating AI response..."):

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "system",
                                "content": f"You are an agricultural expert in {country}. Provide structured advice with sections: Recommended Crops, Reason, Practical Advice, and Safety Tips."
                            },
                            {
                                "role": "user",
                                "content": question
                            }
                        ],
                        temperature=0.7,
                        max_tokens=800
                    )

                    ai_response = response.choices[0].message.content
                    st.markdown(ai_response)
                    st.session_state.queries += 1

            except Exception as e:
                st.error(f"Groq API error: {e}")

# ================= CROP CALENDAR =================
elif page == "Crop Calendar":
    st.header("Crop Calendar")

    season = st.selectbox("Select Season", ["Spring", "Summer", "Winter"])

    if season == "Spring":
        st.write("🌱 Tomato – 18-24°C – Needs sunlight")
        st.write("🌱 Lettuce – 15-20°C – Cool season crop")
    elif season == "Summer":
        st.write("🌱 Corn – 25-30°C – Strong sunlight")
        st.write("🌱 Watermelon – 25-35°C – Needs space & water")
    else:
        st.write("🌱 Wheat – 10-15°C – Cool climate")
        st.write("🌱 Garlic – Cold season crop")

# ================= ALERTS =================
elif page == "Alerts":
    st.header("Alerts")
    st.warning("High temperature advisory.")
    st.warning("Pest activity detected.")
    st.warning("Irrigation monitoring recommended.")

# ================= FEEDBACK =================
elif page == "Feedback":
    st.header("Feedback")

    feedback = st.text_area("Share your feedback")

    if st.button("Submit"):
        st.success("Thank you for your feedback.")