from dotenv import load_dotenv
import os
load_dotenv()
# Copyleaks Account credintials 
EMAIL_ADDRESS= os.environ.get('EMAIL_ADDRESS')
KEY = os.environ.get('KEY')
# Zotero credintials 
library_id = os.environ.get('library_id')
library_type = os.environ.get('library_type')
zoter_api_key = os.environ.get('zoter_api_key')
# OPENAI credintials 
#open_ai_key = os.environ.get('open_ai_key')
Anthropic_key = os.environ.get('Anthropic_key')

api_url = os.environ.get('API_URL')
semantic_api_key = os.environ.get('semantic_api_key')
#webhook endpoint for plagiarism
webhook_endpoint = os.environ.get('webhook_endpoint')