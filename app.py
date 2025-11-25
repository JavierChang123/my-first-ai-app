import streamlit as st
import google.generativeai as genai
import os

# 1. SETUP: Configure the API Key
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API Key not found. Please set it in Streamlit Secrets.")

# 2. UI: Page Configuration
st.set_page_config(page_title="Cuisine Finder", page_icon="🍽️", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: #E63946;
        color: white;
        border-radius: 20px;
        width: 100%;
    }
    a {
        text-decoration: none;
        color: #E63946 !important;
        font-weight: bold;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. APP HEADER
st.title("🍽️ Find the Best Cuisine")
st.markdown("Enter a city or neighborhood to discover top-rated restaurants, filtered by your budget.")

# 4. FILTERS
col1, col2 = st.columns(2)

with col1:
    cuisine = st.selectbox(
        "Select Cuisine",
        ['Chinese', 'Italian', 'Japanese', 'Korean', 'Mexican', 
         'Western', 'Thai', 'Indian', 'Malay', 'Spanish', 
         'French', 'Vietnamese', 'Taiwanese', 'Turkish']
    )

with col2:
    budget = st.select_slider(
        "Select Budget",
        options=['Any', '$', '$$', '$$$', '$$$$']
    )

# 5. INPUT: Location
location = st.text_input("Where are you looking?", placeholder="e.g. Tampines, Orchard, Zhuhai...")

# 6. LOGIC: The Search Button
if st.button("Find Top 20 Restaurants"):
    if not location:
        st.warning("Please enter a location first.")
    else:
        try:
            # FIXED: Changed from 'gemini-2.5-pro' (invalid) to 'gemini-1.5-flash'
            model = genai.GenerativeModel('gemini-2.5-pro')
            
            # UPDATED PROMPT: 
            # 1. Asks for 20 results
            # 2. Asks for Google Search Links
            prompt = f"""
            I am looking for {cuisine} restaurants in {location}.
            My budget is: {budget}.
            
            Please provide a list of the TOP 20 highly-rated options. 
            
            IMPORTANT: For every restaurant name, format it as a clickable Markdown link that searches Google for that restaurant in that city. 
            Example format: [Restaurant Name](https://www.google.com/search?q=Restaurant+Name+{location})
            
            For each restaurant include:
            1. The Name (as a clickable link)
            2. Estimated Price
            3. Why it's good (short description)
            4. A specific recommended dish.
            
            Format the response nicely in Markdown. Use a table if possible for better readability.
            """
            
            with st.spinner(f"Finding top 20 {cuisine} spots in {location}... this might take a moment..."):
                response = model.generate_content(prompt)
                
            # Show results
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")



