import streamlit as st
import pandas as pd
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="Wine Portfolio Swap Tool", page_icon="🍷")

# --- TITLES ---
st.title("🍷 Wine Portfolio Swap Tool")
st.markdown("Enter a restaurant menu URL to identify priority swaps and partner protection.")

# --- INPUT ---
url = st.text_input("Menu URL", placeholder="https://www.lapecorabianca.com/nomad-menu/")

if url:
    with st.spinner('Analyzing menu...'):
        # This is where the logic we built resides
        # Note: In a live app, this would trigger a scraping function.
        # For this version, we are pre-loading the analysis for the sites we discussed.
        
        data = [
            {"Wine": "Prosecco, Cantina Di Lana", "Supplier": "Matchvilla", "Btl Wholesale": 12.00, "Recommendation": "La Marca", "Type": "Tier 1 Priority"},
            {"Wine": "Sauvignon Blanc, Luisa", "Supplier": "Polaner", "Btl Wholesale": 14.66, "Recommendation": "Whitehaven", "Type": "Tier 1 Priority"},
            {"Wine": "Soave, Pieropan", "Supplier": "Empire", "Btl Wholesale": 15.33, "Recommendation": "SKIP", "Type": "Partner Distributor"},
            {"Wine": "Gavi, Villa Sparina", "Supplier": "Skurnik", "Btl Wholesale": 14.66, "Recommendation": "Whitehaven", "Type": "Tier 1 Priority"},
            {"Wine": "Barbera, GD Vajra", "Supplier": "Vinifera", "Btl Wholesale": 16.00, "Recommendation": "Orin Swift 'Abstract'", "Type": "Luxury BU"},
            {"Wine": "Cabernet, Chimney Rock", "Supplier": "Kobrand", "Btl Wholesale": 84.00, "Recommendation": "SKIP", "Type": "Excluded Supplier"}
        ]
        
        df = pd.DataFrame(data)
        
        # --- DISPLAY TABLE ---
        st.subheader("Analysis Summary")
        
        def highlight_skips(val):
            color = '#ff4b4b' if val == 'SKIP' else '#00cc66'
            return f'color: {color}; font-weight: bold'

        st.table(df.style.applymap(highlight_skips, subset=['Recommendation']))

        # --- EXPORT TO EXCEL ---
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Swaps')
        
        st.download_button(
            label="📥 Download Excel Report",
            data=output.getvalue(),
            file_name="wine_portfolio_analysis.xlsx",
            mime="application/vnd.ms-excel"
        )

st.sidebar.header("Instructions")
st.sidebar.write("1. Paste the URL of the menu.")
st.sidebar.write("2. View the swap recommendations.")
st.sidebar.write("3. Empire and Kobrand items are automatically skipped.")