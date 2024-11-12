import logging
from typing import Annotated

import aiohttp
from livekit.agents import llm

logger = logging.getLogger("weather-demo")

class GetWeather(llm.FunctionContext):

    @llm.ai_callable()
    async def get_weather(
        self,
        location: Annotated[
            str, llm.TypeInfo(description="The location to get the weather for")
        ],
    ):
        """Fetches weather information for a given location."""
        logger.info(f"Getting weather for {location}")
        url = f"https://wttr.in/{location}?format=%C+%t"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    weather_data = await response.text()
                    logger.info(f"Weather data for {location}: {weather_data}")
                    return f"The weather in {location} is {weather_data}."
                else:
                    raise Exception(f"Failed to get weather data, status code: {response.status}")