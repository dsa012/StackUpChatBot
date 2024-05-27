# StackUp Helpdesk Bot 🤖

## Description
StackUp Helpdesk Bot is an AI-powered application designed to help users quickly find answers to their queries without having to manually search through the entire Zendesk Help Center. The bot fetches articles from Zendesk, cleans and processes the data, and uses this information to provide accurate and efficient responses to user questions via a user-friendly chatbot interface.

## Installation

### Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account
- EdenAI account
- Streamlit

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/dsa012/StackUpChatBot.git
   cd StackUpChatbot
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
- Create a .env file in the root directory and add the following variables:
  
  ```bash
  ATLAS_URI=your_mongodb_atlas_uri
  EDEN_API_KEY=your_edenai_api_key
  ```
4. Run the data retrieval script:
  ```bash
  python get-data.py
  ```
5. Clean the retrieved data:
  ```bash
  python clean-data.py
  ```
6. Run create-embedding.ipynb file to create and store the embeddings of the data on MongoDB
7. Goto Atlas Search on MongoDB and use the mongodb_vector_search_ed.json as schema for vector search and Name as "idx_embeddings", And finally select data document.
8. Run the main application:
  ```bash
  streamlit run main.py
  ```
9. Visit localhost:8501 to use the streamlit application.

