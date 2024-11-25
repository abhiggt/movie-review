import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

OMDB_API_KEY = "1f176288"
OMDB_URL = "http://www.omdbapi.com/"

# App Title
st.title("Movie Review ")
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Search Movies", "Submit Reviews", "Analytics"])

# Session State for storing reviews
if "reviews" not in st.session_state:
    st.session_state["reviews"] = []

# Page 1: Search Movies
if page == "Search Movies":
    st.header("🔍 Search Movies")
    movie_name = st.text_input("Enter movie name:")
    
    if st.button("Search"):
        if movie_name:
            params = {"t": movie_name, "apikey": OMDB_API_KEY}
            response = requests.get(OMDB_URL, params=params)
            movie_data = response.json()
            
            if movie_data.get("Response") == "True":
                # Display movie details
                st.image(movie_data["Poster"], width=200)
                st.subheader(movie_data["Title"])
                st.write(f"**Genre:** {movie_data['Genre']}")
                st.write(f"**Released:** {movie_data['Released']}")
                st.write(f"**Plot:** {movie_data['Plot']}")
            else:
                st.error("Movie not found! Try another name.")
        else:
            st.warning("Please enter a movie name.")

# Page 2: Submit Reviews
elif page == "Submit Reviews":
    st.header(" Write Review")
    movie_title = st.text_input("Movie Title:")
    review = st.text_area("Your Review:")
    rating = st.slider("Rating", 1, 10, 5)
    
    if st.button("Submit Review"):
        if movie_title and review:
            st.session_state["reviews"].append({"Movie": movie_title, "Review": review, "Rating": rating})
            st.success("Review submitted!")
        else:
            st.warning("Please fill in all fields.")

    # Show recent reviews
    if st.session_state["reviews"]:
        st.subheader("Recent Reviews")
        reviews_df = pd.DataFrame(st.session_state["reviews"])
        st.table(reviews_df)

# Page 3: Analytics
elif page == "Analytics":
    st.header("Review Analytics")
    
    if st.session_state["reviews"]:
        reviews_df = pd.DataFrame(st.session_state["reviews"])
        
        # Average ratings per movie
        avg_ratings = reviews_df.groupby("Movie")["Rating"].mean().sort_values(ascending=False)
        st.subheader("Average Ratings by Movie")
        st.bar_chart(avg_ratings)

        # Most Reviewed Movies
        review_counts = reviews_df["Movie"].value_counts()
        st.subheader("Most Reviewed Movies")
        st.bar_chart(review_counts)
    else:
        st.warning("No reviews submitted yet!")
