CSS_STYLE = '''
<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        overflow: hidden; /* Prevent unwanted scrolling */
    }
    [data-testid="stSidebar"][aria-expanded="true"] {
        min-width: 350px;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .full-screen-map {
        height: calc(100vh); /* Full viewport height minus Streamlit padding */
        margin: 0;
        padding: 0;
        top: 0;
    }
    .block-container {
        padding: 0 !important;
    }
    .stMainBlockContainer .stVerticalBlock {
        gap: 0rem !important;
    }
</style>
'''
