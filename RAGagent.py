import google.generativeai as genai

# 1. Setup API Key
genai.configure(api_key="YOUR_FREE_API_KEY")

# 2. Upload your Resume (Once)
sample_file = genai.upload_file(path="resume.pdf", display_name="My Resume")

# 3. Initialize Model with "Tools" for GitHub


def get_github_activity(username: str):
    # You would put your real fetch logic here
    return f"Latest activity for {username}: Added Docker support to Kanban project."


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[get_github_activity]  # This allows the AI to 'call' your code
)

# 4. Ask a question
response = model.generate_content(
    [sample_file, "What is the user's latest GitHub activity?"])
print(response.text)
