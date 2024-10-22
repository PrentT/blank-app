import streamlit as st
import requests
import json

# Streamlit App
st.set_page_config(layout="wide")
st.title('Design Project Assistant')

# Creating columns for left and right layout
col1, col2 = st.columns(2)

# Placeholder questions in the left column
with col1:
    st.header("General Overview")
    vision_goals = st.text_area("Can you describe your vision or goals for this project?", placeholder="I’m aiming for a fresh, functional design that suits my lifestyle and personal taste.")

    st.header("Room Use & Function")
    primary_function = st.text_input("What is the primary function of this space?", placeholder="This will be a multi-purpose room used for both work and relaxation.")
    traffic = st.text_input("How much daily traffic does this room get?", placeholder="It will have moderate traffic throughout the day.")
    children_use = st.text_input("Will children use this room? If so, what should be considered for them?", placeholder="Yes, this space needs to be kid-friendly and safe.")
    personal_shared = st.text_input("Will this space be primarily for personal use, or shared?", placeholder="This room will be shared with family and occasional guests.")

    st.header("Emotions")
    atmosphere = st.text_input("What feeling or atmosphere do you want this space to create?", placeholder="I’d like it to feel serene and inviting, but also energizing.")

    st.header("Budget")
    budget = st.text_input("Do you have a budget in mind for this project?", placeholder="I’m looking to stay within a mid-range budget, but open to flexibility.")

    st.header("Existing Furniture/Items")
    existing_pieces = st.text_area("Are there any existing pieces or elements you’d like to incorporate into the design?", placeholder="I’d like to keep a few key pieces of furniture and some family heirlooms.")

    st.header("Upload Images")
    uploaded_images = st.file_uploader("Upload images that represent the style and vibe you want for this project", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

    # Setting the context for the API call
    st.header("API Call Setup")
    api_key = st.text_input("OpenAI API Key", type="password")
    context = st.text_area("Context for ChatGPT:", "You’re helping to interpret responses from a customer about their upcoming design project. Extract key details from their answers to display them as clear project specifications. All details are optional, so if any information is not provided, leave it blank or state \"N/A\" for that item. Highlight details such as the timeframe, budget, number of rooms, primary use of each room, emotional atmosphere they want, existing furniture or items they want to keep, and consider any uploaded images that provide a sense of the style or vibe desired.\n\nAdditionally, provide two outputs:\n1. A friendly, human-like response that acknowledges the customer's design inputs and summarizes them concisely.\n2. A list of key elements extracted from the input, displayed separately at the top for quick reference.")
    chat_message = st.text_area("Chat Message (use {variable_name} for placeholders):", "Here’s the customer’s input:\n\n* General Overview: \"{vision_goals}\"\n* Room Use & Function:\n    * Primary Function: \"{primary_function}\"\n    * Traffic Level: \"{traffic}\"\n    * Kids: \"{children_use}\"\n    * Personal or Shared: \"{personal_shared}\"\n* Emotions: \"{atmosphere}\"\n* Budget: \"{budget}\"\n* Existing Furniture/Items: \"{existing_pieces}\"\n* Uploaded Images: {uploaded_images}\n\nUsing this information, please extract and summarize the following project specs. If any information is missing or not mentioned, note it as \"N/A.\"\n* Timeframe:\n* Budget:\n* Number of Rooms:\n* Primary Room Use:\n* Emotional Atmosphere:\n* Existing Furniture/Items:\n* Uploaded Images:\n\nExpected Output Example:\nKey Elements Summary:\n* Timeframe: N/A (Customer hasn’t provided a specific deadline)\n* Budget: {budget}\n* Number of Rooms: N/A\n* Primary Room Use: {primary_function}\n* Emotional Atmosphere: {atmosphere}\n* Existing Furniture/Items: {existing_pieces}\n* Uploaded Images: {uploaded_images}\n\nHuman-Like Summary for Customer: \"Thank you for sharing your vision for your project!\"")

    if st.button("Submit"):
        if not api_key:
            st.warning("Please provide your API key to proceed.")
        else:
            # Convert uploaded images to base64 strings to include in prompt (if any images are uploaded)
            image_descriptions = []
            if uploaded_images:
                for img in uploaded_images:
                    image_descriptions.append(f"Image: {img.name}")
            images_text = "\n".join(image_descriptions) if image_descriptions else "N/A"

            # Use customer's answers to set up the message
            prompt = chat_message.format(
                vision_goals=vision_goals,
                primary_function=primary_function,
                traffic=traffic,
                children_use=children_use,
                personal_shared=personal_shared,
                atmosphere=atmosphere,
                budget=budget,
                existing_pieces=existing_pieces,
                uploaded_images=images_text
            )
            prompt = f"{context}\n\n{prompt}"

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

            # Display the entire request and response for debugging purposes
            with st.expander("Debugging Information"):
                st.subheader("Request Data")
                st.json(data)
                st.subheader("Response Data")
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.text(response.text)

    # Button to autofill placeholders for testing
    if st.button("Autofill Placeholder Values"):
        vision_goals = st.session_state.vision_goals = "I’m aiming for a fresh, functional design that suits my lifestyle and personal taste."
        primary_function = st.session_state.primary_function = "This will be a multi-purpose room used for both work and relaxation."
        traffic = st.session_state.traffic = "It will have moderate traffic throughout the day."
        children_use = st.session_state.children_use = "Yes, this space needs to be kid-friendly and safe."
        personal_shared = st.session_state.personal_shared = "This room will be shared with family and occasional guests."
        atmosphere = st.session_state.atmosphere = "I’d like it to feel serene and inviting, but also energizing."
        budget = st.session_state.budget = "I’m looking to stay within a mid-range budget, but open to flexibility."
        existing_pieces = st.session_state.existing_pieces = "I’d like to keep a few key pieces of furniture and some family heirlooms."
