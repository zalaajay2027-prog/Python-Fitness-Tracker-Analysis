import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Page Configuration

st.set_page_config(
    page_title="Fitness Tracker",
    page_icon="🏃",
    layout="wide"
)


# Title

st.title(" Fitness Tracker & Activity Data Analysis")
st.write("Analyze fitness activities, duration and calories burned.")


# Load Csv

try:
    df = pd.read_csv("fitness_data.csv")

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"])

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    st.success("Fitness data loaded successfully!")


except FileNotFoundError:
    st.error("fitness_data.csv not found. Please keep CSV in the same folder as app.py.")
    st.stop()


# Data Preview


st.header(" Fitness Dataset")

st.dataframe(df, use_container_width=True)


# Metrics


total_activities = len(df)

total_calories = df["calories_burned"].sum()

total_duration = df["duration_(minutes)"].sum()

average_calories = df["calories_burned"].mean()

average_duration = df["duration_(minutes)"].mean()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Activities", total_activities)

with col2:
    st.metric("Total Calories", f"{total_calories:.0f}")

with col3:
    st.metric("Total Duration", f"{total_duration:.0f} min")

with col4:
    st.metric("Average Calories", f"{average_calories:.2f}")


# Summary

st.header(" Activity Summary")

summary = df.groupby("activity_type").agg({
    "duration_(minutes)": "sum",
    "calories_burned": "sum"
}).reset_index()

st.dataframe(summary, use_container_width=True)

# Activity  Filter

st.header(" Filter Activities")

activities = ["All"] + sorted(df["activity_type"].unique().tolist())

selected_activity = st.selectbox(
    "Select Activity",
    activities
)

if selected_activity == "All":
    filtered_df = df
else:
    filtered_df = df[df["activity_type"] == selected_activity]

st.dataframe(filtered_df, use_container_width=True)


# Bar Chart

st.header(" Total Duration by Activity")

duration_summary = df.groupby("activity_type")["duration_(minutes)"].sum()

fig1, ax1 = plt.subplots()

duration_summary.plot(
    kind="bar",
    ax=ax1
)

ax1.set_xlabel("Activity Type")
ax1.set_ylabel("Total Duration (Minutes)")
ax1.set_title("Total Duration by Activity")

plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig1)


# Line Chart

st.header(" Calories Burned Over Time")

fig2, ax2 = plt.subplots()

for activity in df["activity_type"].unique():

    activity_data = df[df["activity_type"] == activity]

    ax2.plot(
        activity_data["date"],
        activity_data["calories_burned"],
        marker="o",
        label=activity
    )

ax2.set_xlabel("Date")
ax2.set_ylabel("Calories Burned")
ax2.set_title("Calories Burned Over Time")

ax2.legend()

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig2)


# Pie Chart

st.header(" Activity Distribution")

activity_counts = df["activity_type"].value_counts()

fig3, ax3 = plt.subplots()

ax3.pie(
    activity_counts,
    labels=activity_counts.index,
    autopct="%1.1f%%"
)

ax3.set_title("Activity Type Distribution")

st.pyplot(fig3)


# Correlation Heatmap

st.header(" Correlation Heatmap")

corr = df[
    ["duration_(minutes)", "calories_burned"]
].corr()

fig4, ax4 = plt.subplots()

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax4
)

ax4.set_title("Duration vs Calories Correlation")

st.pyplot(fig4)



# Footer


st.success(" Fitness Tracker Dashboard Completed!")