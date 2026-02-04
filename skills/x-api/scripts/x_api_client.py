#!/usr/bin/env python3
"""
X API Client - A Python wrapper for X (Twitter) API v2

This module provides functions for interacting with X API v2 endpoints.
Uses OAuth 1.0a user context authentication.

Environment variables required:
    X_API_KEY: Consumer Key (API Key)
    X_API_SECRET: Consumer Secret (API Secret)
    X_ACCESS_TOKEN: Access Token
    X_ACCESS_SECRET: Access Token Secret

Or use a .env file in the root directory with these variables.
"""

import os
import json
import re
import base64
import hashlib
import hmac
import time
import random
import urllib.parse
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library is required. Install with: pip3 install requests")
    raise


class XAPIClientError(Exception):
    """Base exception for X API client errors."""
    pass


class XAPIAuthenticationError(XAPIClientError):
    """Authentication related errors."""
    pass


class XAPIRateLimitError(XAPIClientError):
    """Rate limit exceeded errors."""
    pass


class XAPIClient:
    """X API v2 Client using OAuth 1.0a authentication."""

    BASE_URL = "https://api.x.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        access_secret: Optional[str] = None,
    ):
        """
        Initialize the X API client with OAuth 1.0a credentials.

        Args:
            api_key: Consumer Key (API Key). If None, will try to load from env.
            api_secret: Consumer Secret. If None, will try to load from env.
            access_token: Access Token. If None, will try to load from env.
            access_secret: Access Token Secret. If None, will try to load from env.
        """
        self.api_key = api_key or os.getenv("X_API_KEY") or os.getenv("TWITTER_API_KEY")
        self.api_secret = api_secret or os.getenv("X_API_SECRET") or os.getenv("TWITTER_API_SECRET")
        self.access_token = access_token or os.getenv("X_ACCESS_TOKEN") or os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_secret = access_secret or os.getenv("X_ACCESS_SECRET") or os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

        if not all([self.api_key, self.api_secret, self.access_token, self.access_secret]):
            raise XAPIAuthenticationError(
                "Missing OAuth 1.0a credentials. Required: X_API_KEY, X_API_SECRET, "
                "X_ACCESS_TOKEN, X_ACCESS_SECRET"
            )

        # Caching for API efficiency
        self._cached_user_id = None
        self._username_cache = {}
        self._CACHE_TTL = 3600  # 1 hour for username cache

    def _generate_nonce(self) -> str:
        """Generate a random nonce for OAuth signature."""
        return base64.b64encode(os.urandom(32)).decode('utf-8').rstrip('=')

    def _generate_timestamp(self) -> str:
        """Generate Unix timestamp for OAuth signature."""
        return str(int(time.time()))

    def _percent_encode(self, s: str) -> str:
        """Percent encode a string for OAuth."""
        return urllib.parse.quote(s, safe='-._~')

    def _collect_parameters(
        self,
        params: Optional[Dict],
        oauth_params: Dict[str, str],
        url: str,
    ) -> Dict[str, str]:
        """Collect all parameters for signature."""
        all_params = {}
        if params:
            for k, v in params.items():
                if isinstance(v, list):
                    for item in v:
                        all_params[self._percent_encode(str(k))] = self._percent_encode(str(item))
                else:
                    all_params[self._percent_encode(str(k))] = self._percent_encode(str(v))

        # Add OAuth parameters
        for k, v in oauth_params.items():
            all_params[self._percent_encode(k)] = self._percent_encode(v)

        return all_params

    def _create_signature_base_string(
        self,
        method: str,
        url: str,
        params: Dict[str, str],
    ) -> str:
        """Create the signature base string."""
        # Sort parameters
        encoded_params = []
        for k in sorted(params.keys()):
            encoded_params.append(f"{k}={params[k]}")

        parameter_string = '&'.join(encoded_params)
        parsed_url = urllib.parse.urlparse(url)

        base_string = '&'.join([
            method.upper(),
            self._percent_encode(f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"),
            self._percent_encode(parameter_string)
        ])

        return base_string

    def _generate_signature(
        self,
        method: str,
        url: str,
        params: Dict[str, str],
    ) -> str:
        """Generate OAuth 1.0a signature."""
        signing_key = f"{self._percent_encode(self.api_secret)}&{self._percent_encode(self.access_secret)}"
        base_string = self._create_signature_base_string(method, url, params)

        signature = hmac.new(
            signing_key.encode('utf-8'),
            base_string.encode('utf-8'),
            hashlib.sha256
        ).digest()

        return base64.b64encode(signature).decode('utf-8')

    def _create_oauth_header(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
    ) -> str:
        """Create OAuth 1.0a Authorization header."""
        oauth_params = {
            'oauth_consumer_key': self.api_key,
            'oauth_token': self.access_token,
            'oauth_signature_method': 'HMAC-SHA256',
            'oauth_timestamp': self._generate_timestamp(),
            'oauth_nonce': self._generate_nonce(),
            'oauth_version': '1.0',
        }

        # Collect all parameters including OAuth params
        all_params = self._collect_parameters(params, oauth_params, url)

        # Generate signature
        signature = self._generate_signature(method, url, all_params)
        oauth_params['oauth_signature'] = signature

        # Build OAuth header
        oauth_header_parts = []
        for k, v in oauth_params.items():
            oauth_header_parts.append(f'{k}="{self._percent_encode(v)}"')

        return f'OAuth {", ".join(oauth_header_parts)}'

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        multipart: bool = False,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the X API with OAuth 1.0a authentication.

        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data
            files: Files for multipart upload
            multipart: Whether to use multipart/form-data

        Returns:
            JSON response as dictionary

        Raises:
            XAPIClientError: On API errors
        """
        url = f"{self.BASE_URL}{endpoint}"

        # X API OAuth 1.0a signature rules:
        # - Query params always in signature
        # - Body params NOT included in signature for JSON requests (X API v2 style)

        sig_params = {}
        if params:
            sig_params.update(params)

        headers = {
            "Content-Type": "application/json",
        }

        # Create OAuth header with appropriate parameters for signature
        oauth_header = self._create_oauth_header(method, url, sig_params)
        headers["Authorization"] = oauth_header

        if multipart:
            headers.pop("Content-Type", None)

        try:
            if files:
                response = requests.request(
                    method, url, headers=headers, data=data, files=files, params=params
                )
            else:
                response = requests.request(
                    method, url, headers=headers, json=data, params=params
                )

            # Handle rate limiting
            if response.status_code == 429:
                raise XAPIRateLimitError("Rate limit exceeded")

            # Handle other errors
            if not response.ok:
                try:
                    error_data = response.json() if response.content else {}
                except:
                    error_data = {}
                error_msg = error_data.get("title", response.text)
                detail = error_data.get("detail", "")
                if detail:
                    error_msg += f": {detail}"
                raise XAPIClientError(
                    f"API Error {response.status_code}: {error_msg}"
                )

            return response.json()

        except requests.RequestException as e:
            raise XAPIClientError(f"Request failed: {e}")

    def extract_tweet_id(self, tweet_url_or_id: str) -> str:
        """
        Extract tweet ID from a URL or return the ID if already an ID.

        Args:
            tweet_url_or_id: Tweet URL or ID

        Returns:
            Tweet ID as string
        """
        # Check if it's already a numeric ID
        if re.match(r'^\d{15,20}$', tweet_url_or_id):
            return tweet_url_or_id

        # Try to extract from URL
        patterns = [
            r'twitter\.com/\w+/status/(\d+)',
            r'x\.com/\w+/status/(\d+)',
            r'mobile\.twitter\.com/\w+/status/(\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, tweet_url_or_id)
            if match:
                return match.group(1)

        raise XAPIClientError(f"Could not extract tweet ID from: {tweet_url_or_id}")

    def _get_my_user_id(self) -> str:
        """
        Get the authenticated user's ID with caching.

        Returns:
            Cached user ID as string
        """
        if self._cached_user_id is None:
            response = self._make_request("GET", "/2/users/me")
            self._cached_user_id = response["data"]["id"]
        return self._cached_user_id

    def get_user_id_from_username(self, username: str) -> str:
        """
        Get user ID from username with caching.

        Args:
            username: X handle (with or without @)

        Returns:
            User ID as string
        """
        username = username.lstrip("@")

        # Check cache
        if username in self._username_cache:
            cached_id, timestamp = self._username_cache[username]
            if time.time() - timestamp < self._CACHE_TTL:
                return cached_id

        # Fetch from API
        response = self._make_request(
            "GET",
            f"/2/users/by/username/{username}",
        )
        if "data" not in response:
            raise XAPIClientError(f"User not found: {username}")

        user_id = response["data"]["id"]
        self._username_cache[username] = (user_id, time.time())
        return user_id

    def upload_media(self, media_path: str, media_category: str = "tweet_image") -> str:
        """
        Upload media and return media_id.

        Args:
            media_path: Path to media file
            media_category: Category (tweet_image, dm_image, subtitles)

        Returns:
            Media ID string
        """
        # Check if file exists
        path = Path(media_path)
        if not path.exists():
            raise XAPIClientError(f"File not found: {media_path}")

        # Determine media type
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".bmp": "image/bmp",
            ".gif": "image/gif",
            ".mp4": "video/mp4",
            ".mov": "video/quicktime",
        }
        ext = path.suffix.lower()
        media_type = mime_types.get(ext)
        if not media_type:
            raise XAPIClientError(f"Unsupported file type: {ext}")

        # Upload media using OAuth 1.0a with multipart
        url = f"{self.BASE_URL}/2/media/upload"

        # Create OAuth header for multipart
        oauth_header = self._create_oauth_header("POST", url, {})

        with open(path, "rb") as f:
            files = {"media": (path.name, f, media_type)}
            data = {
                "media_category": media_category,
            }
            headers = {
                "Authorization": oauth_header,
            }

            response = requests.post(url, headers=headers, data=data, files=files)

        if response.status_code == 429:
            raise XAPIRateLimitError("Rate limit exceeded")

        if not response.ok:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get("title", response.text)
            raise XAPIClientError(f"Media upload failed: {error_msg}")

        result = response.json()
        if "data" not in result:
            raise XAPIClientError(f"Media upload failed: {result}")

        return result["data"]["id"]

    # ============== POST FUNCTIONS ==============

    def post_tweet(
        self,
        text: str,
        reply_to_id: Optional[str] = None,
        quote_tweet_id: Optional[str] = None,
        media_ids: Optional[List[str]] = None,
        reply_settings: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Post a tweet, reply, or quote tweet.

        Args:
            text: Tweet text content
            reply_to_id: Tweet ID to reply to (parent post)
            quote_tweet_id: Tweet ID to quote (child post)
            media_ids: List of media IDs to attach
            reply_settings: Who can reply (everyone, mentionedUsers, following, subscribers)

        Returns:
            Response with tweet data
        """
        data: Dict[str, Any] = {"text": text}

        if reply_to_id:
            data["reply"] = {"in_reply_to_tweet_id": reply_to_id}

        if quote_tweet_id:
            data["quote_tweet_id"] = quote_tweet_id

        if media_ids:
            data["media"] = {"media_ids": media_ids}

        if reply_settings:
            data["reply_settings"] = reply_settings

        return self._make_request("POST", "/2/tweets", data=data)

    def post_reply(self, text: str, parent_post_link: str, **kwargs) -> Dict[str, Any]:
        """
        Post a reply to a tweet.

        Args:
            text: Reply text content
            parent_post_link: Parent post URL or ID
            **kwargs: Additional arguments for post_tweet

        Returns:
            Response with tweet data
        """
        parent_id = self.extract_tweet_id(parent_post_link)
        return self.post_tweet(text, reply_to_id=parent_id, **kwargs)

    def post_quote(self, text: str, child_post_link: str, **kwargs) -> Dict[str, Any]:
        """
        Post a quote tweet.

        Args:
            text: Quote tweet text content
            child_post_link: Post URL or ID to quote
            **kwargs: Additional arguments for post_tweet

        Returns:
            Response with tweet data
        """
        quote_id = self.extract_tweet_id(child_post_link)
        return self.post_tweet(text, quote_tweet_id=quote_id, **kwargs)

    def post_with_media(
        self,
        text: str,
        media_location: str,
        is_url: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Post a tweet with media.

        Args:
            text: Tweet text content
            media_location: Path to media file
            is_url: Whether media_location is a URL (not supported)
            **kwargs: Additional arguments for post_tweet

        Returns:
            Response with tweet data
        """
        media_id = self.upload_media(media_location)
        return self.post_tweet(text, media_ids=[media_id], **kwargs)

    def delete_post(self, post_link: str) -> Dict[str, Any]:
        """
        Delete a tweet.

        Args:
            post_link: Tweet URL or ID to delete

        Returns:
            Response with deletion status
        """
        tweet_id = self.extract_tweet_id(post_link)
        return self._make_request("DELETE", f"/2/tweets/{tweet_id}")

    def retweet(self, child_post_link: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Retweet a post.

        Args:
            child_post_link: Post URL or ID to retweet
            user_id: Your user ID (if None, will use cached value)

        Returns:
            Response with retweet data
        """
        tweet_id = self.extract_tweet_id(child_post_link)

        if not user_id:
            user_id = self._get_my_user_id()

        data = {"tweet_id": tweet_id}
        return self._make_request("POST", f"/2/users/{user_id}/retweets", data=data)

    def like_post(self, post_link: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Like a post.

        Args:
            post_link: Post URL or ID to like
            user_id: Your user ID (if None, will use cached value)

        Returns:
            Response with like data
        """
        tweet_id = self.extract_tweet_id(post_link)

        if not user_id:
            user_id = self._get_my_user_id()

        data = {"tweet_id": tweet_id}
        return self._make_request("POST", f"/2/users/{user_id}/likes", data=data)

    # ============== DIRECT MESSAGE FUNCTIONS ==============

    def send_dm(
        self,
        recipient_handle: str,
        text: str,
        media_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send a direct message.

        Args:
            recipient_handle: X handle of recipient (with or without @)
            text: Message text content
            media_path: Optional path to media file

        Returns:
            Response with DM data
        """
        participant_id = self.get_user_id_from_username(recipient_handle)

        data: Dict[str, Any] = {}

        if text:
            data["text"] = text

        if media_path:
            media_id = self.upload_media(media_path, media_category="dm_image")
            data["attachments"] = [{"media_id": media_id}]

        return self._make_request(
            "POST",
            f"/2/dm_conversations/with/{participant_id}/messages",
            data=data,
        )

    # ============== TIMELINE FUNCTIONS ==============

    def get_user_posts(
        self,
        username: str,
        timeframe: Optional[str] = None,
        max_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Get recent posts from a user.

        Args:
            username: X handle (with or without @)
            timeframe: Time filter like "2hrs", "8hrs", "1d", "1w"
            max_results: Number of results (5-100)

        Returns:
            List of tweet data
        """
        user_id = self.get_user_id_from_username(username)

        params: Dict[str, Any] = {
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics,reply_settings",
        }

        # Parse timeframe and set start_time
        if timeframe:
            now = datetime.utcnow()
            time_mappings = {
                "min": ("minutes", 1),
                "mins": ("minutes", 1),
                "hr": ("hours", 1),
                "hrs": ("hours", 1),
                "h": ("hours", 1),
                "d": ("days", 1),
                "day": ("days", 1),
                "days": ("days", 1),
                "w": ("weeks", 1),
                "week": ("weeks", 1),
                "weeks": ("weeks", 1),
            }

            # Parse the timeframe
            match = re.match(r'^(\d+)\s*([a-z]+)$', timeframe.lower())
            if match:
                amount = int(match.group(1))
                unit = match.group(2)

                if unit in time_mappings:
                    unit_name, multiplier = time_mappings[unit]
                    kwargs = {unit_name: amount}
                    start_time = now - timedelta(**kwargs)
                    params["start_time"] = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        response = self._make_request(
            "GET",
            f"/2/users/{user_id}/tweets",
            params=params,
        )

        return response.get("data", [])

    def get_timeline(
        self,
        count: int = 10,
        user_id: Optional[str] = None,
        exclude: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get timeline posts (reverse chronological home timeline).

        Args:
            count: Number of posts to retrieve (1-100)
            user_id: Your user ID (if None, will use cached value)
            exclude: List of types to exclude (replies, retweets)

        Returns:
            List of tweet data
        """
        if not user_id:
            user_id = self._get_my_user_id()

        params: Dict[str, Any] = {
            "max_results": min(max(1, count), 100),
            "tweet.fields": "created_at,public_metrics,reply_settings,author_id",
        }

        if exclude:
            params["exclude"] = exclude

        response = self._make_request(
            "GET",
            f"/2/users/{user_id}/timelines/reverse_chronological",
            params=params,
        )

        return response.get("data", [])

    # ============== SEARCH FUNCTIONS ==============

    def search_tweets(
        self,
        query: str,
        max_results: int = 10,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        since_id: Optional[str] = None,
        until_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for tweets using X API v2 recent search.

        Args:
            query: Search query (supports operators like #hashtag, @mention, from:user, etc.)
            max_results: Number of results (10-100)
            start_time: ISO 8601 datetime string (e.g., "2025-01-01T00:00:00Z")
            end_time: ISO 8601 datetime string (e.g., "2025-01-31T23:59:59Z")
            since_id: Return tweets after this ID (exclusive)
            until_id: Return tweets before this ID (exclusive)

        Returns:
            List of tweet data dictionaries

        Search Query Operators:
            - Text: "keyword", "phrase search"
            - Hashtag: #hashtag or #cryptocurrency
            - Mention: @username
            - From user: from:username
            - To user: to:username
            - Boolean: keyword1 AND keyword2, keyword1 OR keyword2
            - Negation: keyword -unwanted
            - URL: url:example.com
            - Media: has:images, has:videos, has:links
            - Language: lang:en (ISO 639-1 code)
            - Replies: is:reply, is:quote_tweet
            - Verified: is:verified
            - Min retweets: min_retweets:5
            - Min likes: min_faves:10
        """
        params: Dict[str, Any] = {
            "query": query,
            "max_results": min(max(10, max_results), 100),
            "tweet.fields": "created_at,public_metrics,reply_settings,author_id,lang",
        }

        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        if since_id:
            params["since_id"] = since_id
        if until_id:
            params["until_id"] = until_id

        response = self._make_request(
            "GET",
            "/2/tweets/search/recent",
            params=params,
        )

        # Return tweets with author info merged
        results = []
        users_map = {}
        if "includes" in response and "users" in response["includes"]:
            for user in response["includes"]["users"]:
                users_map[user["id"]] = user

        for tweet in response.get("data", []):
            tweet_data = tweet.copy()
            if "author_id" in tweet and tweet["author_id"] in users_map:
                tweet_data["author"] = users_map[tweet["author_id"]]
            results.append(tweet_data)

        return results


# ============== CLI FUNCTIONS ==============

def _load_env():
    """Load environment variables from .env file in root directory."""
    env_path = Path("/root/.env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()


def get_client() -> XAPIClient:
    """Get an initialized X API client."""
    _load_env()
    return XAPIClient()


if __name__ == "__main__":
    # Test import
    print("X API Client module loaded successfully")
