README.md - Monday.com BI Agent
Overview
This project implements a simple Business Intelligence (BI) Agent that connects to monday.com boards and answers business questions such as:
•	Sales pipeline overview
•	Sector performance
•	Execution status of work orders
The agent retrieves live data from monday.com using the GraphQL API and performs lightweight analysis to generate business insights.
A simple web interface built with Streamlit allows users to ask questions and receive analytical summaries.
________________________________________
Architecture Overview
The system consists of three main components:
1. Data Retrieval Layer
The agent connects to the monday.com API using GraphQL requests.
Function:
fetch_board_data(board_id)
Responsibilities:
•	Send API request to monday.com
•	Retrieve board items
•	Extract column values
•	Convert results into a pandas DataFrame
This layer ensures that all analysis uses the latest data from the monday.com boards.
________________________________________
2. Question Interpretation Layer
User questions are interpreted using a simple rule-based approach.
Function: interpret_question(question)
The function categorizes questions into three main types:
•	Pipeline analysis
•	Sector performance
•	Execution status analysis
Keyword detection is used to determine the appropriate category.
________________________________________
3. Analysis Layer
Once a question is categorized, the system performs the appropriate analysis.
Key functions include:
pipeline_summary(deals)
This generates:
•	Total deals in pipeline
•	Deals by stage
•	Deals by status
•	Sector distribution
•	Simple executive insights
Additional analysis functions summarize work orders by sector and execution status.
________________________________________
4. User Interface
The user interface is implemented using Streamlit.
Features:
•	Text input for business questions
•	Automatic question interpretation
•	Display of analytical results
•	Real-time interaction with monday.com data
________________________________________
Setup Instructions
1. Install Dependencies
Create a virtual environment and install required packages:
pip install -r requirements.txt
Required libraries include:
•	requests
•	pandas
•	streamlit
________________________________________
2. Configure monday.com API
1.	Generate a monday.com API token from your monday.com account.
2.	Replace the token in the code:
API_TOKEN = "YOUR_API_TOKEN"
________________________________________
3. Configure Board IDs
Update the board IDs used by the system:
Work Orders Board:
5027142116

Deals / Pipeline Board:
5027142158
These boards should contain columns such as:
Work Orders board:
•	Sector
•	Execution Status
Deals board:
•	Deal Stage
•	Deal Status
•	Sector/service
________________________________________
4. Run the Application
Run the Streamlit application:
streamlit run app.py
The application will start locally and open in the browser.
________________________________________
Deployment
The project can be deployed using Streamlit Community Cloud.
Steps:
1.	Push the code to GitHub
2.	Connect the repository to Streamlit Cloud
3.	Deploy the app
Example deployment URL:
https://monday-bi-agent-assignment.streamlit.app/
________________________________________
Limitations
•	Question interpretation uses simple keyword matching
•	Data visualization is limited
•	Large boards may require pagination and caching
These could be improved in future iterations.
________________________________________
Bonus Feature
The system includes a Leadership Update feature that generates a high-level pipeline summary including:
•	Total deals
•	Deals by stage
•	Deals by status
•	Sector distribution
•	Key insights about negotiation and conversion stages
This simulates the type of summary typically shared with leadership teams during business reviews.

