from PIL import Image
import streamlit as st
import base64
import os
import pandas as pd
import plotly.express as px

st.markdown('<h1 style="text-align: center;">Uber Dashboard Page</h1>', unsafe_allow_html=True)

# Page ko wapiss Home pahe me le jane ke leya #
if st.button("⬅ Back to Home", key="back_home_dash"): 
    st.switch_page("Home.py")

# data set#
df = pd.read_csv(r"D:\ubar dash\UBAR\Ubar Row.csv")

st.dataframe(df) 

import streamlit as st

# ---- CSS for KPI cards ----
st.markdown("""
<style>
.kpi-card {
    background-color: #0e1117;
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.35);
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---- First row: 4 KPIs ----
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        '<div class="kpi-card">'
        '<p style="font-size:12px; font-weight:600;"> 🚕Total🚕  Bookings</p>'
        '<h4>148,767</h4>'
        '</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="kpi-card">'
        '<p style="font-size:12px; font-weight:600;">✅ Completed Rides</p>'
        '<h4>92,551</h4>'
        '</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<div class="kpi-card">'
        '<p style="font-size:12px; font-weight:600;">👤 Customer Cancel %</p>'
        '<h4>7.06%</h4>'
        '</div>',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        '<div class="kpi-card">'
        '<p style="font-size:12px; font-weight:600;">🚖 Driver Cancel %</p>'
        '<h4>18.15%</h4>'
        '</div>',
        unsafe_allow_html=True
    )


# ---- Second row: 3 KPIs ----
col5, col6, col7 = st.columns(3)
    
with col5:
    st.markdown(
        '<div class="kpi-card"><p style="font-size:12px; font-weight:600;">⏳ Avg VTAT</p><h4>8.46 min</h4></div>',
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        '<div class="kpi-card"><p style="font-size:12px; font-weight:600;">💰 Total Booking Value</p><h4>₹ 51,846,183</h4></div>',
        unsafe_allow_html=True
    )

with col7:
    st.markdown(
        '<div class="kpi-card"><p style="font-size:12px; font-weight:600;">⭐ Avg Driver Rating</p><h4>4.2</h4></div>',
        unsafe_allow_html=True
    )



st.sidebar.title("🔍 Filters")

vehicle_type = st.sidebar.multiselect(
    "🚗 Vehicle Type",
    options=sorted(df["Vehicle Type"].dropna().unique()),
    default=sorted(df["Vehicle Type"].dropna().unique())
)

# Filter lagao
filtered_df = df[df["Vehicle Type"].isin(vehicle_type)]

# Subheader for filtered data
st.subheader("📄 Filtered Data")

# Show filtered table
st.dataframe(filtered_df, use_container_width=True)

# ---------------- KPI CALCULATIONS ----------------
total_bookings = filtered_df["Booking ID"].nunique()

completed_rides = filtered_df[
    filtered_df["Booking Status"] == "Completed"
]["Booking ID"].nunique()

customer_cancel = filtered_df["Cancelled Rides by Customer"].sum()
driver_cancel = filtered_df["Cancelled Rides by Driver"].sum()

customer_cancel_pct = (customer_cancel / total_bookings * 100) if total_bookings > 0 else 0
driver_cancel_pct = (driver_cancel / total_bookings * 100) if total_bookings > 0 else 0

avg_vtat = filtered_df["Avg VTAT"].dropna().mean()
total_booking_value = filtered_df["Booking Value"].dropna().sum()
avg_driver_rating = filtered_df["Driver Ratings"].dropna().mean()

# ---------------- KPI DISPLAY ----------------
st.subheader("📊 Key Metrics")

# 4 KPIs in first row
col1, col2, col3, col4 = st.columns(4)
col1.metric("🚕 Total Bookings", total_bookings)
col2.metric("✅ Completed Rides", completed_rides)
col3.metric("👤 Customer Cancel %", f"{customer_cancel_pct:.2f}%")
col4.metric("🚖 Driver Cancel %", f"{driver_cancel_pct:.2f}%")

# 3 KPIs in second row
col5, col6, col7 = st.columns(3)
col5.metric("⏳ Avg VTAT", f"{avg_vtat:.2f} min")
col6.metric("💰 Total Booking Value", f"₹ {total_booking_value:,.0f}")
col7.metric("⭐ Avg Driver Rating", f"{avg_driver_rating:.1f}") 




# ===================== SIDEBAR : NEW SLIDER FILTER (CHARTS ONLY) =====================
st.sidebar.subheader("🎚️ Chart Filters")

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Booking Value'] = pd.to_numeric(df['Booking Value'], errors='coerce')
df['Ride Distance'] = pd.to_numeric(df['Ride Distance'], errors='coerce')
df['Avg VTAT'] = pd.to_numeric(df['Avg VTAT'], errors='coerce')
df['Avg CTAT'] = pd.to_numeric(df['Avg CTAT'], errors='coerce')
df['Driver Ratings'] = pd.to_numeric(df['Driver Ratings'], errors='coerce')
df['Customer Rating'] = pd.to_numeric(df['Customer Rating'], errors='coerce')

df_chart_base = df.dropna(subset=['Date'])

start_date, end_date = st.sidebar.slider(
    "📅 Date Range (Charts)",
    min_value=df_chart_base['Date'].min().date(),
    max_value=df_chart_base['Date'].max().date(),
    value=(df_chart_base['Date'].min().date(), df_chart_base['Date'].max().date())
)

chart_df = df_chart_base[
    (df_chart_base['Date'].dt.date >= start_date) &
    (df_chart_base['Date'].dt.date <= end_date)
]

# ===================== BOOKING STATUS BAR =====================
st.subheader("Booking Status Distribution")
status_counts = chart_df['Booking Status'].value_counts().reset_index()
status_counts.columns = ['Booking_Status', 'Number_of_bookings']

fig = px.bar(
    status_counts, x='Booking_Status', y='Number_of_bookings',
    color='Booking_Status', text='Number_of_bookings',
    template='plotly_dark'
)
st.plotly_chart(fig, use_container_width=True) 
st.markdown("""
The booking status distribution reveals customer preferences and operational efficiency. A high number of completed bookings indicates good service reliability, while cancellations highlight areas for improvement in customer satisfaction and driver availability.
""")


# ===================== DAILY BOOKINGS LINE =====================
st.subheader("Daily Booking Trends")
daily_bookings = chart_df.groupby(chart_df['Date'].dt.date).size().reset_index(name='Booking_Count')

fig = px.line(
    daily_bookings, x='Date', y='Booking_Count',
    
    markers=True, template='plotly_dark'
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
Analyzing daily booking trends helps identify peak demand periods and seasonal patterns. This insight allows for better resource allocation, marketing strategies, and service improvements to enhance customer experience and operational efficiency.
""")

# ===================== VEHICLE TYPE COUNT =====================
st.subheader("Bookings by Vehicle Type")
vehicle_counts = chart_df['Vehicle Type'].value_counts().reset_index()
vehicle_counts.columns = ['Vehicle_Type', 'Number_of_bookings']

fig = px.bar(
    vehicle_counts, x='Vehicle_Type', y='Number_of_bookings',
    title='🚗 Bookings by Vehicle Type',
    text='Number_of_bookings', template='plotly_dark'
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
Understanding bookings by vehicle type provides insights into customer preferences and market trends. This information can guide fleet management, marketing strategies, and service offerings to better meet customer needs and optimize operational efficiency.
""")

# ===================== VEHICLE vs STATUS ===================== 
st.subheader("Vehicle Type vs Booking Status")
vehicle_status_counts = chart_df.groupby(
    ['Vehicle Type', 'Booking Status']
).size().reset_index(name='Ride_Count')

fig = px.bar(
    vehicle_status_counts, x='Vehicle Type', y='Ride_Count',
    color='Booking Status', barmode='stack',
    template='plotly_dark'
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
Analyzing the relationship between vehicle type and booking status helps identify which vehicles are more likely to complete rides versus those that are frequently canceled. This insight can inform fleet management decisions, improve customer satisfaction, and optimize resource allocation.
""")

# ===================== AVG RIDE DISTANCE =====================
st.subheader("Avg Ride Distance by Vehicle Type")
avg_distance = chart_df.groupby('Vehicle Type')['Ride Distance'].mean().reset_index()

fig = px.bar(
    avg_distance, x='Vehicle Type', y='Ride Distance',
    text='Ride Distance', template='plotly_dark'
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
Examining the average ride distance by vehicle type provides insights into customer travel patterns and preferences. This information can help optimize fleet composition, improve service offerings, and enhance overall customer satisfaction by aligning vehicle types with typical ride distances.
""")



# ===================== PAYMENT SHARE =====================
payment_share = chart_df.groupby('Payment Method')['Booking Value'].sum().reset_index()

fig = px.pie(
    payment_share, names='Payment Method', values='Booking Value',
    title='💰 Payment Method Share',
    hole=0.3, template='plotly_dark'
)
st.plotly_chart(fig, use_container_width=True)



# ===================== BOX : CUSTOMER RATINGS =====================
df_clean = chart_df.dropna(subset=['Customer Rating'])

fig = px.box(
    df_clean, x='Vehicle Type', y='Customer Rating',
    color='Vehicle Type',
    title='📦 Customer Ratings by Vehicle Type',
    template='plotly_dark'
)
st.plotly_chart(fig, use_container_width=True)


# ===================== booking status distribution =====================
st.markdown("<h3 style='text-align: center;'>Booking Status Distribution (Filtered Data)</h3>", unsafe_allow_html=True)
status_counts = (
    filtered_df['Booking Status']
    .value_counts()
    .reset_index()
)

status_counts.columns = ['Booking_Status', 'Number_of_bookings']

# 🔽 Plotly Bar Chart (Premium Colors)
fig = px.bar(
    status_counts,
    x='Booking_Status',
    y='Number_of_bookings',
    color='Booking_Status',
    template='plotly_dark',
    text='Number_of_bookings'
)
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Count of Bookings'
)
st.plotly_chart(fig)
st.markdown("""
Analyzing the booking status distribution in the filtered data provides insights into customer behavior and service efficiency. A higher proportion of completed bookings indicates effective service delivery, while cancellations highlight areas for improvement in customer satisfaction and operational processes.
""")

#==================== booking value by vehicle type ====================
st.markdown("<h3 style='text-align: center;'>Booking Value by Vehicle Type</h3>", unsafe_allow_html=True)
df['Booking Value'] = pd.to_numeric(df['Booking Value'], errors='coerce')

# Aggregate total booking value by vehicle type
vehicle_revenue = (
    df.groupby('Vehicle Type')['Booking Value']
      .sum()
      .reset_index(name='Total_Booking_Value')
)
# Bar Chart
fig = px.bar(
    vehicle_revenue,
    x='Vehicle Type',
    y='Total_Booking_Value',
    color='Vehicle Type',
    text='Total_Booking_Value',
    template='plotly_dark'
)
st.plotly_chart(fig)
st.markdown("""
Analyzing booking value by vehicle type provides insights into revenue generation across different segments. This information can guide strategic decisions in fleet management, marketing efforts, and service offerings to maximize profitability and meet customer demand effectively.
""")    


#===================== AVERAGE VTAT OVER TIME =====================
st.markdown("<h3 style='text-align: center;'>Average VTAT Over Time</h3>", unsafe_allow_html=True)
avg_vtat_time = (
    df.groupby(df['Date'].dt.date)['Avg VTAT']
      .mean()
      .reset_index(name='Average_VTAT')
)
fig = px.line(
    avg_vtat_time,
    x='Date',
    y='Average_VTAT',
    
markers=True,
    template='plotly_dark'
)

st.plotly_chart(fig)
st.markdown("""
Monitoring the average VTAT (Vehicle Turnaround Time) over time helps identify trends in operational efficiency and service quality. A decreasing VTAT indicates improved performance, while increases may signal potential issues that need to be addressed to enhance customer satisfaction and optimize resource utilization.
""") 


#===================== AVERAGE CTAT OVER TIME =====================

st.markdown("<h3 style='text-align: center;'>Average CTAT Over Time</h3>",unsafe_allow_html=True)

avg_ctat_time = (
    df.groupby(df['Date'].dt.date)['Avg CTAT']
      .mean()
      .reset_index(name='Average_CTAT')
)
fig = px.line(
    avg_ctat_time,
    x='Date',
    y='Average_CTAT',
    markers=True,
    template='plotly_dark'
)
st.plotly_chart(fig)
st.markdown("""
Monitoring the average CTAT (Customer Turnaround Time) over time provides insights into customer service efficiency and satisfaction levels. A decreasing CTAT indicates improved responsiveness, while increases may highlight areas for improvement in service delivery and customer experience.
""")    