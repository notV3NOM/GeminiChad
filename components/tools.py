"""
GeminiChad
Copyright (c) 2024 @notV3NOM

See the README.md file for licensing and disclaimer information.
"""

import requests
import asyncio
import aiohttp
import time

from datetime import datetime
from bs4 import BeautifulSoup
from markdown import markdown

from .prompts import CALC_TEMPLATE
from .config import (
    JINA_BASE_URL,
    JINA_HEADERS,
    logger,
    SEARXNG_BASE_URL,
    SEARXNG_HEADERS,
)
from .llm import calc_model, IMAGE_MODELS, IMAGE_GENERATORS


async def fetch_content(result):
    content = None
    try:
        content = await get_content_from_jina(result["url"])
        if content is None:
            content = await scrape_content(result["url"])
    except Exception as e:
        logger.warning(f"Error fetching content for {result['url']}: {e}")
    return content


async def run_searches(query):
    start = time.perf_counter()
    search_results = []
    search_result_urls = []
    tasks = []
    for result in searxng(query):
        tasks.append(fetch_content(result))
        search_result_urls.append(result["url"])
    results = await asyncio.gather(*tasks)
    for content in results:
        if content:
            search_results.append(content)
    end = time.perf_counter()
    logger.info(f"SEARCH took {end-start:.2f} seconds")
    return search_results, search_result_urls


def web_search(query: str):
    """
    Perform a web search and get the search results.
    With this tool, you have full access to the internet.
    Always utilize this tool to find accurate and up-to-date information, such as current events, prices, or any other missing details.
    Do not instruct the user to perform the search themselves.
    Instead, conduct the web search and provide the relevant information directly to the user.
    Make sure to leverage this capability whenever additional or current information is needed to answer the user's query.

    Args:
        query: The search query string.

    Returns:
        A List containing the search results.
    """
    search_results = []

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        search_results, _ = loop.run_until_complete(run_searches(query))
    except Exception as e:
        logger.exception(f"Error during web search: {e}")

    return search_results


async def get_content_from_jina(url):
    """Get content using the Jina API"""
    logger.info(f"JINA {url}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                JINA_BASE_URL + url, headers=JINA_HEADERS
            ) as response:
                response.raise_for_status()
                json_response = await response.json()
                content = json_response.get("data", {}).get("content")
                if content:
                    return truncate_content(content)
    except Exception:
        if "Authorization" in JINA_HEADERS:
            del JINA_HEADERS["Authorization"]
            logger.info("JINA Key Expired")
        return None


async def scrape_content(url):
    """Scrape content directly from the webpage"""
    logger.info(f"SCRAPE {url}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                soup = BeautifulSoup(await response.text(), "html.parser")
                for tag in soup(["script", "style", "header", "footer", "nav"]):
                    tag.decompose()
                text_content = " ".join(soup.get_text(strip=True).split())
                return truncate_content(text_content)
    except Exception:
        return None


def truncate_content(content: str, max_length=2500):
    """Truncate content"""
    html = markdown(content)
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "header", "footer", "nav"]):
        tag.decompose()
    plaintext = " ".join(soup.get_text(strip=True).split())
    if len(plaintext) <= max_length:
        return plaintext
    truncation_point = plaintext.rfind(".", 0, max_length)
    return (
        plaintext[: truncation_point + 1]
        if truncation_point != -1
        else plaintext[:max_length]
    )


def calculate(expression: str):
    """
    Calculate/Solve a problem using python code execution.
    This tool will generate and run python code to solve the problem or expression.
    Use this tool to solve any problem asked by the user.
    Use this tool to perform any calculation asked by the user.

    Args:
        expression (str): A problem to be solved or a mathematical expression.

    Returns:
        result (str): Result of the problem or expression
    """
    logger.info(f"CALCULATE {expression}")
    result = calc_model.generate_content(CALC_TEMPLATE.format(problem=expression))
    return result.text


def image_generation(prompt: str):
    """
    Generate an Image and return the path of the generated image.
    Use this tool to draw any kind of image like poster, album art or book covers etc.
    With this tool, you have the capability to generate and display images to the user.
    When you use this tool, it is mandatory to respond by displaying the exact result directly to the user.
    The user will not be able to see the image unless you respond with the exact result directly.

    Args:
        prompt: image prompt

    Returns:
        image_path: path of the generated image enclosed in image tags

    """
    logger.info(f"IMAGE GENERATION {prompt}")
    return (
        "<IMAGE>"
        + IMAGE_GENERATORS[IMAGE_MODELS.SCHNELL](prompt)
        + "||"
        + prompt
        + "</IMAGE>"
    )


def searxng(query: str, category="general") -> list:
    """
    Search Searxng
    Category can be "general", "images", "videos", "news", "map", "music", "it", "science", "social_media"
    """
    logger.info(f"SEARXNG {query}")
    search_results = []
    try:
        searxng_url = f"{SEARXNG_BASE_URL}/search?q={query}&format=json&categories={category}&disabled_engines=bing"
        response = requests.get(searxng_url, headers=SEARXNG_HEADERS)
        response.raise_for_status()
        for result in response.json().get("results", [])[:3]:
            search_results.append(result)
    except Exception as e:
        logger.exception(f"Search query failed with error: {e}")

    return search_results


def clock():
    """
    Returns the current date and time as a string in 12-hour format with AM/PM.
    Use this tool to get the current date/time.

    Returns:
        str: A string representing the current date and time in 12-hour format with AM/PM.
    """
    logger.info(f"CLOCK")
    return datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
