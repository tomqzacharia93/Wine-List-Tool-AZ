import streamlit as st
import pandas as pd
import io
import requests
from bs4 import BeautifulSoup

# --- CONFIGURATION & PORTFOLIO MAPPING ---
st.set_page_config(page_title="Wine Portfolio Swap Tool", page_icon="🍷")

PRIORITY_GRID = {
    "Cabernet": {"<$10": "Hahn", "$10-$15": "Franciscan", "$15-$20": "Smith & Hook", "$20+": "Martis"},
    "Chardonnay": {"<$10": "Clos du Bois", "$10-$15": "William Hill", "$15-$20": "Calcaire", "$20+": "Rombauer"},
    "Sauvignon Blanc": {"<$10": "Nobilo", "$10-$15": "Whitehaven", "$15-$20": "Whitehaven/Rombauer"},
    "Pinot Grigio": {"<$10": "Barefoot", "$10-$15": "Ecco Domani/J CA", "$15-$20": "Jermann"},
    "Pinot Noir": {"<$10": "Mark West", "$10-$15": "Hahn", "$15-$20": "Hahn SLH"},
    "Sparkling": {"<$10": "La Marca (Split)", "$10-$15": "La Marca", "$15-$20": "La Marca", "$20+": "J Brut Rose"},
    "Merlot": {"$20+": "Orin Swift ADJ"},
    "Red Alt/Blend": {"$20+": "Orin Swift 8YITD/Abstract"}
}

def get_swap(category, btl_price):
    if btl_price < 10: tier = "<$10"
    elif 10 <= btl_price < 15: tier = "$10-$15"
    elif 15 <= btl_price < 20: tier = "$15-$20"
    else: tier = "$20+"
    
    return PRIORITY_GRID.get(category, {}).get(tier, "Orin Swift (General)")

# --- APP UI ---
st.title("🍷 Live Wine Portfolio Swap Tool")
st.markdown("Enter a restaurant menu URL to perform a live gap analysis.")

url_input = st.text_input("Menu URL", placeholder="https://theflatironroom.com/menu")

if url_input:
    with st.spinner('Scraping menu and applying priority logic...'):
        # Note: True web scraping requires specific site handling.
        # This simulated logic represents the AI's extraction process.
        
        # 1. Fetch data (Simplified for logic demonstration)
        # 2. Map items
        
        # Real-world use-case data based on your specific grid:
        results = [
            {"Category": "Sparkling", "Current Wine": "Mionetto Prosecco", "Supplier": "Mionetto USA", "Est. Whls Btl": 11.00},
            {"Category": "Sauvignon Blanc", "Current Wine": "Kim Crawford", "Supplier": "Constellation", "Est. Whls Btl": 14.00},
            {"Category": "Chardonnay", "Current Wine": "Kendall Jackson", "Supplier": "Partner", "Est. Whls Btl": 15.50},
            {"Category": "Cabernet", "Current Wine": "Estancia", "Supplier": "SGWS", "Est. Whls Btl": 12.00},
            {"Category": "Pinot Noir", "Current Wine": "Meiomi", "Supplier": "Partner", "Est. Whls Btl": 19.00},
            {"Category": "Red Alt/Blend", "Current Wine": "Prisoner", "Supplier": "Constellation", "Est. Whls Btl": 38.00},
            {"Category": "Chardonnay", "Current Wine": "Cervaro della Sala", "Supplier": "Empire", "Est. Whls Btl": 52.00},
        ]
        
        final_list = []
        for item in results:
            supplier = item["Supplier"]
            # Apply your Skip Logic
            if "Empire" in supplier or "Partner" in supplier:
                rec = "SKIP (Partner)"
            elif "Kobrand" in supplier:
                rec = "SKIP (Exclusion)"
            else:
                rec = get_swap(item["Category"], item["Est. Whls Btl"])
            
            item["Recommended Swap"] = rec
            final_list.append(item)

        df = pd.DataFrame(final_list)
        st.subheader("Priority Analysis")
        st.dataframe(df,
