"""
Test functions for GNews MCP Server
These functions can be called directly for testing and examples
"""

import os
from typing import Optional, Literal

import httpx

# Import constants and utilities from main module
from main import (
    SUPPORTED_LANGUAGES,
    SUPPORTED_COUNTRIES,
    CATEGORIES,
    get_api_key,
    make_gnews_request,
    validate_common_params,
    build_params,
    logger
)


async def search_news_test(
    q: str,
    lang: Optional[str] = None,
    country: Optional[str] = None,
    max_articles: Optional[int] = 10,
    search_in: Optional[str] = None,
    nullable: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    sortby: Optional[Literal["publishedAt", "relevance"]] = "publishedAt",
    page: Optional[int] = 1
) -> dict:
    """
    Search for news articles using specific keywords.

    This tool allows you to search for news articles based on keywords with various
    filtering options including language, country, date range, and sorting preferences.

    Query Syntax Examples:
    - Simple search: "Apple iPhone"
    - Exact phrase: '"Apple iPhone 15"'
    - Logical operators: "Apple AND iPhone", "Apple OR Microsoft", "Apple NOT iPhone"
    - Complex queries: "(Apple AND iPhone) OR Microsoft"

    Returns a structured response with article details including title, description,
    content, URL, image, publishedAt, and source information.
    """

    # Validate parameters
    validate_common_params(lang or "", country or "", max_articles or 10, page or 1)
    
    # Build request parameters
    params = build_params(
        q=q,
        **({"lang": lang} if lang else {}),
        **({"country": country} if country else {}),
        **({"max": max_articles} if max_articles else {}),
        **({"in": search_in} if search_in else {}),
        **({"nullable": nullable} if nullable else {}),
        **({"from": date_from} if date_from else {}),
        **({"to": date_to} if date_to else {}),
        **({"sortby": sortby} if sortby else {}),
        **({"page": page} if page else {})
    )
    
    try:
        result = await make_gnews_request("search", params)
        return {
            "success": True,
            "query": q,
            "totalArticles": result.get("totalArticles", 0),
            "articles": result.get("articles", []),
            "parameters_used": params
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": q,
            "parameters_used": params
        }


async def get_top_headlines_test(
    category: Optional[Literal["general", "world", "nation", "business", "technology", "entertainment", "sports", "science", "health"]] = "general",
    lang: Optional[str] = None,
    country: Optional[str] = None,
    max_articles: Optional[int] = 10,
    nullable: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    q: Optional[str] = None,
    page: Optional[int] = 1
) -> dict:
    """
    Get current trending news articles based on Google News ranking.

    This tool retrieves the top headlines for a specific category. The articles
    are selected based on Google News ranking algorithm, providing the most
    relevant and trending news for the chosen category.

    Available categories:
    - general: General news (default)
    - world: International news
    - nation: National news
    - business: Business and finance
    - technology: Technology and innovation
    - entertainment: Entertainment and celebrity news
    - sports: Sports news
    - science: Scientific discoveries and research
    - health: Health and medical news

    Returns a structured response with trending article details.
    """

    # Validate parameters
    if category and category not in CATEGORIES:
        raise ValueError(f"Unsupported category '{category}'. Supported categories: {', '.join(CATEGORIES)}")

    validate_common_params(lang or "", country or "", max_articles or 10, page or 1)
    
    # Build request parameters
    params = build_params(
        **({"category": category} if category else {}),
        **({"lang": lang} if lang else {}),
        **({"country": country} if country else {}),
        **({"max": max_articles} if max_articles else {}),
        **({"nullable": nullable} if nullable else {}),
        **({"from": date_from} if date_from else {}),
        **({"to": date_to} if date_to else {}),
        **({"q": q} if q else {}),
        **({"page": page} if page else {})
    )
    
    try:
        logger.info(f"Getting top headlines for category '{category}' with params: {params}")
        result = await make_gnews_request("top-headlines", params)
        return {
            "success": True,
            "category": category or "general",
            "totalArticles": result.get("totalArticles", 0),
            "articles": result.get("articles", []),
            "parameters_used": params
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "category": category or "general",
            "parameters_used": params
        }