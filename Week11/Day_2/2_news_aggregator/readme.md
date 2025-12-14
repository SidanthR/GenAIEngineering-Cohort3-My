pip install fastapi uvicorn streamlit

cd Day_2\2_news_aggregator

<!-- run fastapi server -->
python news_api.py 

<!-- check the api server is running -->
localhost:9321/docs

<!-- run streamlit frontend server -->
streamlit run news_app.py