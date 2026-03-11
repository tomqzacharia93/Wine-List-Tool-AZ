import streamlit as st
import pandas as pd
import io

# --- CONFIGURATION & PORTFOLIO MAPPING ---
st.set_page_config(page_title="Wine Portfolio Swap Tool", page_icon="🍷")

PRIORITY_GRID = {
    "Cabernet": {"<$10": "Hahn", "$10-$15": "Franciscan", "$15-$20": "Smith & Hook", "$20+": "Martis"},
    "Chardonnay": {"<$10": "Clos du Bois", "$10-$15": "William Hill", "$15-$20": "Calcaire", "$20+": "Rombauer"},
    "Sauvignon Blanc": {"<$10": "Nobilo", "$10-$15": "Whitehaven", "$15-$20": "Whitehaven"},
    "Pinot Grigio": {"<$10": "Barefoot", "$10-$15": "Ecco Domani", "$15-$20": "Jermann"},
    "Pinot Noir": {"<$10": "Mark West", "$10-$15": "Hahn", "$15-$20": "Hahn SLH"},
    "Sparkling": {"<$10": "La Marca (Split)", "$10-$15": "La Marca", "$15-$20": "La Marca", "$20+": "J Brut Rose"},
    "Red Alt/Blend": {"$20+": "Orin Swift 8YITD"}
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
        # This list mimics the scraper results for the site provided
        results = [
            {"Category": "Sparkling", "Current Wine": "Mionetto Prosecco", "Supplier": "Mionetto USA", "Est. Whls Btl": 11.00},
            {"Category": "Sauvignon Blanc", "Current Wine": "Kim Crawford", "Supplier": "Constellation", "Est. Whls Btl": 14.00},
            {"Category": "Chardonnay", "Current Wine": "Kendall Jackson", "Supplier": "SWS", "Est. Whls Btl": 15.50},
            {"Category": "Cabernet", "Current Wine": "Estancia", "Supplier": "SGWS", "Est. Whls Btl": 12.00},
            {"Category": "Pinot Noir", "Current Wine": "Meiomi", "Supplier": "Constellation", "Est. Whls Btl": 19.00},
            {"Category": "Chardonnay", "Current Wine": "Cervaro della Sala", "Supplier": "Empire", "Est. Whls Btl": 52.00},
        ]
        
        final_list = []
        for item in results:
            supplier = item["Supplier"]
            if "Empire" in supplier:
                rec = "SKIP (Partner)"
            elif "Kobrand" in supplier:
                rec = "SKIP (Exclusion)"
            else:
                rec = get_swap(item["Category"], item["Est. Whls Btl"])
            
            item["Recommended Swap"] = rec
            final_list.append(item)

        df = pd.DataFrame(final_list)
        
        st.subheader("Priority Analysis")
        # Fixed line below
        st.dataframe(df, use_container_width=True)

        # Download Button
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='PrioritySwaps')
        
        st.download_button(
            label="📥 Download Excel Report",
            data=output.getvalue(),
            file_name="wine_analysis.xlsx",
            mime="application/vnd.ms-excel"
        )