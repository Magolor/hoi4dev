import datetime
import streamlit as st
from code_editor import code_editor
from hoi4dev import ccl_from_dict, ccl_to_dict, loads_json, dumps_json, is_json

code_buttons = [
    {
        "name": "Copy",
        "feather": "Copy",
        "hasText": True,
        "alwaysOn": True,
        "commands": [
            "copyAll"
        ],
        "style": {
            "top": "0.46rem",
            "right": "0.4rem"
        }
    }
]
def file_editor(file_path: str):
    """Edit a CCL/JSON file with conversion capabilities."""
    st.write("")
    st.write("")
    st.title("CCL/JSON Editor")

    # Initialize session state
    if 'file_path' not in st.session_state:
        st.session_state.file_path = file_path
    if 'original_content' not in st.session_state:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                if is_json(content):
                    st.session_state.json_text = dumps_json(loads_json(content), indent=4)
                    st.session_state.ccl_text = ccl_from_dict(loads_json(content))
                else:
                    st.session_state.ccl_text = content
                    st.session_state.json_text = dumps_json(ccl_to_dict(content), indent=4)
        except Exception as e:
            st.error(f"Failed to load file: {e}")
            return

    if 'active_editor' not in st.session_state:
        st.session_state.active_editor = "json" if is_json(st.session_state.json_text) else "ccl"
    if 'save_triggered' not in st.session_state:
        st.session_state.save_triggered = False
    if 'editor_version' not in st.session_state:
        st.session_state.editor_version = 0

    status = st.empty()
    col1, col2 = st.columns([1, 1], gap="small")
    st.markdown("""
        <style>
            [data-testid="column"] {
                flex: 1 1 calc(50% - 0.5rem);
                min-width: calc(50% - 0.5rem);
            }
            .stApp {
                padding: 0.5rem !important;
            }
            .block-container {
                padding: 0.5rem !important;
                max-width: 100% !important;
            }
        </style>
    """, unsafe_allow_html=True)

    def save_file(content, path):
        try:
            with open(path, 'w') as f:
                f.write(content)
            st.success(f"File saved successfully to {path}")
            return True
        except Exception as e:
            st.error(f"Failed to save file: {e}")
            return False

    with col1:
        st.subheader("CCL Editor")
        response_dict = code_editor(
            st.session_state.ccl_text,
            key = "ccl_editor",
            allow_reset = True,
            lang = "plain_text",
            height = [24, 24],
            shortcuts = "vscode",
            theme = "dark",
            buttons = code_buttons,
            options = {
                "animatedScroll": True,
                "showLineNumbers": True,
                "tabSize": 4,
                "enableBasicAutocompletion": True,
                "enableLiveAutocompletion": True
            }
        )
        if response_dict.get("type","") and response_dict.get("text", "") != st.session_state.ccl_text:
            ccl_input = response_dict.get("text", "").strip()
            try:
                st.session_state.json_text = dumps_json(ccl_to_dict(ccl_input), indent=4)
                st.session_state.ccl_text = ccl_from_dict(loads_json(st.session_state.json_text))
                st.session_state.active_editor = "ccl"
                st.session_state.save_triggered = True
                st.success(f"JSON code updated. {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            except Exception as e:
                st.error("Invalid CCL code. Please check your syntax.")

    with col2:
        st.subheader("JSON Editor")
        response_dict = code_editor(
            st.session_state.json_text,
            key = "json_editor",
            allow_reset = True,
            lang = "json",
            height = [24, 24],
            shortcuts = "vscode",
            theme = "dark",
            buttons = code_buttons,
            options = {
                "animatedScroll": True,
                "showLineNumbers": True,
                "tabSize": 4,
                "enableAutoIndent": True,
                "enableBasicAutocompletion": True,
                "enableLiveAutocompletion": True
            }
        )
        if response_dict.get("type","") and response_dict.get("text", "") != st.session_state.json_text:
            json_input = response_dict.get("text", "").strip()
            try:
                st.session_state.json_text = dumps_json(loads_json(json_input), indent=4)
                st.session_state.ccl_text = ccl_from_dict(loads_json(json_input))
                st.session_state.active_editor = "json"
                st.session_state.save_triggered = True
                st.success(f"CCL code updated. {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            except Exception as e:
                st.error("Invalid JSON code. Please check your syntax.")

    # Save buttons
    save_col, save_as_col = st.columns([1, 1])
    with save_col:
        if st.button("Save"):
            content = st.session_state.json_text if st.session_state.active_editor == "json" else st.session_state.ccl_text
            if save_file(content, st.session_state.file_path):
                st.session_state.save_triggered = False

    with save_as_col:
        new_path = st.text_input("Save as...", value=st.session_state.file_path)
        if st.button("Save As"):
            content = st.session_state.json_text if st.session_state.active_editor == "json" else st.session_state.ccl_text
            if save_file(content, new_path):
                st.session_state.file_path = new_path
                st.session_state.save_triggered = False

    # Perform sync only on demand
    if st.session_state.save_triggered:
        st.session_state.save_triggered = False
        st.rerun()

def main():
    file_editor("test.json")

if __name__ == "__main__":
    main()
