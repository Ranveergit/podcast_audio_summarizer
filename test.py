import requests
import time
import random

# def extract_transcript_details(video_id):
#     # Store the original requests.get method
#     original_get = requests.get

#     # Define a patched version of requests.get to route through the Webshare rotating proxy
#     def proxy_get(*args, **kwargs):
#         kwargs['proxies'] = {
#             "http": "http://uvmfwcbs-rotate:imui7uhheoxm@proxy.webshare.io:80",
#             "https": "http://uvmfwcbs-rotate:imui7uhheoxm@proxy.webshare.io:80"
#         }
#         return original_get(*args, **kwargs)

#     # Monkey patch requests.get
#     requests.get = proxy_get

#     try:
#         # List available transcripts for the video
#         transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

#         # Debugging: Print available languages
#         available_languages = [t.language_code for t in transcripts]
#         print(f"Available transcripts for video {video_id}: {available_languages}")

#         # Try fetching transcript in the following order: English, English (India), Hindi
#         for lang in ['en', 'en-IN', 'hi']:
#             if lang in available_languages:
#                 try:
#                     # Try to find the transcript for the language
#                     transcript = transcripts.find_transcript([lang])
#                     transcript_data = transcript.fetch()

#                     print(f"Checking transcript of {lang} ....")
#                     full_transcript = " ".join([getattr(item, "text", "") for item in transcript_data])
#                     print(f"Retrieved transcript for {lang} successfully")

#                     return full_transcript
#                 except Exception as e:
#                     print(f"Could not retrieve transcript for {lang}. Error: {e}")
#             else:
#                 print(f"Transcript for language {lang} not available in the video.")

#         # If no transcript was found in any of the preferred languages, raise an error
#         raise ValueError(
#             f"No available transcripts for the video in the preferred languages: "
#             f"from English, English-India, Hindi. Available languages: {available_languages}"
#         )

#     except Exception as e:
#         raise e  # Re-raise the error if something went wrong

#     finally:
#         # Restore the original requests.get method
#         requests.get = original_get

# # Webshare proxy credentials
# proxy_username = "uvmfwcbs-rotate"
# proxy_password = "imui7uhheoxm"
# proxy_url = f"http://{proxy_username}:{proxy_password}@proxy.webshare.io:80"

# proxies = {
#     "http": proxy_url,
#     "https": proxy_url
# }

# headers = {
#     "User-Agent": (
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#         "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
#     )
# }

# # Test rotating IP 5 times
# for i in range(5):
#     try:
#         # Test using ifconfig.me for IP check
#         response = requests.get("https://ifconfig.me/all.json", proxies=proxies, headers=headers, timeout=10)

#         print(f"[{i+1}] Raw response: {response.text}")
#         data = response.json()
#         print(f"[{i+1}] ✅ Current IP: {data.get('ip')}\n")

#     except Exception as e:
#         print(f"[{i+1}] ❌ Request failed: {e}")

#     time.sleep(random.uniform(2, 4))
# import requests
# requests.get(
#     "https://ipv4.webshare.io/",
#     proxies={
#         "http": "http://p.webshare.io:9999/",
#         "https": "http://p.webshare.io:9999/"
#     }
# ).text

# def check_ip_using_proxy():
#     # This will help you check the current IP being used by the proxy
#     try:
#         response = requests.get("https://api.ipify.org?format=json", proxies={
#             "http": "http://uvmfwcbs-rotate:imui7uhheoxm@p.webshare.io:80",
#             "https": "http://uvmfwcbs-rotate:imui7uhheoxm@p.webshare.io:80"
#         })
#         data = response.json()
#         print(f"Current IP: {data['ip']}")
#     except Exception as e:
#         print(f"Error checking IP: {e}")

# check_ip_using_proxy()

# def check_ip_using_proxy():
#     try:
#         # Use a non-HTTPS service (HTTP) for testing
#         response = requests.get("http://api.ipify.org?format=json", proxies={
#             "http": "http://uvmfwcbs-rotate:imui7uhheoxm@proxy.webshare.io:80",
#             "https": "http://uvmfwcbs-rotate:imui7uhheoxm@proxy.webshare.io:80"
#         })
#         data = response.json()
#         print(f"Current IP: {data['ip']}")
#     except Exception as e:
#         print(f"Error checking IP: {e}")


# def check_ip_without_proxy():
#     try:
#         # Directly accessing the IP service without proxy
#         response = requests.get("https://api.ipify.org?format=json")
#         data = response.json()
#         print(f"Current IP without proxy: {data['ip']}")
#     except Exception as e:
#         print(f"Error checking IP: {e}")

# check_ip_without_proxy()  # Run this to check your direct connection

# check_ip_without_proxy()
# def check_ip_using_proxy():
#     try:
#         # Use a non-HTTPS service (HTTP) for testing
#         response = requests.get("http://api.ipify.org?format=json", proxies={
#             "http": "http://uvmfwcbs-rotate:imui7uhheoxm@proxy.webshare.io:80",
#             "https": "http://uvmfwcbs-rotate:imui7uhheoxm@proxy.webshare.io:80"
#         })
        
#         print(f"Status Code: {response.status_code}")
#         print(f"Raw response: {response.text}")

#         # Try parsing the JSON response
#         data = response.json()
#         print(f"Current IP: {data['ip']}")
        
#     except Exception as e:
#         print(f"Error checking IP: {e}")

# check_ip_using_proxy()

# import requests

# # Define your Webshare API token
# WEBSHARE_API_TOKEN = "8tvdvri0qf5k52x67f0iv7peuub1t4o11aqvl87y"

# # Webshare Proxy URL
# PROXY_URL = "https://proxy.webshare.io/api/v2/proxy/list/"

# # Headers with Authorization Token
# headers = {
#     "Authorization": f"Token {WEBSHARE_API_TOKEN}"
# }

# def check_proxy_status():
#     try:
#         # Send request to Webshare API to check the proxy list
#         response = requests.get(PROXY_URL, headers=headers)
        
#         if response.status_code == 200:
#             # Parse the JSON response
#             data = response.json()
#             print("Proxy list retrieved successfully:")
#             print(data)
#         elif response.status_code == 429:
#             print("Rate limit exceeded. Please wait 60 seconds before making another request.")
#         else:
#             print(f"Error: {response.status_code} - {response.text}")
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")

# def check_ip_using_proxy():
#     try:
#         # Test the proxy by using an IP-checking service (e.g., httpbin)
#         response = requests.get("https://httpbin.org/ip", proxies={
#             "http": "http://uvmfwcbs-rotate:imui7uhheoxm@p.webshare.io:80",
#             "https": "http://uvmfwcbs-rotate:imui7uhheoxm@p.webshare.io:80"
#         })

#         if response.status_code == 200:
#             # Print the IP address detected by the proxy
#             data = response.json()
#             print(f"Proxy IP address: {data['origin']}")
#         else:
#             print(f"Failed to retrieve IP address. Status code: {response.status_code}")
#     except requests.exceptions.RequestException as e:
#         print(f"Error during request: {e}")

# def main():
#     # First, check proxy status by fetching proxy list from Webshare API
#     check_proxy_status()

#     # Then, check if rotating proxy is working using IP-check service
#     # check_ip_using_proxy()

# # Execute the main function
# main()
# import requests
# import time

# # Proxy credentials
# proxy_user = "uvmfwcbs-rotate"
# proxy_pass = "imui7uhheoxm"
# proxy_host = "p.webshare.io"
# proxy_port = "80"

# # Construct proxy URL
# proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

# # Proxy configuration
# proxies = {
#     "http": proxy_url,
#     "https": proxy_url,
# }

# # Function to check current IP via proxy
# def check_proxy_ip():
#     try:
#         response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
#         if response.status_code == 200:
#             ip_data = response.json()
#             print(f"✅ Proxy IP: {ip_data['origin']}")
#         else:
#             print(f"❌ Failed. Status Code: {response.status_code}")
#     except requests.exceptions.RequestException as e:
#         print(f"❌ Request error: {e}")

# # Test multiple times to see if IP rotates
# for i in range(5):
#     print(f"\n[Attempt {i + 1}]")
#     check_proxy_ip()
#     time.sleep(5)  # wait 5 seconds between requests to allow potential IP rotation
# check_proxy_ip()

import requests
from youtube_transcript_api import YouTubeTranscriptApi

# def extract_transcript_details(video_id):
#     # Store the original requests.get method
#     original_get = requests.get

#     # Define your proxy settings
#     proxy_url = "http://uvmfwcbs-rotate:imui7uhheoxm@p.webshare.io:80"
#     proxies = {
#         "http": proxy_url,
#         "https": proxy_url
#     }

#     # Define a patched version of requests.get to route through the Webshare rotating proxy
#     def proxy_get(*args, **kwargs):
#         kwargs['proxies'] = proxies
#         return original_get(*args, **kwargs)

#     # Monkey patch requests.get
#     requests.get = proxy_get

#     try:
#         # ⏱ Step 1: Check current IP through proxy
#         try:
#             print("Checking current IP through proxy...")
#             ip_check = requests.get("http://httpbin.org/ip", timeout=10)
#             print(f"✅ Proxy IP used: {ip_check.json().get('origin')}")
#         except Exception as ip_err:
#             print(f"⚠️ Could not verify proxy IP: {ip_err}")

#         # ⏱ Step 2: Call the YouTubeTranscriptApi
#         print(f"Fetching transcript for video: {video_id}")
#         transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

#         # Print available languages
#         available_languages = [t.language_code for t in transcripts]
#         print(f"Available transcripts for video {video_id}: {available_languages}")

#         for lang in ['en', 'en-IN', 'hi']:
#             if lang in available_languages:
#                 try:
#                     transcript = transcripts.find_transcript([lang])
#                     transcript_data = transcript.fetch()
#                     full_transcript = " ".join([getattr(item, "text", "") for item in transcript_data])
#                     print(f"✅ Retrieved transcript for {lang} successfully.")
#                     return full_transcript
#                 except Exception as e:
#                     print(f"❌ Could not retrieve transcript for {lang}: {e}")
#             else:
#                 print(f"ℹ️ Transcript for language {lang} not available.")

#         raise ValueError(
#             f"No transcripts in preferred languages. Available: {available_languages}"
#         )

#     except Exception as e:
#         print(f"❌ Error occurred: {e}")
#         raise e

#     finally:
#         # Restore original requests.get
#         requests.get = original_get
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import random
import re  # Import the regular expression module


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


if __name__ == "__main__":
    # Example Usage
    video_id_to_test = "HISRUrJsD08"  # Replace with a YouTube video ID.
    transcript = extract_transcript_details(video_id_to_test)
    if transcript:
        print(transcript)
    else:
        print("Failed to retrieve transcript.")

        
# GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
# ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
# MONGODB_URI = os.environ.get("MONGODB_URI")

# def extract_transcript_details(video_id):
#     """
#     Extracts transcript details from a YouTube video, using a rotating proxy to avoid IP blocking.

#     Args:
#         video_id (str): The YouTube video ID.

#     Returns:
#         str: The full transcript text, or None if no transcript is found or an error occurs.
#     """

#     # Webshare proxy configuration (Add more proxies to this list for better rotation)
#     proxy_list = [
#         "http://uvmfwcbs-rotate:imui7uhheoxm@p.webshare.io:80",
#         # "http://user2:pass2@host2:port2",  # Add more proxies here to rotate through
#         # "http://user3:pass3@host3:port3",
#     ]

#     def get_working_proxy(proxies):
#         """
#         Checks if the proxies are working and returns a working proxy.
#         Args:
#             proxies (list): A list of proxy URLs
#         Returns:
#              str: A working proxy.
#         """
#         for proxy_url in proxies:
#             try:
#                 print(f"ℹ️  Checking proxy: {proxy_url}")
#                 response = requests.get(
#                     "https://ipv4.webshare.io/",
#                     proxies={"http": proxy_url, "https": proxy_url},
#                     timeout=5  # Added timeout
#                 )
#                 response.raise_for_status()
#                 response_text = response.text

#                 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", response_text):
#                     print(f"✅  Working proxy: {proxy_url}, IP: {response_text}")
#                     return proxy_url
#                 else:
#                     print(
#                         f"❌  Proxy {proxy_url} did not return an IP address.  Response: {response_text}"
#                     )

#             except requests.exceptions.RequestException as e:
#                 print(f"❌  Proxy {proxy_url} failed: {e}")
#         return None

#     original_get = requests.get  # Store the original requests.get

#     try:
#         working_proxy = get_working_proxy(proxy_list)
#         if not working_proxy:
#             raise Exception("No working proxies available")

#         def proxy_get(*args, **kwargs):
#             kwargs["proxies"] = {"http": working_proxy, "https": working_proxy}
#             return original_get(*args, **kwargs)

#         requests.get = proxy_get  # Apply the monkey patch

#         transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
#         available_languages = [t.language_code for t in transcripts]
#         print(f"Available transcripts for video {video_id}: {available_languages}")

#         for lang in ["en", "en-IN", "hi"]:
#             if lang in available_languages:
#                 try:
#                     transcript = transcripts.find_transcript([lang])
#                     transcript_data = transcript.fetch()
#                     full_transcript = " ".join([item.text for item in transcript_data])
#                     print(f"✅ Retrieved transcript for {lang}")
#                     return full_transcript
#                 except Exception as e:
#                     print(f"❌ Error retrieving transcript for {lang}: {e}")
#         raise ValueError(
#             f"No transcripts found in preferred languages. Available: {available_languages}"
#         )

#     except Exception as e:
#         print(f"❌ Error during transcript extraction: {e}")
#         return None  # Important:  Return None on error, don't just raise.
#     finally:
#         requests.get = original_get  # Restore the original requests.get

