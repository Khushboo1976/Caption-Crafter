import streamlit as st
from generator.model import generate_caption
import os

st.set_page_config(page_title="CaptionCrafter", layout="centered", page_icon="✨")

# Load custom CSS
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

logo_path = "assets/logo.jpg"
if os.path.exists(logo_path):
    st.markdown("""
    <div style='display: flex; justify-content: center; align-items: center; margin-bottom: 10px;'>
    <div style='width: 100%; max-width: 600px;'>
    """, unsafe_allow_html=True)
    st.image(logo_path, use_container_width=True, caption=None)
    st.markdown("""
    </div>
    </div>
    """, unsafe_allow_html=True)

st.title("✨ Caption Crafter")
st.subheader("Chat with the AI Caption Generator ✨")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Theme options
themes = ["Trip", "New Project", "Achievement", "Event", "Announcement", "Other"]

# Chat input area
with st.form("caption_form"):
    col1, col2 = st.columns([4, 1])
    with col1:
        selected_theme = st.selectbox("Pick a theme:", themes, key="theme_select")
        if selected_theme == "Other":
            user_input = st.text_input("Enter your own keywords or theme:", key="user_input")
        else:
            user_input = st.text_input("Add specific keywords (optional):", key="user_input")
        description = st.text_area("Add a description (optional):", key="desc_input")
    with col2:
        uploaded_image = st.file_uploader("Attach an image (optional):", type=["jpg", "jpeg", "png"], key="img_uploader")
    submitted = st.form_submit_button("Generate Caption")

# Handle text submission
if submitted and (user_input or description):
    # Show progress bar while generating caption
    progress_bar = st.progress(0)
    progress_bar.progress(50, text="Generating caption...")
    if selected_theme == "Other":
        prompt = f"{user_input}. {description}" if description else user_input
    else:
        prompt = f"{selected_theme}: {user_input}. {description}" if description else (f"{selected_theme}: {user_input}" if user_input else selected_theme)
    ai_caption = generate_caption(prompt)
    progress_bar.progress(100, text="Completed!")
    st.session_state["caption"] = ai_caption
    progress_bar.empty()

# Handle image upload (if not already handled by form submission)
if uploaded_image and not submitted:
    st.session_state["messages"].append({"role": "user", "content": "[Image uploaded]"})
    ai_caption = "Image-to-caption is not implemented in this demo. Please enter text for now."
    st.session_state["messages"].append({"role": "ai", "content": ai_caption})

# Display output only (no user messages)
if "caption" in st.session_state:
    st.markdown(f"""
    <div class='ai-output-bubble'>
        <b>AI Caption:</b><br/>
        <pre style='margin:0;background:none;border:none;white-space:pre-wrap;'>{st.session_state['caption']}</pre>
    </div>
    """, unsafe_allow_html=True)
