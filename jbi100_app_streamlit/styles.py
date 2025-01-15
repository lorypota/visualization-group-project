CSS_STYLE = '''
<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        overflow: hidden; /* Prevent unwanted scrolling */
    }
    [data-testid="stSidebar"][aria-expanded="true"] {
        min-width: 350px;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main > div.block-container > div > div > div{
        gap: 0rem !important; /* Delete top gap */
    }
    #stVerticalBlock {
        gap: 0rem !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .full-screen-map {
        height: calc(100vh); 
        margin: 0;
        padding: 0;
        top: 0;
    }
    .block-container {
        padding: 0 !important;
    }
    .stMainBlockContainer .stHorizontalBlock{
        gap: 0rem !important;
    }
    .stMainBlockContainer .stVerticalBlock{
        gap: 0rem !important;
    }
</style>
'''
