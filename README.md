# Podcast Summarizer App

This Streamlit application allows users to summarize YouTube podcast transcripts using Google's Gemini AI model and optionally generate an audio summary using ElevenLabs. It also provides functionality to save and search summaries in a MongoDB database.

## Features

* **Summarize YouTube Podcasts:** Simply paste the YouTube podcast link, and the app will extract the transcript, generate a concise summary with a headline using Gemini, and display it.
* **Save Summaries:** The generated summaries (including the YouTube URL, headline, and the summary text) are saved to a MongoDB Atlas database for later retrieval.
* **Search by Headline:** Users can search through the saved summaries by entering keywords from the headline. The app will display all matching summaries.
* **View Latest Summaries:** An expandable section allows users to view a selected number of the most recently saved summaries.
* **(Optional) Generate Voice Summary:** A button (currently commented out in the provided code) allows users to generate an audio version of the headline and summary using ElevenLabs.

## Technologies Used

* **Streamlit:** For building the interactive web application interface.
* **Google Gemini (via `google.generativeai`):** For generating the podcast summaries and headlines.
* **ElevenLabs (via `elevenlabs`):** (Optional) For text-to-speech functionality to create audio summaries.
* **PyMongo:** For interacting with the MongoDB Atlas database to save and retrieve summaries.
* **YouTube Transcript API (`youtube_transcript_api`):** For extracting transcripts from YouTube videos.
* **Requests (`requests`):** (In the original, commented-out proxy code) For making HTTP requests, potentially for proxy management.
* **Regular Expressions (`re`):** For extracting the YouTube video ID from the URL.
* **Datetime (`datetime`):** For recording the timestamp when summaries are saved.
* **Environment Variables (`os`):** For securely managing API keys and the MongoDB connection URI.

## Setup and Deployment

### Prerequisites

* Python 3.6 or higher
* API keys for:
    * Google Gemini API
    * ElevenLabs API (if you want to use the voice summary feature)
* MongoDB Atlas account and connection URI

### Local Installation

1.  **Clone the repository** (if you have the code in a repository).
2.  **Install the required Python libraries:**
    ```bash
    pip install streamlit google-generativeai elevenlabs pymongo youtube-transcript-api requests python-dotenv
    ```
3.  **Set up environment variables:**
    * Create a `.env` file in the same directory as your Streamlit app.
    * Add your API keys and MongoDB URI to the `.env` file:
        ```
        GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
        ELEVENLABS_API_KEY="YOUR_ELEVENLABS_API_KEY"
        MONGODB_URI="YOUR_MONGODB_CONNECTION_URI"
        # Optional: WEBSHARE_PROXY="YOUR_WEBSHARE_PROXY_URL"
        ```
    * Make sure to load these environment variables in your Streamlit app (although the provided code directly uses `os.environ.get`).

4.  **Run the Streamlit app:**
    ```bash
    streamlit run your_app_name.py
    ```
    (Replace `your_app_name.py` with the name of your Python file).

### Deployment on Render

1.  **Prepare your Streamlit app files:**
    * Your Python script (`.py` file).
    * A `requirements.txt` file listing all the Python dependencies. You can generate this using:
        ```bash
        pip freeze > requirements.txt
        ```
2.  **Connect your repository to Render:**
    * Go to [Render](https://render.com/) and create a new Web Service.
    * Connect your Git repository (e.g., GitHub, GitLab, Bitbucket) that contains your Streamlit app.
3.  **Configure your Render Web Service:**
    * **Build Command:** `pip install -r requirements.txt`
    * **Start Command:** `streamlit run your_app_name.py` (Replace with your file name)
    * **Environment Variables:** Add the following environment variables in the Render dashboard's "Environment" section:
        * `GOOGLE_API_KEY`: Your Google Gemini API key.
        * `ELEVENLABS_API_KEY`: Your ElevenLabs API key.
        * `MONGODB_URI`: Your MongoDB connection URI.
        * **(Optional)** `WEBSHARE_PROXY`: Your Webshare proxy URL (if you intend to use a proxy for transcript extraction).
4.  **Deploy:** Save the configuration, and Render will automatically build and deploy your application.

### Potential Issues on Deployment (e.g., Render)

* **Network Restrictions:** Deployed environments might have stricter network policies that could interfere with accessing external APIs (like YouTube or proxy services).
* **Resource Limits:** Cloud platforms often have resource limits (CPU, memory, execution time). Ensure your app doesn't exceed these limits, especially during transcript extraction and AI processing.
* **Proxy Configuration:** If you are using a proxy, ensure that the environment variable is correctly set on the deployment platform and that the proxy service is accessible from the platform's network. The provided code in the prompt was attempting a complex rotating proxy mechanism, which might be less reliable in a deployed environment. The simplified approach of using a single proxy via an environment variable (as suggested in previous responses) is generally more stable for deployment.

## Usage

1.  Open the deployed Streamlit application in your web browser.
2.  Paste the URL of the YouTube podcast you want to summarize into the "🔗 Paste the podcast Link Below:" text input.
3.  Click the "📝 Generate Detailed Summary" button.
4.  The app will display the video preview, extract the transcript, generate a headline and summary, and save it to the MongoDB database.
5.  You can search for previously summarized podcasts using the "🔍 Search by Headline:" text input.
6.  Expand the "Show Latest Saved Summaries" section to view the most recent summaries.
7.  **(If enabled)** Click the "🎧 Generate Voice Summary" button to generate an audio version of the summary.

## Notes

* The voice summary feature is currently commented out in the provided code. To enable it, uncomment the `generate_audio` function and the "🎧 Generate Voice Summary" button section. Ensure your ElevenLabs API key is correctly configured.
* Consider implementing more robust error handling and user feedback mechanisms for a better user experience.
* For production deployments, it's crucial to manage API keys and sensitive information securely using environment variables or secrets management provided by your hosting platform.


