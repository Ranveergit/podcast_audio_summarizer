import streamlit as st
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from pymongo import MongoClient
from datetime import datetime
import requests
import re
from tenacity import retry, stop_after_attempt, wait_exponential
from youtube_transcript_api import YouTubeTranscriptApi
import random
import time
# import os  # Import the os module
# from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
# load_dotenv()

# Your API keys and MongoDB connection (from environment variables)
# GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
# ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
# MONGODB_URI = os.environ.get("MONGODB_URI")

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
MONGODB_URI = st.secrets["MONGODB_URI"]

# Check if the environment variables are set
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY is not set. Please set it as an environment variable or in a .env file.")
if not ELEVENLABS_API_KEY:
    raise EnvironmentError("ELEVENLABS_API_KEY is not set. Please set it as an environment variable or in a .env file.")
if not MONGODB_URI:
    raise EnvironmentError("MONGODB_URI is not set. Please set it as an environment variable or in a .env file.")


# Set up your API keys and MongoDB connection
genai.configure(api_key=GOOGLE_API_KEY)
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# MongoDB Atlas connection setup
client_mongo = MongoClient(MONGODB_URI)
db = client_mongo.summaries_db
summaries_collection = db.summaries

prompt = """You are a video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text along with headline in 4 words given here:  """

# Save summary with headline to MongoDB
def save_summary(youtube_url, headline, summary):
    document = {
        "youtube_url": youtube_url,
        "headline": headline,
        "summary": summary,
        "timestamp": datetime.now(),
    }
    summaries_collection.insert_one(document)

# Fetch the latest summaries from MongoDB based on user selection
def get_latest_saved_summaries(limit):
    results = summaries_collection.find().sort("timestamp", -1).limit(limit)
    return list(results)

# Search summaries in MongoDB by headline
def search_summaries_by_headline(search_query):
    results = summaries_collection.find({
        "headline": {"$regex": search_query, "$options": "i"},  # Case-insensitive search by headline
    })
    return list(results)

def extract_video_id(url):
    """
    Extracts the YouTube video ID from different URL formats.
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    """
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


# @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1000, max=5000))
# def extract_transcript_details(video_id):
#     """
#     Extracts transcript details from a YouTube video, using a rotating proxy
#     and User-Agent for each request to avoid IP blocking.
#     Args:
#         video_id (str): The YouTube video ID.
#     Returns:
#         str: The full transcript text, or None if no transcript is found or
#              an error occurs after multiple retries.
#     """
#     # Webshare proxy configuration
#     proxy_url = "http://uvmfwcbs-rotate:imui7uhheoxm@p.webshare.io:80"
#     # User-Agent list for rotation
#     user_agent_list = [
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
#         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0",
#         "Mozilla/5.0 (X11; Linux i686; rv:123.0) Gecko/20100101 Firefox/123.0",
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/123.0.2420.81 Safari/537.36",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Edge/123.0.2420.81 Safari/537.36",
#     ]

#     original_get = requests.get  # Store the original requests.get
    
#     # Initialize a counter for proxy rotation
#     proxy_counter = 0

#     def get_transcript_with_retry(video_id, current_proxy, num_retries=0):
#         """
#         Helper function to get transcript with retries within the function
#         """
#         nonlocal original_get
#         nonlocal proxy_counter # Use the nonlocal keyword to modify the global proxy_counter
#         try:
#             # Introduce a random delay before each request
#             time.sleep(random.uniform(2, 5))  # Simulate human behavior
#             user_agent = random.choice(user_agent_list) # Rotate User-Agent
#             def proxy_get(*args, **kwargs):
#                 kwargs["proxies"] = {"http": current_proxy, "https": current_proxy}
#                 kwargs["headers"] = {"User-Agent": user_agent}  # Set User-Agent
#                 return original_get(*args, **kwargs)

#             requests.get = proxy_get
#             # Get the IP address used for the request
#             ip_response = requests.get('https://api.ipify.org')
#             ip_address = ip_response.text
#             print(f"Request made from IP address: {ip_address}") # Print IP Address
#             transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
#             available_languages = [t.language_code for t in transcripts]
#             print(f"Available transcripts for video {video_id}: {available_languages}")
#             for lang in ["en", "en-IN", "hi"]:
#                 if lang in available_languages:
#                     transcript = transcripts.find_transcript([lang])
#                     transcript_data = transcript.fetch()
#                     full_transcript = " ".join([item.text for item in transcript_data])
#                     print(f"✅ Retrieved transcript for {lang} using proxy {current_proxy}")
#                     requests.get = original_get
#                     return full_transcript
#             requests.get = original_get
#             raise ValueError(
#                 f"No transcripts found in preferred languages. Available: {available_languages}"
#             )
#         except Exception as e:
#             requests.get = original_get
#             print(f"❌ Error retrieving transcript with proxy {current_proxy}: {e}")
#             if num_retries < 3:
#                 proxy_counter += 1
#                 next_proxy = f"{proxy_url}:{proxy_counter}"
#                 print(f"🔄 Retrying with proxy: {next_proxy}..")
#                 return get_transcript_with_retry(video_id, next_proxy, num_retries + 1)
#             else:
#                 raise  # Re-raise the last exception if all proxies failed

#     try:
#         transcript_text = get_transcript_with_retry(video_id, proxy_url)
#         return transcript_text

#     except Exception as e:
#         print(f"❌  All retries failed: {e}")
#         raise


def extract_transcript_details(video_id):
    """
    Extracts transcript details from a YouTube video, using a rotating proxy to avoid IP blocking.

    Args:
        video_id (str): The YouTube video ID.

    Returns:
        str: The full transcript text, or None if no transcript is found or an error occurs.
    """

    # Webshare proxy configuration (Add more proxies to this list for better rotation)
    proxy_list = [
        "http://uvmfwcbs-rotate:imui7uhheoxm@p.webshare.io:80",
        # "http://user2:pass2@host2:port2",  # Add more proxies here to rotate through
        # "http://user3:pass3@host3:port3",
    ]

    def get_working_proxy(proxies):
        """
        Checks if the proxies are working and returns a working proxy.
        Args:
            proxies (list): A list of proxy URLs
        Returns:
             str: A working proxy.
        """
        for proxy_url in proxies:
            try:
                print(f"ℹ️  Checking proxy: {proxy_url}")
                response = requests.get(
                    "https://ipv4.webshare.io/",
                    proxies={"http": proxy_url, "https": proxy_url},
                    timeout=5  # Added timeout
                )
                response.raise_for_status()
                response_text = response.text

                if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", response_text):
                    print(f"✅  Working proxy: {proxy_url}, IP: {response_text}")
                    return proxy_url
                else:
                    print(
                        f"❌  Proxy {proxy_url} did not return an IP address.  Response: {response_text}"
                    )

            except requests.exceptions.RequestException as e:
                print(f"❌  Proxy {proxy_url} failed: {e}")
        return None

    original_get = requests.get  # Store the original requests.get

    try:
        working_proxy = get_working_proxy(proxy_list)
        if not working_proxy:
            raise Exception("No working proxies available")

        def proxy_get(*args, **kwargs):
            kwargs["proxies"] = {"http": working_proxy, "https": working_proxy}
            return original_get(*args, **kwargs)

        requests.get = proxy_get  # Apply the monkey patch

        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        available_languages = [t.language_code for t in transcripts]
        print(f"Available transcripts for video {video_id}: {available_languages}")

        for lang in ["en", "en-IN", "hi"]:
            if lang in available_languages:
                try:
                    transcript = transcripts.find_transcript([lang])
                    transcript_data = transcript.fetch()
                    full_transcript = " ".join([item.text for item in transcript_data])
                    print(f"✅ Retrieved transcript for {lang}")
                    return full_transcript
                except Exception as e:
                    print(f"❌ Error retrieving transcript for {lang}: {e}")
        raise ValueError(
            f"No transcripts found in preferred languages. Available: {available_languages}"
        )

    except Exception as e:
        print(f"❌ Error during transcript extraction: {e}")
        return None  # Important:  Return None on error, don't just raise.
    finally:
        requests.get = original_get  # Restore the original requests.get



def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(prompt + transcript_text)
        lines = response.text.split("\n", 1)
        headline = lines[0] if len(lines) > 0 else "No headline available"
        summary = lines[1] if len(lines) > 1 else "No summary available"
        return headline, summary
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        st.error(f"❌ Error generating summary.")
        raise  # Re-raise to trigger retry






# def generate_audio(response_text):
#     try:
#         audio_stream = client.text_to_speech.convert(
#             text=response_text,
#             voice_id="JBFqnCBsd6RMkjVDRZzb",
#             model_id="eleven_multilingual_v2",
#             output_format="mp3_44100_128",
#         )
#         print("audio is ready... now playing")
#         audio_bytes = b"".join(audio_stream)  # Convert generator to bytes
#         return audio_bytes
#     except Exception as e:
#         print(f"❌ Error generating audio: {e}")
#         st.error(f"❌ Error generating audio.")
#         raise RuntimeError(f"Failed to generate audio: {e}")

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
    num_summaries = st.slider(
        "Select number of latest summaries to show", 1, 20, 10
    )  # Default: 10, min: 1, max: 20
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
        video_id = extract_video_id(youtube_link)
        thumbnail_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"
        st.image(thumbnail_url, use_column_width=True, caption="🎬 Video Preview")
    except IndexError:
        st.error("❌ Please enter a valid YouTube video link.")

# Generate Summary with Headline and Optionally Save
if st.button("📝 Generate Detailed Summary"):
    with st.spinner("⏳ Extracting transcript and summarizing..."):
        try:
            transcript_text = extract_transcript_details(video_id)
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
        except Exception as e:
            st.error(f"❌ Error: {str(e)}") # Show the last error

# # Generate Voice Summary
# if st.button("🎧 Generate Voice Summary"):
#     with st.spinner("🎙️ Processing audio summary..."):
#         try:
#             # Extract transcript text from the YouTube link
#             transcript_text = extract_transcript_details(video_id)
#             if transcript_text:
#                 # Generate the headline and summary using the Gemini model
#                 headline, summary = generate_gemini_content(transcript_text, prompt)
#                 if summary:
#                     # Combine headline and summary
#                     content_to_audio = f"{headline}\n\n{summary}"
#                     # Generate audio for the combined content (headline + summary)
#                     audio_data = generate_audio(content_to_audio)
#                     # Display success message and audio player
#                     st.markdown("### 📄 Headline:")
#                     st.markdown(f"**{headline}**")  # Display the headline
#                     st.markdown("### 📄 Detailed Summary:")
#                     st.markdown(summary)
#                     save_summary(youtube_link, headline, summary)
#                     st.success("✅ Summary has been saved successfully!")
#                     st.success("✅ Voice Summary Ready!")
#                     st.markdown("### 🔊 Play Voice Summary Below:")
#                     st.audio(audio_data, format="audio/mp3")
#                 else:
#                     st.warning("⚠️ No summary generated.")
#             else:
#                 st.warning("⚠️ No transcript available.")
#         except Exception as e:
#             st.error(f"❌ Error generating voice summary: {str(e)}") # Show the last error

st.markdown("---")
st.caption("✨ Built with ❤️ using Streamlit, Google Gemini, and ElevenLabs.")


