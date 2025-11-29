import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Netflix Data Cleaning & Analysis", layout="wide")

st.title("📺 Netflix Data Cleaning, Analysis & Visualization (PDF Version)")

# -------------------------
# Load Dataset
# -------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/netflix1(1).csv")

df = load_data()

st.header("📌 Raw Dataset Preview")
st.dataframe(df.head())

# -------------------------
# Dataset Info (PDF Style)
# -------------------------
st.subheader("📊 Dataset Info")
st.write("Rows:", df.shape[0])
st.write("Columns:", df.shape[1])

buffer = []
df.info(buf=buffer.append)
st.text("\n".join(buffer))

# -------------------------
# CLEANING STEPS (PDF)
# -------------------------
st.header("🧹 Data Cleaning Steps (Based on PDF)")

# 1. Drop duplicates
before = df.shape[0]
df = df.drop_duplicates()
after = df.shape[0]
st.write(f"✔ Removed **{before - after} duplicates**")

# 2. Convert date_added to datetime
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
st.write("✔ Converted `date_added` to datetime")

# 3. Replace missing values with "Not Given"
df = df.fillna("Not Given")
st.write("✔ Missing values replaced with 'Not Given'")

# 4. Extract new date columns
df["year"] = df["date_added"].dt.year
df["month"] = df["date_added"].dt.month
df["day"] = df["date_added"].dt.day
st.write("✔ Extracted year, month, day from date")

# -------------------------
# EDA (PDF)
# -------------------------
st.header("📈 Exploratory Data Analysis (PDF Version)")

# 1. Movies vs TV Shows
st.subheader("1️⃣ Movie vs TV Show Distribution")
type_counts = df["type"].value_counts()

col1, col2 = st.columns(2)
with col1:
    st.bar_chart(type_counts)

with col2:
    fig, ax = plt.subplots()
    ax.pie(type_counts, labels=type_counts.index, autopct="%.0f%%")
    st.pyplot(fig)

# 2. Ratings Distribution
st.subheader("2️⃣ Ratings Distribution")

fig, ax = plt.subplots(figsize=(10, 4))
sns.countplot(data=df, x="rating", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# 3. Top 10 Countries
st.subheader("3️⃣ Top 10 Countries with Most Content")

top_countries = df["country"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_countries.index, y=top_countries.values, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# 4. Monthly Releases
st.subheader("4️⃣ Monthly Releases (Movies vs TV Shows)")

movies_month = df[df["type"] == "Movie"]["month"].value_counts().sort_index()
shows_month = df[df["type"] == "TV Show"]["month"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(10, 5))
plt.plot(movies_month.index, movies_month.values, label="Movies")
plt.plot(shows_month.index, shows_month.values, label="TV Shows")
plt.legend()
plt.xticks(range(1, 13))
plt.grid(True)
st.pyplot(fig)

# 5. Yearly Releases
st.subheader("5️⃣ Yearly Releases")

movies_year = df[df["type"] == "Movie"]["year"].value_counts().sort_index()
shows_year = df[df["type"] == "TV Show"]["year"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(10, 5))
plt.plot(movies_year.index, movies_year.values, label="Movies")
plt.plot(shows_year.index, shows_year.values, label="TV Shows")
plt.legend()
plt.grid(True)
st.pyplot(fig)

# 6. Movie Genres
st.subheader("6️⃣ Top 10 Movie Genres")

movie_genre = df[df["type"] == "Movie"].groupby("listed_in").size().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=movie_genre.index, y=movie_genre.values, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# 7. TV Show Genres
st.subheader("7️⃣ Top 10 TV Show Genres")

tv_genre = df[df["type"] == "TV Show"].groupby("listed_in").size().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=tv_genre.index, y=tv_genre.values, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# 8. Top Directors
st.subheader("8️⃣ Top 15 Directors")

top_directors = df["director"].value_counts().head(15)

fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(x=top_directors.index, y=top_directors.values, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

st.success("🎉 EDA Completed Successfully! (Matches PDF St)")
