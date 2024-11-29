import streamlit as st
import google.generativeai as genai

# Load API key
def load_api_key(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        st.error("API key file not found. Please check the file path.")
        return None

# Configure Generative AI API
def configure_genai(api_key):
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to configure Generative AI: {e}")

# Initialize the generative model
def initialize_model(model_name, system_instruction):
    try:
        return genai.GenerativeModel(
            model_name=model_name, system_instruction=system_instruction
        )
    except Exception as e:
        st.error(f"Failed to initialize the model: {e}")
        return None

# Main function for the Streamlit app
def main():
    st.set_page_config(page_title="AI Code Reviewer", layout="centered")
    
    # Title and introduction
    st.title("🔍 AI Code Reviewer")
    st.subheader("Get instant, expert feedback on your Python code!")
    st.markdown(
        """
        This app leverages AI to review your Python code for errors, 
        suggest improvements, and provide helpful feedback.
        """
    )

    # Load and configure API key
    api_key_path = r"C:\Users\skjaa\.vscode\GEMINI\KEYS\.gemini.txt"
    api_key = load_api_key(api_key_path)
    if not api_key:
        return

    configure_genai(api_key)

    # Load system instruction (if needed)
    sys_instruction_path = r"C:\Users\skjaa\.vscode\GEMINI\KEYS\requirements.txt"
    try:
        with open(sys_instruction_path, "r") as f:
            system_instruction = f.read()
    except FileNotFoundError:
        st.warning("System instruction file not found. Using default instructions.")
        system_instruction = "You are an expert AI code reviewer. Review and suggest improvements."

    # Input area for Python code
    user_prompt = st.text_area(
        "📄 Enter your Python code here:",
        placeholder="Paste your code here...",
        height=300
    )

    # Generate review button
    if st.button("🛠 Generate Review"):
        if user_prompt.strip():
            try:
                # Initialize the AI model
                model = initialize_model("models/gemini-1.5-pro", system_instruction)
                if not model:
                    return

                # Start a chat session with the model
                ai_assistant = model.start_chat(history=[])

                # Generate AI review
                response = ai_assistant.send_message(
                    f"Please review the following Python code for errors or improvements:\n\n{user_prompt}\n\nProvide feedback and suggest fixes if necessary."
                )

                # Display the AI's response
                st.markdown("### ✅ **Code Review Feedback**")
                st.success(response.text)

            except Exception as e:
                st.error(f"An error occurred while generating the review: {e}")
        else:
            st.warning("Please enter Python code to review.")

# Run the app
if __name__ == "__main__":
    main()