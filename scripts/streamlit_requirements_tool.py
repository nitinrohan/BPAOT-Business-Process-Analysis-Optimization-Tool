import io  # Add to the top of your file if not already
import streamlit as st
import pandas as pd
import os
import sqlite3
import matplotlib.pyplot as plt


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
    
        tab5 = st.tabs(["📊 Insights & SQL"])[0]

    with tab5:
        st.subheader("📈 SQL Insights & Analytics")

        # Connect to SQLite
        conn = sqlite3.connect("data/bpaot.db")
        cursor = conn.cursor()

        # 🔍 Show total records
        cursor.execute("SELECT COUNT(*) FROM requirements")
        total = cursor.fetchone()[0]
        st.metric(label="Total Requirements in Database", value=total)

        # 🔢 Most Common Words in Requirements
        st.markdown("### 🔤 Most Common Words in Requirements")

        df_db = pd.read_sql("SELECT * FROM requirements", conn)
        all_words = " ".join(df_db["requirement"].dropna().tolist()).lower().split()
        freq = pd.Series(all_words).value_counts().head(10)

        fig, ax = plt.subplots()
        freq.plot(kind='bar', ax=ax)
        st.pyplot(fig)

        # 💬 Custom SQL Query Tool
        st.markdown("### 💬 Run Custom SQL Query")
        user_query = st.text_area("Enter SQL Query (e.g., SELECT * FROM requirements LIMIT 5):")
        if user_query:
            try:
                result_df = pd.read_sql(user_query, conn)
                st.dataframe(result_df)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

        conn.close()

    tab6 = st.tabs(["📸 Post to Instagram"])[0]

    with tab6:
        st.subheader("Post Word Frequency Chart to Instagram")

        if st.button("📸 Post Now"):
            with st.spinner("Uploading to Instagram..."):
                result = os.system("python scripts/post_to_instagram.py")
            if result == 0:
                st.success("✅ Post published to Instagram!")
            else:
                st.error("❌ Failed to post to Instagram. Check credentials or network.")



if __name__ == "__main__":
    main()
