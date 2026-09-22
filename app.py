import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/search"


st.set_page_config(
    page_title="Semantic Search Engine",
    page_icon="🔎",
    layout="wide"
)


# -----------------------------
# Header
# -----------------------------

st.title("🔎 Semantic Search Engine")

st.write(
    "Search documents using semantic similarity with "
    "Sentence Transformers and ChromaDB."
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("Search Settings")

top_k = st.sidebar.slider(
    "Number of results",
    min_value=1,
    max_value=5,
    value=5
)

st.sidebar.divider()

st.sidebar.subheader("System Information")

st.sidebar.write("**Embedding Model**")
st.sidebar.code("all-MiniLM-L6-v2")

st.sidebar.write("**Vector Database**")
st.sidebar.code("ChromaDB")

st.sidebar.write("**Backend**")
st.sidebar.code("FastAPI")

st.sidebar.write("**Frontend**")
st.sidebar.code("Streamlit")

st.sidebar.write("**Chunking**")
st.sidebar.code("Paragraph-based")

st.sidebar.write("**Documents**")
st.sidebar.write("3")

st.sidebar.write("**Chunks**")
st.sidebar.write("8")


# -----------------------------
# Search
# -----------------------------

query = st.text_input(
    "Search your documents",
    placeholder="e.g. What is SQL used for?"
)


if st.button("🔍 Search", use_container_width=True):

    if not query.strip():

        st.warning("Please enter a search query.")

    else:

        with st.spinner("Searching documents..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "query": query,
                        "top_k": top_k
                    }
                )

                response.raise_for_status()

                data = response.json()

                st.subheader(
                    f"Top {len(data['results'])} Results"
                )

                for result in data["results"]:

                    st.markdown(
                        f"### {result['rank']}. "
                        f"{result['source']}"
                    )

                    st.write(result["text"])

                    col1, col2 = st.columns(2)

                    with col1:
                        st.caption(
                            f"Distance: "
                            f"{result['distance']:.4f}"
                        )

                    with col2:
                        st.caption(
                            "Smaller distance = more similar"
                        )

                    st.divider()

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the FastAPI server. "
                    "Make sure FastAPI is running on port 8000."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"API request failed: {e}"
                )


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "Semantic Search Engine • "
    "Sentence Transformers + ChromaDB + FastAPI + Streamlit"
)

st.divider()

st.subheader("📊 Retrieval Evaluation")

st.write(
    "The retrieval system was evaluated using 10 labelled queries "
    "and Precision@5."
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Paragraph-based Precision@5",
        "0.54"
    )

with col2:
    st.metric(
        "Fixed-size Precision@5",
        "0.54"
    )

st.caption(
    "Both chunking strategies achieved the same Precision@5 "
    "on the current evaluation dataset."
)