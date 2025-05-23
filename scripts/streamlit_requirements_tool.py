import io  # Add to the top of your file if not already
import streamlit as st
import pandas as pd
import os

FILE_PATH = "/Users/rohanb/BPAOT/data/requirements.xlsx"

def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH)
    else:
        return pd.DataFrame(columns=["Requirement", "Pain Point", "Proposed Solution"])

def save_data(df):
    df.to_excel(FILE_PATH, index=False)

def main():
    st.set_page_config(page_title="BPAOT - Requirement Manager", layout="wide")
    st.title("📋 Business Requirement Manager (BPAOT)")
    
    df = load_data()

    # Tabs for organization
    tab1, tab2, tab3 = st.tabs(["➕ Add Requirement", "🔍 View/Search/Edit", "🗑️ Delete"])

    # ADD NEW
    with tab1:
        st.subheader("Add a New Requirement")
        with st.form("add_form"):
            req = st.text_input("Requirement")
            pain = st.text_input("Pain Point")
            sol = st.text_input("Proposed Solution")
            submitted = st.form_submit_button("Add Entry")
            if submitted:
                if req and pain and sol:
                    new_entry = {"Requirement": req, "Pain Point": pain, "Proposed Solution": sol}
                    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                    save_data(df)
                    st.success("✅ Entry added!")
                else:
                    st.warning("❗ All fields must be filled out.")

    # VIEW & EDIT
    with tab2:
        st.subheader("View / Search / Edit Requirements")
        with st.expander("📤 Export Data"):
            st.download_button(
                label="Download as CSV",
                data=df.to_csv(index=False),
                file_name="requirements.csv",
                mime="text/csv"
            )


            # Inside your "Export Data" section
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False, engine="openpyxl")
            excel_buffer.seek(0)

            st.download_button(
                label="Download as Excel",
                data=excel_buffer,
                file_name="requirements.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


        search = st.text_input("Search by keyword:")
        filtered_df = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)] if search else df.copy()
        
        if len(filtered_df):
            edited_df = st.data_editor(filtered_df, use_container_width=True, num_rows="dynamic")
            if st.button("💾 Save Changes"):
                # Match edited_df rows to df using index
                df.update(edited_df)
                save_data(df)
                st.success("✅ Changes saved.")
        else:
            st.info("No matching results.")

    # DELETE
    with tab3:
        st.subheader("Delete a Requirement")
        if df.empty:
            st.info("No data to delete.")
        else:
            row_to_delete = st.selectbox("Select row to delete", df["Requirement"])
            if st.button("🗑️ Delete Selected"):
                df = df[df["Requirement"] != row_to_delete]
                save_data(df)
                st.success(f"✅ Deleted: {row_to_delete}")

    # USER STORY GENERATION TAB
    tab4 = st.tabs(["📘 Generate User Stories"])[0]
    with tab4:
        st.subheader("Generate User Stories from Requirements")

        if df.empty:
            st.info("No data to generate stories.")
        else:
            user_stories = [
                f"As a user, I want to {row['Requirement'].lower()} because {row['Pain Point'].lower()}. Solution: {row['Proposed Solution']}."
                for _, row in df.iterrows()
            ]
            stories_text = "\n".join(user_stories)

            st.text_area("📖 Generated User Stories", stories_text, height=250)

            st.download_button(
                label="📥 Download User Stories (.txt)",
                data=stories_text,
                file_name="user_stories.txt",
                mime="text/plain"
            )




if __name__ == "__main__":
    main()
