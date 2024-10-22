import streamlit as st
import requests

# Streamlit App
st.set_page_config(layout="wide")
st.title('Design Project Assistant')

# Creating columns for left and right layout
col1, col2 = st.columns(2)

# Placeholder questions in the left column
with col1:
    st.header("Tell me about your next design project")
    project_name = st.text_input("Project Name:", "Barn-inspired Design")
    design_style = st.text_input("Preferred Design Style:", "Rustic and minimal")
    materials = st.text_area("Materials you're thinking about:", "Wood, metal, natural elements")

    # Setting the context for the API call
    st.header("API Call Setup")
    api_key = st.text_input("OpenAI API Key", type="password")
    context = st.text_area("Context for ChatGPT:", "This is a design project that is based on a barn with meaningful family connections.")

    if st.button("Submit"):
        if not api_key:
            st.warning("Please provide your API key to proceed.")
        else:
            # Use customer's answers to set up the message
            prompt = f"{context}\n\nThe project is called '{project_name}'. It follows a '{design_style}' design style and uses materials such as '{materials}'. Could you give me ideas and suggestions for this design?"

            # API call to ChatGPT
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)

            # Handle API Response
            if response.status_code == 200:
                chat_response = response.json().get("choices", [])[0].get("message", {}).get("content", "No response from API.")
                with col2:
                    st.header("ChatGPT Response")
                    st.write(chat_response)
            else:
                with col2:
                    st.error(f"Error: {response.status_code}, {response.text}")
