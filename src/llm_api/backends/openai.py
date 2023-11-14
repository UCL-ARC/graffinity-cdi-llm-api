"""Provides user search processing and OpenAI language model calling functionality."""
import json

import openai
from openai import AsyncOpenAI

from llm_api.config import Settings


class OpenaiModelCallError(Exception):
    """Generate a custom exception for Openai API errors."""


class OpenaiCaller:
    """Process prompts and call Openai LLMs."""

    def __init__(self, settings: Settings) -> None:
        """
        Class constructor.

        Args:
            settings (Settings): Pydantic settings object.
        """
        self.settings = settings

        self.client = self.get_client()

    def get_client(self) -> AsyncOpenAI:
        """
        Retrieve an asynchronous OpenAI client object.

        Returns
            OpenAI: OpenAI client object
        """
        return AsyncOpenAI(api_key=self.settings.openai_api_key.get_secret_value())

    @staticmethod
    def generate_openai_prompt(user_input: str) -> list[dict[str, str]]:
        """
        Generate a prompt from user input to send to Openai models.

        The prompt includes `system` and `user` roles to define expected
        input and output formats.

        Args:
            user_input (str): User search input.

        Returns:
            list[dict[str, str]]: A list of dictionaries containing roles and content.
        """
        return [
            {
                "role": "system",
                "content": "You are a helpful search assistant that extracts \
                    useful entities and relationships from user search queries.",
            },
            {
                "role": "system",
                "content": "Users will provide you with a search, as a string. \
                    You should examine this string and determine entities directly \
                    from the string in addition to any other entities not found in \
                    the string that may be relevant to the search. \
                    Try to find at least 5 relevant entities in each case, but no \
                    more than 10. Try to keep entities specific to the search. \
                    If you are unsure whether an entity is connected to the search, \
                    do not include it.",
            },
            {
                "role": "system",
                "content": "You should provide your response as valid JSON, in a \
                format matching the following example. The example will be preceded and \
                followed by three backticks. Dictionary keys should be taken literally, but \
                dictionary values are indicative. \
                ```\
                    {'entities': [ \
                        {'uri': 'entity name', 'description': 'entity description', \
                        'wikipedia_url': 'entity wikipedia url'} \
                    ]},\
                    'connections': [\
                    {'from': 'uri'\
                    'to': 'uri'\
                    'label': 'label describing entity-entity relationship\
                    }]\
                    }\
                ```",
            },
            {"role": "user", "content": f"{user_input}"},
        ]

    async def call_model(self, openai_model: str, prompt: list[dict]) -> dict[str, str]:
        """
        Call the external Openai model specified with a defined prompt.

        Args:
            openai_model (str): String representing OpenAI model to call
            prompt (list[dict]): Constructed prompt from user input

        Raises:
            OpenaiModelCallError: API connection exception
            OpenaiModelCallError: Rate limit exception
            OpenaiModelCallError: General API error exception

        Returns:
            dict: Dictionary created from JSON response
        """
        try:
            response = await self.client.chat.completions.create(
                model=openai_model,
                messages=prompt,
                response_format={"type": "json_object"},
            )
            response_content = response.choices[0].message.content

            return json.loads(response_content)

        except openai.APIConnectionError as connection_error:
            message = f"Unable to connect to OpenAI. {connection_error}"
            raise OpenaiModelCallError(message) from connection_error
        except openai.RateLimitError as rate_limit_error:
            message = f"Rate limit exceeded. {rate_limit_error}"
            raise OpenaiModelCallError(message) from rate_limit_error
        except openai.APIError as api_error:
            message = f"OpenAI API error: {api_error}"
            raise OpenaiModelCallError(message) from api_error
