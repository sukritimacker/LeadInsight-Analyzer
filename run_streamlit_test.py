# For Data Manipulation
import pandas as pd
import numpy as np
from datetime import datetime as dt



import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import io

df = pd.read_excel("Telemarketing.xlsx", header=2)

df['Timestamp'] = df['Timestamp'].apply(lambda date_time: date_time[:-9])
df['Timestamp'] = df['Timestamp'].apply(lambda date_time: dt.strptime(date_time, '%Y/%m/%d %I:%M:%S %p'))
df['Day of Week'] = df['Timestamp'].dt.dayofweek
df['Time_Bucket'] = pd.cut(df['Timestamp'].dt.hour,
                            bins=[0, 12, 17, 24],
                            labels=['Morning', 'Noon', 'Evening'],
                            include_lowest=True,
                            right=False)

df['Picked the phone'] = df['Picked the phone'].replace({'Yes, but mentioned to call later': 'Yes'})
df['Reason Why Phone is not picked'] = df['Reason Why Phone is not picked'].replace({'not pickup the call ': 'Not Picked the Call'})

# ... (your other imports and data loading)

st.set_option('deprecation.showPyplotGlobalUse', False)


st.title("LeadInsight Analyser")

# Sidebar for user input if needed
# st.sidebar.header("User Input")

# Add user input widgets as needed (e.g., dropdowns, sliders, etc.)

# Visualizations
st.header("Painting the Story of Lead Engagements")

# Use st.pyplot() for Matplotlib plots
fig, ax = plt.subplots(figsize=(10, 7))
sns.countplot(x='City', hue='Picked the phone', data=df, palette='pastel', ax=ax)
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')
ax.set_xlabel('City')
ax.set_ylabel('Number of Calls Made')
ax.set_title('Picked phone by City')
ax.legend(title='Picked the phone', labels=['Not Picked', 'Picked'])

# Display the plot using Streamlit
st.pyplot(fig)