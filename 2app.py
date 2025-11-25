import streamlit as st
import requests
import pandas as pd

# --- Configuration ---
# REPLACE THIS WITH YOUR ACTUAL GOOGLE MAPS API KEY
API_KEY = "YOUR_API_KEY_HERE" 

def get_food_recommendations(query, location, min_price=0, max_price=4):
    """
    Fetches restaurant data from Google Places API.
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    # Combine query and location for a natural search string
    search_query = f"{query} in {location}"
    
    params = {
        "query": search_query,
        "key": API_KEY,
        "minprice": min_price,
        "maxprice": max_price,
        "type": "restaurant",
        "opennow": True  # Optional: only show places currently open
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] != 'OK':
            if data['status'] == 'ZERO_RESULTS':
                return []
            st.error(f"API Error: {data.get('error_message', data['status'])}")
            return []
            
        results = []
        for place in data['results']:
            # Construct Google Maps Link
            place_id = place.get("place_id")
            map_link = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            
            # Get basic info
            name = place.get("name")
            rating = place.get("rating", 0)
            user_ratings = place.get("user_ratings_total", 0)
            address = place.get("formatted_address", "No address found")
            price_level = place.get("price_level", None)
            
            # Create a clickable HTML link for the name
            name_html = f'<a href="{map_link}" target="_blank" style="text-decoration: none; color: #1E88E5; font-weight: bold;">{name}</a>'
            
            # Format price as symbols ($$$, etc.)
            price_symbol = "$" * int(price_level) if price_level is not None else "N/A"

            results.append({
                "Restaurant": name_html, # This contains the HTML link
                "Rating": rating,
                "Reviews": user_ratings,
                "Price": price_symbol,
                "Address": address,
                "Raw_Rating": rating # kept for sorting
            })
            
        return results

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# --- Streamlit App Layout ---
st.set_page_config(page_title="Global Food Finder", page_icon="🍔", layout="wide")

st.title("🍔 Global Food Finder")
st.markdown("Search for top-rated food anywhere in the world. Filter by budget and click the name to view on Google Maps.")

# Create columns for input fields
col1, col2 = st.columns(2)

with col1:
    food_query = st.text_input("What are you craving?", placeholder="e.g. Sushi, Italian, Tacos")

with col2:
    location_query = st.text_input("Where?", placeholder="e.g. Tokyo, New York, Orchard Road Singapore")

# Budget Slider (0=Free, 4=Very Expensive)
budget_map = {0: "Free/Cheap", 1: "Inexpensive ($)", 2: "Moderate ($$)", 3: "Expensive ($$$)", 4: "Very Expensive ($$$$)"}
budget_range = st.select_slider(
    "Select Budget Range",
    options=[0, 1, 2, 3, 4],
    value=(1, 3), # Default range
    format_func=lambda x: budget_map[x]
)

if st.button("Find Top 20 Recommendations", type="primary"):
    if food_query and location_query:
        with st.spinner(f"Searching for the best {food_query} in {location_query}..."):
            # Fetch Data
            results = get_food_recommendations(food_query, location_query, min_price=budget_range[0], max_price=budget_range[1])
            
            if results:
                # Convert to DataFrame
                df = pd.DataFrame(results)
                
                # Sort by Rating (Descending) to get the "Top" items
                df = df.sort_values(by="Raw_Rating", ascending=False).head(20)
                
                # Drop the raw rating column used for sorting
                df = df.drop(columns=["Raw_Rating"])
                
                # Reset index to show 1, 2, 3...
                df.index = range(1, len(df) + 1)
                
                # Display as an HTML table to allow clickable links
                # We use st.markdown with unsafe_allow_html=True to render the <a> tags
                table_html = df.to_html(escape=False, classes="table table-striped")
                st.markdown(table_html, unsafe_allow_html=True)
                
                st.success(f"Found {len(df)} top-rated places!")
            else:
                st.warning("No restaurants found matching your criteria. Try widening the budget or changing the location.")
    else:
        st.warning("Please enter both a food type and a location.")
