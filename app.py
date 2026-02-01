import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


@st.cache_data
def load_data():
    try:
        file_path=os.path.join(os.path.dirname(__file__),"mr_mrs_asa_dashboard.xlsx")
        dfs=pd.read_excel(file_path,sheet_name=None)
        return dfs
    except FileNotFoundError:
        st.error("Excel fie not found! Please ensure 'mr_mrs_asa_dashboard.xlsx' is in the same folder.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()
dfs=load_data()
st.set_page_config(page_title="Mr & Mrs ASA Dashboard", layout="wide")
#header and tabs
st.title("Mr & Mrs ASA Dashboard")
tabs= st.tabs(
    ["Data View","Scoring","Leaderboard","Finance & Insights"]
)
# Data view
with tabs[0]:
    st.header("📊 Data View")
    st.write("Browse and explore all data sheets in the system.")
    
    st.divider()
    
    sheet_names = list(dfs.keys())
    
    # Better layout with columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_sheet = st.selectbox("📋 Choose a sheet to view:", sheet_names)
    
    with col2:
        # Show sheet info
        row_count = len(dfs[selected_sheet])
        col_count = len(dfs[selected_sheet].columns)
        st.metric("📏 Rows", row_count)
    
    st.divider()
    
    # Sheet descriptions
    sheet_descriptions = {
        "Participants": "👥 All contestants participating in the competition",
        "Segments": "🎭 Different competition rounds and categories",
        "Scores": "🎯 Judge scores for each contestant per segment",
        "Revenue": "💰 Income sources and amounts",
        "Expenses": "💸 Expense categories and spending",
        "Tickets": "🎟️ Ticket sales information"
    }
    
    # Show description if available
    if selected_sheet in sheet_descriptions:
        st.info(f"ℹ️ {sheet_descriptions[selected_sheet]}")
    
    search_term = st.text_input("🔎 Search in this sheet", placeholder="Enter text to filter rows...")
    
    if search_term:
        # Filter dataframe based on search term (searches all columns)
        filtered_df = dfs[selected_sheet][
            dfs[selected_sheet].astype(str).apply(
                lambda row: row.str.contains(search_term, case=False).any(), axis=1
            )
        ]
        st.info(f"Found {len(filtered_df)} rows matching '{search_term}'")
        st.dataframe(filtered_df, use_container_width=True, height=400)
    else:
        st.dataframe(dfs[selected_sheet], use_container_width=True, height=400)
    st.divider()
    
    # Show column info in an expander
    with st.expander("�Column Details"):
        col_info = pd.DataFrame({
            "Column Name": dfs[selected_sheet].columns,
            "Data Type": dfs[selected_sheet].dtypes.values,
            "Non-Null Count": dfs[selected_sheet].count().values,
            "Null Count": dfs[selected_sheet].isnull().sum().values
        })
        st.dataframe(col_info, hide_index=True, use_container_width=True)
    
    # Download option
    st.divider()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # Convert dataframe to CSV for download
        csv = dfs[selected_sheet].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv,
            file_name=f"{selected_sheet}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
   
#Scoring
with tabs[1]:
    st.header("🎯 Scoring System")
    st.write("Enter judge scores for each segment. Scores range from 0-10.")
    
    st.divider()

    # Import tables and merge
    segments_df = dfs["Segments"]
    
    # Better segment selector with container
    col1, col2 = st.columns([2, 1])
    with col1:
        segment_choice = st.selectbox("📋 Choose a Competition Segment", segments_df["Segment_Name"])
    with col2:
        st.metric("Current Segment", segment_choice)

    selected_segment_id = segments_df.loc[
        segments_df["Segment_Name"] == segment_choice, "Segment_Id"
    ].values[0]
    
    scores_df = dfs["Scores"]
    scores_for_segment = scores_df[scores_df["Segment_Id"] == selected_segment_id]    

    participants_df = dfs["Participants"]
    merged_df = participants_df[["Contestant_No", "Name", "Category"]].merge(
        scores_for_segment[["Contestant_No", "Judge_1", "Judge_2", "Judge_3", "Average_Score"]], 
        on="Contestant_No", how="left"
    )
    mr_df = merged_df[merged_df["Category"] == "Mr"]
    mrs_df = merged_df[merged_df["Category"] == "Mrs"]

    

    st.divider()

    # Input Total Scores with better styling
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👨 Mr ASA Contestants")
        mr_edit = st.data_editor(
            mr_df,
            column_config={
                "Contestant_No": st.column_config.NumberColumn("No.", disabled=True),
                "Name": st.column_config.TextColumn("Name", disabled=True),
                "Category": st.column_config.TextColumn("Category", disabled=True),
                "Judge_1": st.column_config.NumberColumn("Judge 1", min_value=0, max_value=10, step=0.1),
                "Judge_2": st.column_config.NumberColumn("Judge 2", min_value=0, max_value=10, step=0.1),
                "Judge_3": st.column_config.NumberColumn("Judge 3", min_value=0, max_value=10, step=0.1),
                "Average_Score": st.column_config.NumberColumn("Average", disabled=True, format="%.2f"),
            },
            hide_index=True,
            use_container_width=True
        )
     
    with col2:
        st.subheader("👩 Mrs ASA Contestants")
        mrs_edit = st.data_editor(
            mrs_df,
            column_config={
                "Contestant_No": st.column_config.NumberColumn("No.", disabled=True),
                "Name": st.column_config.TextColumn("Name", disabled=True),
                "Category": st.column_config.TextColumn("Category", disabled=True),
                "Judge_1": st.column_config.NumberColumn("Judge 1", min_value=0, max_value=10, step=0.1),
                "Judge_2": st.column_config.NumberColumn("Judge 2", min_value=0, max_value=10, step=0.1),
                "Judge_3": st.column_config.NumberColumn("Judge 3", min_value=0, max_value=10, step=0.1),
                "Average_Score": st.column_config.NumberColumn("Average", disabled=True, format="%.2f"),
            },
            hide_index=True,
            use_container_width=True
        )

    # Calculate average_score for each contestant per segment
    mrs_edit["Average_Score"] = mrs_edit[["Judge_1","Judge_2","Judge_3"]].mean(axis=1)
    mr_edit["Average_Score"] = mr_edit[["Judge_1","Judge_2","Judge_3"]].mean(axis=1)

    st.divider()

    # Update button with better styling
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💾 Update Scores", type="primary", use_container_width=True):
            updated_scores = pd.concat([mr_edit, mrs_edit], ignore_index=True)
            updated_scores = updated_scores[["Contestant_No", "Judge_1", "Judge_2", "Judge_3", "Average_Score"]]
            updated_scores["Segment_Id"] = selected_segment_id

            # Remove old scores for this segment from the Scores DataFrame
            scores_df = dfs["Scores"]
            scores_df = scores_df[scores_df["Segment_Id"] != selected_segment_id]

            # Append the new data with the updated scores
            dfs["Scores"] = pd.concat([scores_df, updated_scores], ignore_index=True)

            # Save the updated data to the Excel file
            try:
                file_path=os.path.join(os.path.dirname(__file__),"mr_mrs_asa_dashboard.xlsx")
                with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                    for sheet_name, df in dfs.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                st.success("✅ Scores updated successfully!")
                st.balloons()  # Fun celebration effect!
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error saving data: {e}")
#Leaderboard
with tabs[2]:
    st.title("🏆 Leaderboard")
    st.write("Real-time rankings based on cumulative scores across all segments.")
    
    st.divider()

    # Load Data
    participants_df = dfs["Participants"]
    segments_df = dfs["Segments"]
    scores_df = dfs["Scores"]

    # Merge all three dataframes
    first_merge = scores_df.merge(segments_df, on="Segment_Id", how="left")
    merged = first_merge.merge(participants_df, on="Contestant_No", how="left")

    # Split the merged Data
    mr_leaderboard = merged[merged["Category"] == "Mr"]
    mrs_leaderboard = merged[merged["Category"] == "Mrs"]

    # Calculate the Total Score Separately
    mr_leaderboard = mr_leaderboard.groupby(["Contestant_No", "Name", "Category"])["Average_Score"].sum().reset_index()
    mrs_leaderboard = mrs_leaderboard.groupby(["Contestant_No", "Name", "Category"])["Average_Score"].sum().reset_index()

    # Sort Separately
    mr_leaderboard = mr_leaderboard.sort_values("Average_Score", ascending=False)
    mrs_leaderboard = mrs_leaderboard.sort_values("Average_Score", ascending=False)

    # Rank them
    mr_leaderboard["Rank"] = mr_leaderboard["Average_Score"].rank(method="dense", ascending=False).astype(int)
    mrs_leaderboard["Rank"] = mrs_leaderboard["Average_Score"].rank(method="dense", ascending=False).astype(int)
    
    # Display side by side
    col1, col2 = st.columns(2)
    
    # Display Mr ASA Leaderboard
    with col1:
        st.subheader("👨 Mr ASA Leaderboard")
        
        if mr_leaderboard.empty:
            st.info("No scores recorded yet for Mr ASA contestants.")
        else:
            for idx, row in mr_leaderboard.iterrows():
                rank = row["Rank"]
                name = row["Name"]
                score = row["Average_Score"]

                if rank == 1:
                    st.markdown(f"### 🥇 **{name}**")
                    st.markdown(f"**Score: {score:.2f}**")
                elif rank == 2:
                    st.markdown(f"### 🥈 **{name}**")
                    st.markdown(f"**Score: {score:.2f}**")
                elif rank == 3:
                    st.markdown(f"### 🥉 **{name}**")
                    st.markdown(f"**Score: {score:.2f}**")
                else:
                    st.markdown(f"**{rank}.** {name} — {score:.2f}")
                
                st.divider()

    # Display Mrs ASA Leaderboard
    with col2:
        st.subheader("👩 Mrs ASA Leaderboard")
        
        if mrs_leaderboard.empty:
            st.info("No scores recorded yet for Mrs ASA contestants.")
        else:
            for idx, row in mrs_leaderboard.iterrows():
                rank = row["Rank"]
                name = row["Name"]
                score = row["Average_Score"]

                if rank == 1:
                    st.markdown(f"### 🥇 **{name}**")
                    st.markdown(f"**Score: {score:.2f}**")
                elif rank == 2:
                    st.markdown(f"### 🥈 **{name}**")
                    st.markdown(f"**Score: {score:.2f}**")
                elif rank == 3:
                    st.markdown(f"### 🥉 **{name}**")
                    st.markdown(f"**Score: {score:.2f}**")
                else:
                    st.markdown(f"**{rank}.** {name} — {score:.2f}")
                
                st.divider()
    
    st.divider()
    
    # Optional: Show detailed stats
    with st.expander("📊 View Detailed Statistics"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Mr ASA Full Rankings**")
            st.dataframe(
                mr_leaderboard[["Rank", "Name", "Average_Score"]].rename(columns={"Average_Score": "Total Score"}),
                hide_index=True,
                use_container_width=True
            )
        with col2:
            st.write("**Mrs ASA Full Rankings**")
            st.dataframe(
                mrs_leaderboard[["Rank", "Name", "Average_Score"]].rename(columns={"Average_Score": "Total Score"}),
                hide_index=True,
                use_container_width=True
            )
#Finance and Insights
with tabs[3]:
    st.title("💰 Finance & Insights")
    st.write("Financial overview including revenue, expenses, and net profit/loss.")
    
    # Load data
    revenue_df = dfs["Revenue"]
    expenses_df = dfs["Expenses"]
    
    # Calculate totals
    Total_Revenue = revenue_df.loc[revenue_df["Source"] == "Total_Revenue", "Amount"].values[0]
    Total_Expenses = expenses_df.loc[expenses_df["Category"] == "Total_Expenses", "Amount"].values[0]
    net_profit_loss = Total_Revenue - Total_Expenses
    
    # Display key metrics at top using st.metric
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💵 Total Revenue", f"${Total_Revenue:,.2f}")
    with col2:
        st.metric("💸 Total Expenses", f"${Total_Expenses:,.2f}")
    with col3:
        if net_profit_loss >= 0:
            st.metric("✅ Net Profit", f"${net_profit_loss:,.2f}")
        else:
            st.metric("⚠️ Net Loss", f"${abs(net_profit_loss):,.2f}")
    
    st.divider()
    
    # Revenue and Expenses side by side
    col1, col2 = st.columns(2)
    
    
    # Revenue Section
    with col1:
        st.subheader("📊 Revenue Breakdown")
        chart_df = revenue_df[revenue_df["Source"] != "Total_Revenue"]
        chart_df=chart_df[chart_df["Amount"]>0]
        
        if not chart_df.empty:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(chart_df["Amount"], labels=chart_df["Source"], autopct='%1.1f%%', startangle=90)
            ax.set_title("Revenue Distribution")
            st.pyplot(fig)
        else:
            st.info("No revenue data to display")
        
        # Detailed breakdown
        st.write("**Details:**")
        all_revenue=revenue_df[revenue_df["Source"] != "Total_Revenue"]
        for idx, row in all_revenue.iterrows():
            st.write(f"• {row['Source']}: ${row['Amount']:,.2f}")
    
    # Expenses Section
    with col2:
        st.subheader("📉 Expenses Breakdown")
        chart_df = expenses_df[expenses_df["Category"] != "Total_Expenses"]
        chart_df= chart_df[chart_df["Amount"]>0]
        
        if not chart_df.empty:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(chart_df["Amount"], labels=chart_df["Category"], autopct='%1.1f%%', startangle=90)
            ax.set_title("Expense Distribution")
            st.pyplot(fig)
        else:
            st.info("No expense data to display")
        
        # Detailed breakdown
        st.write("**Details:**")
        all_expenses=expenses_df[expenses_df["Category"]!= "Total_Expenses"]
        for idx, row in all_expenses.iterrows():
            st.write(f"• {row['Category']}: ${row['Amount']:,.2f}")
    
    
    





   