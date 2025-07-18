import streamlit as st
import pandas as pd
import json
st.title("Mr. Krab's Treasure Plan")

with open ("treasures.json") as f:
    treasures = pd.DataFrame(json.load(f))
    
if 'filtered' not in st.session_state:
    st.session_state.filtered = treasures
if 'clue_select' not in st.session_state:
    st.session_state.clue_select= list(treasures['clue'].unique())
if 'diff_select' not in st.session_state:
    st.session_state.diff_select = 10

st.sidebar.header("Filter Treasures")
clues = st.sidebar.multiselect(
    "Clue Types", options=treasures['clue'].unique(),
    default=st.session_state.clue_select,
    key='clue_select'           #NEW
)

max_diff = st.sidebar.number_input(
    "Max Difficulty", min_value=1, max_value=10,
    value=st.session_state.diff_select,
    key="diff_select"     #NEW
)

filtered = treasures[
    treasures['clue'].isin(clues) &
    (treasures['difficulty'] <= max_diff)
]
st.session_state.filtererd = filtered

st.subheader("Treasure Map")
st.map(
    filtered.rename(columns={'lat':'latitude','lon':'longitude'})
)

bar_placeholder = st.empty()  #NEW
line_placeholder = st.empty()  #NEW

if not filtered.empty:
    bar_placeholder.bar_chart(
        filtered.set_index('name')['loot']
    )
    line_placeholder.line_chart(
        filtered[['difficulty','loot']].set_index('difficulty')
    )
else:
    st.info("No treasures mathc your filters.")

if 'found_count' not in st.session_state:
    st.session_state.found_count = 0
if st.button("Claim all listed treasures"):
    st.session_state.found_count += len(filtered)
st.metric("Total treasures found:", st.session_state.found_count)

st.markdown("---")
st.write("**Treasure Details:**")
st.dataframe(filtered)

st.markdown(
    "### How it works:\n"
    "- **Sidebar inputs** filter treasures by clue type and difficulty.\n"
    "- **Map** shows treasure locations.\n"
    "- **Dynamic charts** update based on filter settings.\n"
    "- **Session state** stores selections and found treasurescounter.\n"
)








