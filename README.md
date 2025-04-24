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









#   YouTube Transcript Extractor with Rotating Proxies

This Python script is designed to extract transcripts from YouTube videos while employing rotating proxies to minimize the risk of IP address blocking. It leverages the `youtube-transcript-api` library and the `requests` library to achieve this.

##   Features

* **Transcript Extraction:** Retrieves transcripts from YouTube videos using the `youtube-transcript-api`.
* **Rotating Proxies:** Implements a mechanism to rotate through a list of proxies to avoid detection and blocking by YouTube.
* **Proxy Health Check:** Includes functionality to check the validity of proxies before using them, ensuring only working proxies are utilized.
* **Language Prioritization:** Attempts to fetch transcripts in preferred languages (English, English (India), Hindi) and falls back if those are not available.
* **Error Handling:** Provides robust error handling to manage potential issues during proxy connection, transcript retrieval, and language selection.
* **Proxy Verification Tools:** Contains code segments to explicitly verify proxy functionality and IP rotation.

##   Why Rotating Proxies?

When accessing web services like YouTube, especially from cloud environments or when making frequent requests, your IP address can be flagged and blocked. YouTube employs various anti-scraping mechanisms to protect its data and infrastructure. These mechanisms often involve:

* **IP Address Blocking:** If YouTube detects a large number of requests originating from a single IP address within a short period, it may temporarily or permanently block that IP address. This prevents further access to YouTube's services.
* **Rate Limiting:** YouTube may impose limits on the number of requests that can be made from a specific IP address within a given timeframe. Exceeding these limits can result in temporary blocks or errors.
* **CAPTCHAs:** YouTube may present CAPTCHAs to users whose behavior appears suspicious, requiring them to solve a challenge to prove they are human.

Rotating proxies help mitigate these issues by:

* **Distributing Requests:** By routing requests through different IP addresses, rotating proxies make it harder for YouTube to identify and block a single source.
* **Evading Rate Limits:** Distributing requests across multiple IPs can help stay below the rate limits imposed by YouTube.
* **Avoiding Detection:** Rotating proxies can make your requests appear more like normal user activity, reducing the likelihood of triggering anti-scraping measures.

##   Requirements

* Python 3.6 or higher
* Libraries:
    * `requests`
    * `youtube-transcript-api`

    You can install these using pip:

    ```bash
    pip install requests youtube-transcript-api
    ```

##   Setup

1.  **Install Python:** Ensure you have Python 3.6 or a later version installed on your system.
2.  **Install Libraries:** Use pip to install the required libraries:

    ```bash
    pip install requests youtube-transcript-api
    ```

3.  **Proxy Configuration:**

    * The script is designed to work with a list of HTTP/HTTPS proxies. You'll need to provide your own list of proxy URLs.
    * **Important:** The provided code snippet is configured for Webshare rotating proxies. You will need to replace the example proxy URL (`"http://uvmfwcbs-rotate:imui7uhheoxm@p.webshare.io:80"`) with your actual proxy URLs. If you have multiple proxies, add them to the `proxy_list`.
    * If your proxies require authentication, ensure the URL includes the username and password (e.g., `http://username:password@host:port`).

##   How It Works

1.  **Proxy List and Selection:**

    * The script maintains a list of proxy URLs (`proxy_list`).
    * The `get_working_proxy` function iterates through this list, attempting to connect to a test website (`https://ipv4.webshare.io/`) through each proxy.
    * It checks if the proxy returns a valid IP address. If it does, the proxy is considered working and its URL is returned.
    * If no working proxy is found, an exception is raised.

2.  **Monkey Patching `requests.get`:**

    * To transparently route all HTTP/HTTPS requests through the selected proxy, the script "monkey patches" the `requests.get` function.
    * It temporarily replaces the original `requests.get` with a custom `proxy_get` function.
    * The `proxy_get` function adds the proxy configuration to the keyword arguments of the original `requests.get` before calling it.

3.  **Transcript Retrieval:**

    * The `extract_transcript_details` function uses the `YouTubeTranscriptApi` to:
        * Get a list of available transcripts for the specified `video_id`.
        * Attempt to fetch the transcript in the preferred languages (English, English (India), Hindi).
        * If a transcript is successfully fetched, it concatenates the text segments and returns the full transcript text.
        * If no transcript is found in the preferred languages, it raises a `ValueError`.

4.  **Error Handling:**

    * The script includes `try...except...finally` blocks to handle potential errors during proxy checks, transcript retrieval, and network requests.
    * The `finally` block ensures that the original `requests.get` function is restored, regardless of whether an error occurred. This is crucial to avoid unintended side effects in other parts of your code.

##   Proxy Verification Tools (Included in the Code)

The provided code includes several segments designed to help you verify your proxy setup and ensure it's working as expected. These segments are primarily for debugging and troubleshooting.

1.  **Basic IP Check:**

    * This method uses `ifconfig.me` or `api.ipify.org` to retrieve the IP address seen by the server.
    * By comparing the IP address obtained with and without a proxy, you can confirm whether the proxy is being used.

    ```python
    import requests

    def check_ip_using_proxy():
        try:
            response = requests.get("[https://api.ipify.org?format=json](https://api.ipify.org?format=json)", proxies={
                "http": "YOUR_PROXY_URL",
                "https": "YOUR_PROXY_URL"
            })
            data = response.json()
            print(f"Current IP: {data['ip']}")
        except Exception as e:
            print(f"Error checking IP: {e}")

    def check_ip_without_proxy():
        try:
            response = requests.get("[https://api.ipify.org?format=json](https://api.ipify.org?format=json)")
            data = response.json()
            print(f"Current IP without proxy: {data['ip']}")
        except Exception as e:
            print(f"Error checking IP: {e}")

    check_ip_using_proxy()
    check_ip_without_proxy()
    ```

2.  **Proxy Status Check (for Webshare):**

    * If you're using Webshare, you can use their API to check the status of your proxies.
    * This involves making a request to the Webshare API with your API token.

    ```python
    import requests

    WEBSHARE_API_TOKEN = "YOUR_WEBSHARE_API_TOKEN"
    PROXY_URL = "[https://proxy.webshare.io/api/v2/proxy/list/](https://proxy.webshare.io/api/v2/proxy/list/)"

    headers = {
        "Authorization": f"Token {WEBSHARE_API_TOKEN}"
    }

    def check_proxy_status():
        try:
            response = requests.get(PROXY_URL, headers=headers)
            # Process the response to check proxy status
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    check_proxy_status()
    ```

3.  **IP Rotation Verification:**

    * To ensure your proxy is actually rotating IPs, you can make multiple requests to an IP-checking service with a short delay between them.
    * If the IP address changes with each request, the rotation is working.

    ```python
    import requests
    import time
    import random

    proxy_url = "YOUR_ROTATING_PROXY_URL"
    proxies = {"http": proxy_url, "https": proxy_url}

    def check_proxy_ip():
        try:
            response = requests.get("[http://httpbin.org/ip](http://httpbin.org/ip)", proxies=proxies, timeout=10)
            if response.status_code == 200:
                ip_data = response.json()
                print(f"✅ Proxy IP: {ip_data['origin']}")
            else:
                print(f"❌ Failed. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")

    for i in range(5):
        print(f"\n[Attempt {i + 1}]")
        check_proxy_ip()
        time.sleep(random.uniform(2, 5)) # Wait for potential IP rotation
    ```

**Important Notes on Proxy Verification:**

* Replace `"YOUR_PROXY_URL"` and other placeholders with your actual proxy details.
* The specific methods for checking proxy status and IP rotation might vary depending on your proxy provider. Refer to your provider's documentation.
* Use these verification tools responsibly and avoid making excessive requests that could overload the services.

##   Usage

1.  **Prepare the Script:**

    * Save the provided Python code as a `.py` file (e.g., `extract_youtube_transcript.py`).
    * **Configure your proxy settings** within the `extract_transcript_details` function.
    * **(Optional)** If you want to use the proxy verification code, uncomment and adapt the relevant sections.

2.  **Run the Script:**

    * Execute the script from the command line, providing the YouTube video ID as an argument (or modify the `if __name__ == "__main__":` block to hardcode the video ID).

    ```bash
    python extract_youtube_transcript.py
    ```

3.  **Output:**

    * The script will print the extracted transcript to the console.
    * It will also print debugging information about proxy checks, language availability, and any errors encountered.
    * If you've enabled the proxy verification code, you'll see its output as well.

##   Important Considerations

* **Proxy Reliability:** The effectiveness of this script heavily depends on the reliability of your proxies. Free proxies are often unstable and slow. Consider using a reputable paid proxy service for production use.
* **YouTube's Terms of Service:** Be mindful of YouTube's terms of service when using this script. Excessive or automated transcript retrieval might violate their policies. Use this script responsibly.
* **Error Handling:** The provided script includes basic error handling, but you might need to enhance it based on your specific requirements (e.g., logging errors, retrying failed requests).
* **Rate Limiting:** Even with rotating proxies, YouTube might still impose rate limits. Implement appropriate delays and error handling to manage rate limiting.
* **Maintenance:** YouTube's website structure and API behavior can change. You might need to update the script periodically to ensure it continues to work correctly.
* **Security:** If your proxy requires authentication, handle your credentials securely (e.g., using environment variables or secure configuration files) and avoid hardcoding them directly in the script.
* **Cloud Environments:** When deploying this script in cloud environments (e.g., AWS, Google Cloud, Azure), you are more likely to encounter IP blocking issues. Cloud providers often use shared IP address ranges, and YouTube might be more sensitive to requests originating from these ranges. Rotating proxies become even more critical in such scenarios.





