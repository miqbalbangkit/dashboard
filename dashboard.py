import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def create_sum_order_df(df):
    sum_order_df = df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_order_df

def create_casual_df(df):
    casual_df = df["casual"].sum()
    return casual_df

def create_registered_df(df):
    registered_df = df["registered"].sum()
    return registered_df

all_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    st.image("dicoding.png")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]
            
sum_order_df = create_sum_order_df(main_df)
casual_df = create_casual_df(main_df)
registered_df = create_registered_df(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Daily Share')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_share = sum_order_df.cnt.sum()
    st.metric("Total Share", value=total_share)
 

fig, ax = plt.subplots (figsize=(24, 5))
 
sns.barplot(
    y="cnt", 
    x="hr",
    data=sum_order_df.sort_values(by="cnt", ascending=False),
    ax=ax
)

ax.set_title("Number of Total Customer", loc="center", fontsize=60)
ax.set_xlabel("Hour", fontsize=30)
ax.set_ylabel(None)
ax.tick_params(axis = 'y', labelsize=30)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)




fig, ax = plt.subplots()
ax.set_title("Casual vs Registered Users Proportion", loc="center", fontsize=15)
labels = ["Casual", "Registered"]
sizes = [casual_df, registered_df]
colors = ["#e4604e", "#3d9c73"]
ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=180, colors=colors)
ax.axis("equal") 

st.pyplot(fig)