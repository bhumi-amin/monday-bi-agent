import requests
import json
import pandas as pd
import streamlit as st

API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYzMTY1MzcyOSwiYWFpIjoxMSwidWlkIjoxMDA4NzA1OTEsImlhZCI6IjIwMjYtMDMtMTFUMTA6MTQ6MjUuOTIzWiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM0MTc0NDEzLCJyZ24iOiJhcHNlMiJ9.wxcP81tKSCMl6ZK2FYyCSJ6YoGLfMQrk3PP3fcq25dc"

url = "https://api.monday.com/v2"
headers = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}



######################################

def log_action(message):
    st.write(f"⚙️ {message}")

#####################################

def fetch_board_data(board_id):

    log_action(f"⚙️ Fetching live data from monday board {board_id}")

    query = f"""
    {{
      boards (ids: {board_id}) {{
        items_page {{
          items {{
            name
            column_values {{
              column {{
                title
              }}
              text
            }}
          }}
        }}
      }}
    }}
    """


    try:
        response = requests.post(url, json={'query': query}, headers=headers)
        log_action("Sending API request to monday.com")
        data = response.json()
    except Exception as e:
        log_action(f"⚠️ API error: {e}")
        return pd.DataFrame()

    items = data['data']['boards'][0]['items_page']['items']

    rows = []

    for item in items:
        row = {"Item Name": item["name"]}
        for col in item["column_values"]:
            row[col["column"]["title"]] = col["text"]
        rows.append(row)

    log_action("⚙️ Data retrieved successfully")

    df = pd.DataFrame(rows)

    # Data resilience: clean missing or inconsistent values
    df = df.fillna("Unknown")          # Handle null values
    df.columns = df.columns.str.strip() # Remove accidental spaces in column names

    return df

########################################

def analyze_work_orders():

    df = fetch_board_data(5027142116)

    print("📊 Total Work Orders:", len(df))

    if "Sector" in df.columns:
        print("\n📊 Work Orders by Sector:")
        print(df["Sector"].value_counts())

    if "Execution Status" in df.columns:
        print("\n📊 Execution Status Breakdown:")
        print(df["Execution Status"].value_counts())

#########################################

def ask_agent(question):

    print(f"🧠 Question received: {question}\n")

    work_orders = fetch_board_data(5027142116)
    deals = fetch_board_data(5027142158)

    question = question.lower()

    if "pipeline" in question or "deals" in question:
        print("📊 Pipeline Overview")
        print("Total Deals:", len(deals))

        if "Sector" in deals.columns:
            print("\nDeals by Sector:")
            print(deals["Sector"].value_counts())

    elif "sector" in question:
        print("📊 Work Orders by Sector:")
        print(work_orders["Sector"].value_counts())

    elif "status" in question:
        print("📊 Execution Status:")
        print(work_orders["Execution Status"].value_counts())

    else:
        print("⚠️ I couldn't fully understand the question yet.")
        print("Try asking about pipeline, sector, or status.")

####################################################

def pipeline_summary(deals):

    st.write("📊 Leadership Update: Sales Pipeline")
    st.write("\nTotal Deals:", len(deals))

    if "Deal Status" in deals.columns:
        st.write("\nDeals by Status:")
        st.write(deals["Deal Status"].value_counts())

    if "Deal Stage" in deals.columns:
        st.write("\nDeals by Stage:")
        st.write(deals["Deal Stage"].value_counts())

    if "Sector/service" in deals.columns:
        st.write("\nDeals by Sector:")
        st.write(deals["Sector/service"].value_counts())

    # Generate a simple business insight

    if "Deal Stage" in deals.columns:

        stage_counts = deals["Deal Stage"].value_counts()

        top_stage = stage_counts.idxmax()
        top_count = stage_counts.max()

        st.write("\nExecutive Summary:")
        st.write("💡 Key Insights")

        st.write(f"- Most deals ({top_count}) are currently in '{top_stage}', indicating strong pipeline activity at this stage.")

        if "F. Negotiations" in stage_counts:
            st.write(f"- {stage_counts['F. Negotiations']} deals are in negotiations, which may convert to revenue soon.")

        if "H. Work Order Received" in stage_counts:
            st.write(f"- {stage_counts['H. Work Order Received']} deals have already converted to work orders.")

################################################################


def extract_sector(question):

    q = question.lower()

    sectors = ["energy", "healthcare", "finance", "technology", "manufacturing"]

    for sector in sectors:
        if sector in q:
            return sector.capitalize()

    return None
    
########################################

from datetime import datetime

def extract_time_filter(question):

    q = question.lower()

    if "this quarter" in q:
        return "quarter"

    if "this month" in q:
        return "month"

    if "this year" in q:
        return "year"

    return None

###########################################


def interpret_question(question):

    q = question.lower()

    # pipeline related
    if any(word in q for word in ["pipeline", "deal", "sales", "revenue"]):
        return "pipeline"

    # sector related
    if any(word in q for word in ["sector", "industry", "segment"]):
        return "sector_analysis"

    # execution related
    if any(word in q for word in ["status", "execution", "progress"]):
        return "execution_status"

    return "unknown"

###################################################################

def smart_agent(question):

    print(f"\n🧠 Question: {question}")

    category = interpret_question(question)

    print("🤖 Interpreted as:", category)

    work_orders = fetch_board_data(5027142116)
    deals = fetch_board_data(5027142158)

    if category == "pipeline":
        pipeline_summary(deals)

    elif category == "sector_analysis":
        print("\n📊 Work Orders by Sector:")
        print(work_orders["Sector"].value_counts())

    elif category == "execution_status":
        print("\n📊 Execution Status:")
        print(work_orders["Execution Status"].value_counts())

    else:
        print("⚠️ I couldn't fully understand the question.")
        print("You can ask about pipeline, sector performance, or execution status.")

###############################################


################################################


st.title("📊 Monday.com BI Agent")

st.write("Ask a business question about pipeline, sector performance, or execution status.")

question = st.text_input("Ask a question")

if question:

    st.write("🧠 Question:", question)

    category = interpret_question(question)

    st.write("🤖 Interpreted as:", category)

    work_orders = fetch_board_data(5027142116)
    deals = fetch_board_data(5027142158)

    ##############################
    sector = extract_sector(question)
    time_filter = extract_time_filter(question)

    if sector and "Sector/service" in deals.columns:
        deals = deals[deals["Sector/service"].str.contains(sector, case=False, na=False)]
        st.write(f"📌 Filtered for sector: {sector}")

    if time_filter and "Close Date" in deals.columns:
        deals["Close Date"] = pd.to_datetime(deals["Close Date"], errors="coerce")

        now = datetime.now()

        if time_filter == "quarter":
            current_quarter = (now.month - 1) // 3 + 1
            deals = deals[deals["Close Date"].dt.quarter == current_quarter]
            st.write("📅 Filtered for: This Quarter")

        if time_filter == "month":
            deals = deals[deals["Close Date"].dt.month == now.month]
            st.write("📅 Filtered for: This Month")
#################################

    if category == "pipeline":
        pipeline_summary(deals)

    elif category == "sector_analysis":
        st.write("📊 Work Orders by Sector")
        st.write(work_orders["Sector"].value_counts())

    elif category == "execution_status":
        st.write("📊 Execution Status")
        st.write(work_orders["Execution Status"].value_counts())

    else:
        st.write("⚠️ I couldn't fully understand the question.")
