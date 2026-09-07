import streamlit as st
import requests

st.set_page_config(page_title="Crop AI Doctor", layout="wide")

st.title("🌾 Crop Disease Diagnostic Assistant")
st.markdown("#### *💡 Motive: One photo is equal to disease prevention.*")
st.caption("Identify crop issues early, get local medicine recommendations, and save your harvest.")
st.hr()

with st.sidebar:
    st.header("📋 App Workflow & Guide")
    st.info("1. Select your local region and crop type.\n2. Upload 1 or more clear photos of the infected leaves.\n3. Click Analyze to see stage-based medicine recommendations.")
    
    st.subheader("⚙️ Settings")
    selected_lang = st.selectbox("🌐 Language", ["English", "Hindi/Hinglish"])
    lang_code = "en" if selected_lang == "English" else "hi"
    
    region = st.selectbox("📍 Region / Area", ["North India", "West India", "East India", "South India"])
    crop_type = st.selectbox("🍎 Crop Classification", ["Vegetable", "Fruit", "Grain/Cereal"])

uploaded_files = st.file_uploader(
    "📸 Upload Crop Photos (Select multiple files for better analysis)", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    cols = st.columns(min(len(uploaded_files), 4))
    for idx, file in enumerate(uploaded_files):
        with cols[idx % 4]:
            st.image(file, caption=f"Photo {idx+1}", use_container_width=True)

    if st.button("🔍 Run Full Diagnostic Check"):
        files_payload = [("files", (f.name, f.getvalue(), f.type)) for f in uploaded_files]
        data_payload = {"lang": lang_code, "region": region, "crop_type": crop_type}
        
        try:
            # Change this URL to your deployed Render FastAPI Web Service URL later
            BACKEND_URL = "http://127.0.0" 
            response = requests.post(BACKEND_URL, files=files_payload, data=data_payload)
            
            if response.status_code == 200:
                res = response.json()
                details = res["details"]
                
                st.success(f"## 📋 Detected Condition: {details['name']}")
                st.write(f"*Target Analysis Environment:* Configured for {res['region_applied']} | Category: {res['crop_type']}")
                st.markdown(f"### ⚠️ Visual Symptoms\n{details['symptoms']}")
                st.hr()
                
                st.markdown("### 🛠️ Actionable Treatment Guide (Normal-Early-Deep)")
                t_col1, t_col2, t_col3 = st.columns(3)
                with t_col1:
                    st.subheader("🟢 Early Stage Treatment")
                    st.write(details["early"])
                with t_col2:
                    st.subheader("🟡 Normal Stage Treatment")
                    st.write(details["normal"])
                with t_col3:
                    st.subheader("🔴 Deep/Severe Infection")
                    st.write(details["deep"])
        except Exception:
            st.error("Could not connect to the backend API service.")
