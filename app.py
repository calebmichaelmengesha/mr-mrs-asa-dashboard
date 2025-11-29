import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    dfs=pd.read_excel("mr_mrs_asa_dashboard.xlsx", sheet_name=None)
    return dfs
dfs=load_data()
st.set_page_config(page_title="Mr & Mrs ASA Dashboard", layout="wide")
#header and tabs
st.title("Mr & Mrs ASA Dashboard")
tabs= st.tabs(
    ["Data View","Scoring","Leaderboard","Finance & Insights"]
)
# Data view
with tabs[0]:
    st.write("this is data view")
    sheet_names=list(dfs.keys())
    selected_sheet=st.selectbox("Choose a sheet to view:",sheet_names)
    st.dataframe(dfs[selected_sheet], use_container_width=True)
   
#Scoring
with tabs[1]:
    #import tables and merge
    st.header("Scores")

    # Import tables and merge
    segments_df = dfs["Segments"]
    segment_choice = st.selectbox("Choose a segment", segments_df["Segment_Name"])

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

    # Input Total Scores
    st.subheader("Mr ASA")
    mr_edit = st.data_editor(
        mr_df,
        column_config={
            "Judge_1": st.column_config.NumberColumn("Judge 1", min_value=0, max_value=10, step=0.1),
            "Judge_2": st.column_config.NumberColumn("Judge 2", min_value=0, max_value=10, step=0.1),
            "Judge_3": st.column_config.NumberColumn("Judge 3", min_value=0, max_value=10, step=0.1),
        },
        num_rows="dynamic"
    )
     
    st.subheader("Mrs ASA")
    mrs_edit = st.data_editor(
        mrs_df,
        column_config={
            "Judge_1": st.column_config.NumberColumn("Judge 1", min_value=0, max_value=10, step=0.1),
            "Judge_2": st.column_config.NumberColumn("Judge 2", min_value=0, max_value=10, step=0.1),
            "Judge_3": st.column_config.NumberColumn("Judge 3", min_value=0, max_value=10, step=0.1),
        },
        num_rows="dynamic"
    )

    # Calculate average_score for each contestant per segment
    mrs_edit["Average_Score"] = mrs_edit[["Judge_1","Judge_2","Judge_3"]].mean(axis=1)
    mr_edit["Average_Score"] = mr_edit[["Judge_1","Judge_2","Judge_3"]].mean(axis=1)

    # Update the scores sheet on Excel
    if st.button("Update New Score"):
        updated_scores = pd.concat([mr_edit, mrs_edit], ignore_index=True)
        updated_scores = updated_scores[["Contestant_No", "Judge_1", "Judge_2", "Judge_3", "Average_Score"]]
        updated_scores["Segment_Id"] = selected_segment_id

        # Remove old scores for this segment from the Scores DataFrame
        scores_df = dfs["Scores"]
        scores_df = scores_df[scores_df["Segment_Id"] != selected_segment_id]

        # Append the new data with the updated scores
        dfs["Scores"] = pd.concat([scores_df, updated_scores], ignore_index=True)

        # Save the updated data to the Excel file
        with pd.ExcelWriter("mr_mrs_asa_dashboard.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            for sheet_name, df in dfs.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        st.success("Scores updated successfully!")
#Leaderboard
with tabs[2]:
    st.title("Leaderboard")
    st.write("This is the leaderboard for the contestants")

    # Load Data
    participants_df = dfs["Participants"]
    segments_df = dfs["Segments"]
    scores_df = dfs["Scores"]

    # Merge all three dataframes
    first_merge = scores_df.merge(segments_df, on="Segment_Id", how="left")
    merged = first_merge.merge(participants_df, on="Contestant_No", how="left")

    #Split the merged Data
    mr_leaderboard=merged[merged["Category"]=="Mr"]
    mrs_leaderboard=merged[merged["Category"]=="Mrs"]

    #Calculate the Total Score Separately
    mr_leaderboard=mr_leaderboard.groupby(["Contestant_No","Name","Category"])["Average_Score"].sum().reset_index()
    mrs_leaderboard=mrs_leaderboard.groupby(["Contestant_No","Name","Category"])["Average_Score"].sum().reset_index()

    #Sort Separately
    mr_leaderboard=mr_leaderboard.sort_values("Average_Score", ascending=False)
    mrs_leaderboard=mrs_leaderboard.sort_values("Average_Score", ascending=False)

    #Rank them
    mr_leaderboard["Rank"]=mr_leaderboard["Average_Score"].rank(method="dense", ascending=False).astype(int)
    mrs_leaderboard["Rank"]=mrs_leaderboard["Average_Score"].rank(method="dense", ascending=False).astype(int)
    # Display Mr ASA Leaderboard
    st.subheader("Mr ASA Leaderboard")
    for idx, row in mr_leaderboard.iterrows():
        rank = row["Rank"]
        name = row["Name"]
        score = row["Average_Score"]

        if rank == 1:
            st.markdown(f"🥇 **{rank}. {name} — {score:.1f}**")
        elif rank == 2:
            st.markdown(f"🥈 **{rank}. {name} — {score:.1f}**")
        elif rank == 3:
            st.markdown(f"🥉 **{rank}. {name} — {score:.1f}**")
        else:
            st.markdown(f"{rank}. {name} — {score:.1f}")

    # Display Mrs ASA Leaderboard
    st.subheader("Mrs ASA Leaderboard")
    for idx, row in mrs_leaderboard.iterrows():
        rank = row["Rank"]
        name = row["Name"]
        score = row["Average_Score"]

        if rank == 1:
            st.markdown(f"🥇 **{rank}. {name} — {score:.1f}**")
        elif rank == 2:
            st.markdown(f"🥈 **{rank}. {name} — {score:.1f}**")
        elif rank == 3:
            st.markdown(f"🥉 **{rank}. {name} — {score:.1f}**")
        else:
            st.markdown(f"{rank}. {name} — {score:.1f}")


#Finance and Insights
with tabs[3]:
    st.title("Finance & Insights")
    st.write("This section gives financial insight including total revenue, total expanses, and net profit/loss.")

    #Load the Tickets and Expenses DataFrames
    tickets_df=dfs["Tickets"]
    expenses_df=dfs["Expenses"]
    revenue_df=dfs["Revenue"]

    #Display Total Revenue
    col1,col2=st.columns([1,1])
    with col1:
        st.subheader("Total Revenue Breakdown")
        for idx,row in revenue_df.iterrows():
            source=row["Source"]
            amount=row["Amount"]
            st.write(f"**{source}: ${amount:.2f}**")
    #Pie Chart
    with col2:

        if st.button("Show Pie Chart for Revenue"):
            #Creates a new data fram where total_revenue is removed, because that will disrupt the percentages in the pie chart
            chart_df = revenue_df[revenue_df["Source"]!= "Total_Revenue"]

            #This is the Pie chart
            fig,ax=plt.subplots()
            ax.pie(chart_df["Amount"], labels=chart_df["Source"],autopct='%1.1f%%')
            ax.set_title("Revenue Distribution")
            st.pyplot(fig)

    #Display Total Expenses
    #First load the data
    expenses_df=dfs["Expenses"]
    Col1,Col2=st.columns([1,1])
    with Col1:
        st.subheader("Total ExpensesBreakdown")
        for idx,row in expenses_df.iterrows():
            category=row["Category"]
            amount=row["Amount"]
            st.write(f"**{category}: {amount}**")
    #Pie Chart
    with Col2:

        if st.button("Show Pie Chart for Expenses"):
            #Creates a new data fram where total_expenses is removed, because that will disrupt the percentages in the pie chart
            chart_df = expenses_df[expenses_df["Category"]!= "Total_Expenses"]

            #This is the Pie chart
            fig,ax=plt.subplots()
            ax.pie(chart_df["Amount"], labels=chart_df["Category"],autopct='%1.1f%%')
            ax.set_title("Expense Breakdown")
            st.pyplot(fig)

    #Calculcate Net Profit/Loss
    Total_Revenue=revenue_df.loc[revenue_df["Source"]=="Total_Revenue","Amount"].values[0]
    Total_Expenses=expenses_df.loc[expenses_df["Category"]=="Total_Expenses","Amount"].values[0]
    net_profit_loss = Total_Revenue - Total_Expenses

    #Display New Profit/Loss
    st.subheader("Net Profit/Loss")
    if net_profit_loss >=0:
        st.markdown(f"**Net Profit: ${net_profit_loss:.2f}**")
    else:
        st.markdown(f"**Net Loss: ${abs(net_profit_loss):.2f}**")
    
    





   