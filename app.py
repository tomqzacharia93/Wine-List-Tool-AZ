import streamlit as st
import pandas as pd
import io
import re

# --- CONFIGURATION FROM YOUR GRID ---
PRIORITY_GRID = {
    "Cabernet": {"<$10": "Hahn", "$10-$15": "Franciscan", "$15-$20": "Smith & Hook", "$20+": "Martis"},
    "Chardonnay": {"<$10": "Clos du Bois", "$10-$15": "William Hill", "$15-$20": "Calcaire", "$20+": "Rombauer"},
    "Sauvignon Blanc": {"<$10": "Nobilo", "$10-$15": "Whitehaven", "$15-$20": "Whitehaven/Rombauer"},
    "Pinot Grigio": {"<$10": "Barefoot", "$10-$15": "Ecco Domani/J CA", "$15-$20": "Jermann"},
    "Pinot Noir": {"<$10": "Mark West", "$10-$15": "Hahn", "$15-$20": "Hahn SLH"},
    "Sparkling": {"<$10": "La Marca (split)", "$10-$15": "La Marca", "$15-$20": "La Marca", "$20+": "J Brut Rose"},
    "Merlot": {"$20+": "Orin Swift ADJ"},
    "Red Alt/Blend": {"$20+": "Orin Swift 8YITD/Abstract"}
}

def get_swap(category, price):
    if price < 10: tier = "<$10"
    elif 10 <= price < 15: tier = "$10-$15"
    elif 15 <= price < 20: tier = "$15-$20"
    else: tier = "$20+"
    return PRIORITY_GRID.get(category, {}).get(tier, "Orin Swift (General)")

st.set_page_config(page_title="Priority Swap Tool", page_icon="🍷")
st.title("🍷 Menu Text to Priority Swap")
st.markdown("Copy the text from a menu and paste it below. I'll identify the swaps based on your grid.")

# --- THE INPUT ENGINE ---
menu_text = st.text_area("Paste Menu Text Here:", height=200, placeholder="Example: Sauvignon Blanc, Luisa 2023... $68")

if st.button("Analyze Menu"):
    if menu_text:
        # Regex to find prices and names
        lines = menu_text.split('\n')
        final_results = []
        
        for line in lines:
            if not line.strip(): continue
            
            # Simple logic to find price and category
            price_match = re.findall(r'\d+', line)
            btl_price = int(price_match[-1]) / 4 if price_match else 15 # Est. wholesale from btl price
            
            # Identify Category
            cat = "Red Alt/Blend" # Default
            if "cabernet" in line.lower(): cat = "Cabernet"
            elif "chardonnay" in line.lower(): cat = "Chardonnay"
            elif "sauvignon" in line.lower(): cat = "Sauvignon Blanc"
            elif "grigio" in line.lower(): cat = "Pinot Grigio"
            elif "noir" in line.lower(): cat = "Pinot Noir"
            elif "prosecco" in line.lower() or "brut" in line.lower(): cat = "Sparkling"

            # Logic for Partners/Exclusions
            if any(x in line.lower() for x in ["empire", "antinori", "jermann", "allegrini"]):
                rec = "SKIP (Empire Partner)"
            elif "kobrand" in line.lower() or "chimney" in line.lower():
                rec = "SKIP (Kobrand)"
            else:
                rec = get_swap(cat, btl_price)
            
            final_results.append({
                "Menu Line": line[:50],
                "Detected Category": cat,
                "Est. Wholesale": btl_price,
                "Priority Swap": rec
            })

        df = pd.DataFrame(final_results)
        st.dataframe(df, use_container_width=True)
        
        # Download
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        st.download_button("📥 Download Excel Report", output.getvalue(), "swaps.xlsx")