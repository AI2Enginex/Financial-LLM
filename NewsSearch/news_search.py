
from typing import Optional, List, Dict
from urllib.parse import urlparse
import trafilatura
import os
import re
from dotenv import load_dotenv
from tavily import TavilyClient
from ddgs import DDGS

load_dotenv()


class WebSearchTool:
    """
    Web search tool for retrieving information when LLM is unable to provide answer
    Supports multiple search providers: Tavily (recommended), Google Search API, or DuckDuckGo
    """
    
    def __init__(self, api_key: Optional[str] = None, provider: str = None):
        """
        Initialize web search tool
        
        Args:
            api_key: API key for the search provider
            provider: Search provider to use ("tavily", "google", or "duckduckgo")
                     If None, will auto-select based on available API keys
        """
        self.tavily_key = api_key or os.getenv("TAVILY_API_KEY")
        self.google_key = os.getenv("SERPAPI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        # Auto-select provider based on available keys
        if provider:
            self.provider = provider
        elif self.tavily_key:
            self.provider = "tavily"
            print(f"Using Tavily as search provider")
        elif self.google_key:
            self.provider = "google"
            print(f"Using Google Search as search provider")
        else:
            self.provider = "duckduckgo"
            print(f"Using DuckDuckGo as search provider (free, no API key)")
    
    def _clean_text(self, text: str):
        """
        Clean text by removing HTML tags, URLs, markdown links, and unwanted content
        """
        if not text:
            return ""
        
        # Remove HTML tags like <img>, <video>, <a href>, etc.
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove markdown links [text](url)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        # Remove URLs and hyperlinks
        text = re.sub(r'https?://[^\s]+', '', text)
        text = re.sub(r'www\.[^\s]+', '', text)
        
        # Remove common image/embed references
        text = re.sub(r'\[image\]|\[video\]|\[ad\]|\[embed\]', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\(image\)|\(video\)|\(ad\)', '', text, flags=re.IGNORECASE)
        
        # Remove mailto: and ftp: links
        text = re.sub(r'mailto:[^\s]+|ftp://[^\s]+', '', text)
        
        # Remove multiple spaces and clean up
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    # Read content from search results, fetch full text from URLs, and clean it
    # Returns list of results with 'title', 'url', 'snippet', 'content', and 'source'
    def read_content(self, response: dict, total_results: int):

        results = list()

        for item in response.get("results", []):

                title = item.get("title", "")
                url = item.get("url", "")
                snippet = item.get("content", "")

                try:

                    downloaded = trafilatura.fetch_url(url)

                    full_text = trafilatura.extract(
                        downloaded,
                        include_comments=False,
                        include_tables=False
                    )

                except Exception as extraction_error:
                    print(f"Extraction failed: {extraction_error}")
                    continue

                # fallback
                if not full_text:
                    full_text = snippet

                full_text = self._clean_text(full_text)

                if not full_text:
                    continue

                full_text = full_text.strip().lower()

                results.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                    "content": full_text,
                    "source": urlparse(url).netloc
                })

                if len(results) >= total_results:
                    break
            
        return results
    
    # Perform search using Tavily API (recommended for best quality and relevance)
    def _tavily_search(self, query: str, num_results: int):

        try:

            if not self.tavily_key:
                print("Tavily API key missing")
                return []

            client = TavilyClient(api_key=self.tavily_key)

            response = client.search(
                query=query,
                search_depth="advanced",
                max_results=num_results * 3,
                include_answer=False,
                include_raw_content=False
            )

            results = self.read_content(response, num_results)

            print(f"total {len(results)} high-quality results")

            return results

        except Exception as e:

            print(f"Tavily search error: {e}")

            return []
    
    
    def _duckduckgo_search(self, query: str, num_results: int):
        """
        Search using DuckDuckGo (free, no API key needed)
        Returns list of results with 'title', 'url', and 'snippet'
        """
        try:
            ddgs = DDGS()
            try:
                search_results = list(ddgs.text(query, max_results=num_results*2, timelimit='y'))

                results = self.read_content({"results": search_results}, num_results)

                return results
            except Exception as search_error:
                print(f"DuckDuckGo query error: {search_error}")
                return []
            
            
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
            import traceback
            traceback.print_exc()
            return []
    

    def search(self, query: str, num_results: int):
        """
        Perform web search and return results
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of dictionaries with 'title', 'url', 'snippet'
        """
        print(f"Searching with {self.provider}...")
        try:
            # Try with selected provider
            if self.provider == "tavily" and self.tavily_key:
                results = self._tavily_search(query, num_results)
                if results:
                    return results
            elif self.provider == "google" and self.google_key:
                results = self._google_search(query, num_results)
                if results:
                    return results
            
            # Fallback to DuckDuckGo
            print(f"Primary search failed or returned empty. Trying DuckDuckGo fallback...")
            results = self._duckduckgo_search(query, num_results)
            return results if results else []
            
        except Exception as e:
            print(f"Error in web search ({self.provider}): {e}")
            # Try DuckDuckGo as last resort
            try:
                print(f"Attempting DuckDuckGo as final fallback...")
                results = self._duckduckgo_search(query, num_results)
                return results if results else []
            except Exception as fallback_e:
                print(f"All search providers failed: {fallback_e}")
                return []
    
    # Format search results as a readable string with full content
    # Text-only results, cleaned of unwanted markup, images, and hyperlinks
    def format_search_results(self, results: List[Dict[str, str]]):
        
        if not results:
            return "Web Search: No results found. Please try a different query or refine your search terms."
        
        formatted = "\nWeb Search Results:\n"
        
        
        for idx, result in enumerate(results, 1):
            title = result.get('title', 'N/A')
            url = result.get('url', 'N/A')
            snippet = result.get('snippet', 'N/A')
            
            # Apply additional cleaning to ensure no artifacts remain
            snippet = self._clean_text(snippet)
            snippet = snippet.strip()
            formatted += f"\n{idx}. {title}\n"
            formatted += f"\nURL: {url}\n"
            formatted += f"\nSummary: {snippet}\n"
            
        
        return formatted


if __name__ == "__main__":
    search_tool = WebSearchTool()
    ticker = "IDFC First Bank"
    query = f"""
            Fetch the Latest news about {ticker}.
            Focus on:
            - earnings
            - quarterly results
            - guidance
            - stock performance
            - market sentiment

"""
    results = search_tool.search(query, num_results=10)
    print(search_tool.format_search_results(results))