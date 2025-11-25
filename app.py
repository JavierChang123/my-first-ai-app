import streamlit as st
import google.generativeai as genai
import os

# 1. SETUP: Configure the API Key
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API Key not found. Please set it in Streamlit Secrets.")

# 2. UI: Page Configuration
st.set_page_config(page_title="Cuisine Finder", page_icon="🍽️")

# Custom CSS to make it look nicer (like your React code)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #E63946;
        color: white;
        border-radius: 20px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. APP HEADER
st.title("🍽️ Find the Best Cuisine")
st.markdown("Enter a city or neighborhood to discover top-rated restaurants, filtered by your budget.")

# 4. FILTERS (Cuisine and Budget)
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
location = st.text_input("Where are you looking?", placeholder="e.g. San Francisco, Singapore, Zhuhai...")

# 6. LOGIC: The Search Button
if st.button("Find Restaurants"):
    if not location:
        st.warning("Please enter a location first.")
    else:
        try:
            # Create the model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Create the prompt based on your filters
            prompt = f"""
            I am looking for {cuisine} restaurants in {location}.
            My budget is: {budget}.
            
            Please provide a list of the top 5 highly-rated options. 
            For each restaurant include:
            1. Name
            2. Estimated Price
            3. Why it's good (short description)
            4. A specific recommended dish.
            
            Format the response nicely in Markdown.
            """
            
            with st.spinner(f"Consulting the culinary maps for {cuisine} spots in {location}..."):
                response = model.generate_content(prompt)
                
            # Show results
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")


