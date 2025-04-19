import streamlit as st
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from pymongo import MongoClient
from datetime import datetime
# from dotenv import load_dotenv
# import os
from youtube_transcript_api import YouTubeTranscriptApi

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
MONGODB_URI = st.secrets["MONGODB_URI"]

# Set up your API keys and MongoDB connection
genai.configure(api_key=GOOGLE_API_KEY)
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# load_dotenv()  # Load variables from .env

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# MongoDB Atlas connection setup
client_mongo = MongoClient(MONGODB_URI)  # MongoDB connection URI
# client_mongo = MongoClient(os.getenv("MONGODB_URI"))
db = client_mongo.summaries_db  # Database name
summaries_collection = db.summaries  # Collection name

prompt = """You are a video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text along with headline in 4 words given here:  """

# Save summary with headline to MongoDB
def save_summary(youtube_url, headline, summary):
    document = {
        "youtube_url": youtube_url,
        "headline": headline,  # Store the headline
        "summary": summary,
        "timestamp": datetime.now()
    }
    summaries_collection.insert_one(document)

# Fetch the latest summaries from MongoDB based on user selection
def get_latest_saved_summaries(limit):
    results = summaries_collection.find().sort("timestamp", -1).limit(limit)
    return list(results)

# Search summaries in MongoDB by headline
def search_summaries_by_headline(search_query):
    results = summaries_collection.find({
        "headline": {"$regex": search_query, "$options": "i"}  # Case-insensitive search by headline
    })
    return list(results)

# Get the transcript data from YouTube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

# Get the summary and headline based on the YouTube transcript
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + transcript_text)
    
    # Assuming that the model responds with both headline and summary (you may need to adjust based on actual model behavior)
    lines = response.text.split("\n", 1)
    headline = lines[0] if len(lines) > 0 else "No headline available"
    summary = lines[1] if len(lines) > 1 else "No summary available"

    return headline, summary


# Convert text to audio using ElevenLabs
def generate_audio(response_text):
    try:
        audio_stream = client.text_to_speech.convert(
            text=response_text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        print("audio is ready... now playing")
        # play(audio_stream)
        audio_bytes = b"".join(audio_stream)  # Convert generator to bytes
        return audio_bytes
    except Exception as e:
        raise RuntimeError(f"Failed to generate audio: {e}")
    
    

# Streamlit app setup
st.set_page_config(page_title="🎙️ Podcast Summary App", layout="centered")
st.title("🎙️ Podcast Summarizer")
st.subheader("Summarize & Search Any Podcast Instantly")

# Search functionality for headlines
search_query = st.text_input("🔍 Search by Headline:")
if search_query:
    st.subheader(f"Searching for summaries with headline containing: {search_query}")
    results = search_summaries_by_headline(search_query)
    if results:
        st.subheader(f"Found {len(results)} result(s):")
        for result in results:
            st.markdown(f"### [Video URL]({result['youtube_url']})")
            st.write(f"**Headline:** {result['headline']}")
            st.write(f"**Summary:** {result['summary']}")
            st.write(f"Timestamp: {result['timestamp']}")
    else:
        st.warning("No summaries found matching your search.")

# Show Latest Saved Summaries Button & Select the number of summaries
with st.expander("Show Latest Saved Summaries"):
    # Add a slider to select the number of summaries to retrieve
    num_summaries = st.slider("Select number of latest summaries to show", 1, 20, 10)  # Default: 10, min: 1, max: 20
    
    if st.button("📑 Show Latest Saved Summaries"):
        with st.spinner(f"⏳ Fetching the latest {num_summaries} saved summaries..."):
            try:
                saved_summaries = get_latest_saved_summaries(num_summaries)
                if saved_summaries:
                    st.subheader(f"Showing the latest {num_summaries} saved summaries:")
                    for summary in saved_summaries:
                        st.markdown(f"### [Video URL]({summary['youtube_url']})")
                        st.write(f"**Headline:** {summary['headline']}")
                        st.write(f"**Summary:** {summary['summary']}")
                        st.write(f"Timestamp: {summary['timestamp']}")
                else:
                    st.warning("No saved summaries found.")
            except Exception as e:
                st.error(f"❌ Error fetching saved summaries: {str(e)}")

# Paste YouTube Link
youtube_link = st.text_input("🔗 Paste the podcast Link Below:")

if youtube_link:
    try:
        video_id = youtube_link.split("v=")[1]
        thumbnail_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"
        st.image(thumbnail_url, use_column_width=True, caption="🎬 Video Preview")
    except IndexError:
        st.error("❌ Please enter a valid YouTube video link.")

# Generate Summary with Headline and Optionally Save
if st.button("📝 Generate Detailed Summary"):
    with st.spinner("⏳ Extracting transcript and summarizing..."):
        try:
            transcript_text = extract_transcript_details(youtube_link)
            if transcript_text:
                headline, summary = generate_gemini_content(transcript_text, prompt)
                
                
                
                # Show the summary
                st.success("✅ Summary Generated!")
                st.markdown("### 📄 Headline:")
                st.markdown(f"**{headline}**")  # Display the headline
                st.markdown("### 📄 Detailed Summary:")
                st.markdown(summary)
                save_summary(youtube_link, headline, summary)  # Save the headline and summary
                st.success("✅ Summary has been saved successfully!")

                # Ask the user if they want to save the summary using a radio button
                # save_permission = st.radio(
                #     "Would you like to save this summary?",
                #     options=["Yes", "No"]
                # )

                # # Check if the user selected "Yes"
                # if save_permission == "Yes":
                #     # Provide a Save button for final confirmation
                #     if st.button("💾 Save Summary"):
                #         save_summary(youtube_link, headline, summary)  # Save the headline and summary
                #         st.success("✅ Summary has been saved successfully!")
                # else:
                #     st.info("ℹ️ Summary will not be saved.")
                    
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Generate Voice Summary
if st.button("🎧 Generate Voice Summary"):
    with st.spinner("🎙️ Processing audio summary..."):
        try:
            # Extract transcript text from the YouTube link
            transcript_text = extract_transcript_details(youtube_link)
            
            if transcript_text:
                # Generate the headline and summary using the Gemini model
                headline, summary = generate_gemini_content(transcript_text, prompt)
                
                if summary:
                    # Combine headline and summary
                    content_to_audio = f"{headline}\n\n{summary}"
                    
                    # Generate audio for the combined content (headline + summary)
                    audio_data = generate_audio(content_to_audio)
                    
                    # Display success message and audio player
                    st.markdown("### 📄 Headline:")
                    st.markdown(f"**{headline}**")  # Display the headline
                    st.markdown("### 📄 Detailed Summary:")
                    st.markdown(summary)
                    st.success("✅ Summary has been saved successfully!")
                    st.success("✅ Voice Summary Ready!")

                    st.markdown("### 🔊 Play Voice Summary Below:")
                    st.audio(audio_data, format="audio/mp3")
                    
                else:
                    st.warning("⚠️ No summary generated.")
            else:
                st.warning("⚠️ No transcript available.")
        except Exception as e:
            st.error(f"❌ Error generating voice summary: {str(e)}")

st.markdown("---")
st.caption("✨ Built with ❤️ using Streamlit, Google Gemini, and ElevenLabs.")
