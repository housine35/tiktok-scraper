import subprocess
import re


def get_secuid(tiktok_url):
    # Curl command with headers and compressed content handling
    curl_command = [
        "curl",
        "-s",  # Silent mode
        "-L",  # Follow redirects
        "--compressed",  # Handle compressed responses (gzip, br, etc.)
        "-A",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0",  # User-Agent
        "-H",
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "-H",
        "Accept-Language: en-US,en;q=0.5",
        "-H",
        "Accept-Encoding: gzip, deflate, br",
        "-H",
        "Upgrade-Insecure-Requests: 1",
        "-H",
        "Connection: keep-alive",
        "-H",
        "TE: trailers",
        "-H",
        "Cookie: ttwid=1%7CXo2BSVMt1H3-xaMKZOvQJz68HIZD2rJi9FF2Rg8Yso4%7C1738938025%7C300bfbb29e395061719771060f47b5fb316282ee6fd96e03b3364e013a0b1900;",
        tiktok_url,
    ]

    try:
        # Execute the curl command and capture the output
        result = subprocess.run(
            curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Decode the response using 'latin1' to avoid UTF-8 decoding errors (fallback for non-UTF-8 characters)
        response_text = result.stdout.decode("utf-8", errors="replace")

        # Extract secUid using regex
        match = re.search(r'"verified":.*?,"secUid":"(.*?)",', response_text)
        if match:
            return match.group(1)
        else:
            return "secUid not found or condition not met in the response."

    except Exception as e:
        return f"Error: {e}"
