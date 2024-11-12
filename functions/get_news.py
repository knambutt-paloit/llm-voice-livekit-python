import logging
from typing import Annotated

import aiohttp
from livekit.agents import llm

logger = logging.getLogger("news-demo")

class GetNews(llm.FunctionContext):

    @llm.ai_callable()
    async def get_news(
        self,
        topic: Annotated[
            str, llm.TypeInfo(description="The news topic to retrieve")
        ],
    ):
        """Fetches news information based on a given topic."""
        logger.info(f"Fetching news for topic: {topic}")
        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey=your_news_api_key"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    news_data = await response.json()
                    articles = news_data.get("articles", [])
                    top_article = articles[0]["title"] if articles else "No news found."
                    logger.info(f"Top news article on {topic}: {top_article}")
                    return f"Top news on {topic}: {top_article}"
                else:
                    raise Exception(f"Failed to get news data, status code: {response.status}")