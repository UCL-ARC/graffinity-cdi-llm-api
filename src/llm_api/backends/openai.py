"""Provides user search processing and OpenAI language model calling functionality."""
import json

import openai
from langchain.prompts import ChatPromptTemplate
from langchain.schema.exceptions import LangChainException
from langchain_openai import ChatOpenAI

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

    def get_client(self) -> ChatOpenAI:
        """
        Retrieve an asynchronous OpenAI client object.

        Returns
            ChatOpenAI: Langchain ChatOpenAI client object
        """
        return ChatOpenAI(
            api_key=self.settings.openai_api_key.get_secret_value(),
            model_name=self.settings.openai_llm_name,
            temperature=0.2,
            model_kwargs={"response_format": {"type": "json_object"}},
        )

    @staticmethod
    def generate_openai_prompt() -> ChatPromptTemplate:
        """
        Generate a prompt from user input to send to Openai models.

        The prompt includes `system` and `user` roles to define expected
        input and output formats.

        Args:
            user_input (str): User search input.

        Returns:
            ChatPromptTemplate: A list of dictionaries containing roles and content.
        """
        user_template = "{text}"
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    " ".join(
                        "You are a helpful search assistant that extracts \
                    useful entities and relationships from user search queries.".split()
                    ),
                ),
                (
                    "system",
                    " ".join(
                        "Users will provide you with a search, as a string. \
                    You should examine this string and determine entities directly \
                    from the string in addition to any other entities not found in \
                    the string that may be relevant to the search. \
                    Try to find at least 5 relevant entities in each case, but no \
                    more than 10. Try to keep entities specific to the search. \
                    If you are unsure whether an entity is connected to the search, \
                    do not include it. Also provide the wikipedia URL for each entity \
                    you identify. If you are unsure if the URL is valid, do not include \
                    a URL in your response.".split()
                    ),
                ),
                (
                    "system",
                    " ".join(
                        "You should provide your response as valid JSON, in a \
                format matching the following example, which is shown \
                between the two sets of three backtick characters (`). Dictionary keys \
                should be taken literally, \
                but dictionary values are indicative".split()
                    ),
                ),
                (
                    "system",
                    "```\
                    {{'entities': [ \
                        {{'uri': 'entity name', 'description': 'entity description', \
                        'wikipedia_url': 'entity wikipedia url'}} \
                    ]}},\
                    'connections': [\
                    {{'from': 'uri'\
                    'to': 'uri'\
                    'description': 'short paragraph describing entity-entity relationship\
                    }}]\
                    }} \
            ```",
                ),
                ("user", user_template),
            ]
        )

    async def call_model(
        self, prompt_template: ChatPromptTemplate, user_search: str
    ) -> dict[str, str]:
        """
        Call the external Openai model specified with a defined prompt via LangChain.

        Args:
            prompt_template (ChatPromptTemplate): LangChain ChatPromptTemplate
                containing system instructions and any example formatting required.
            user_search (str): User's search as a string.

        Raises:
            OpenaiModelCallError: General LangChain exception
            OpenaiModelCallError: API connection exception
            OpenaiModelCallError: Rate limit exception
            OpenaiModelCallError: General API error exception

        Returns:
            dict[str, str]: Model JSON response as a dictionary.
        """
        try:
            self.chain = prompt_template | self.client
            model_response = await self.chain.ainvoke({"text": user_search})
            return json.loads(model_response.content)

        except LangChainException as langchain_error:
            message = f"Error sending prompt to LLM. {langchain_error}"
            raise OpenaiModelCallError(message) from langchain_error
        except openai.APIConnectionError as connection_error:
            message = f"Unable to connect to OpenAI. {connection_error}"
            raise OpenaiModelCallError(message) from connection_error
        except openai.RateLimitError as rate_limit_error:
            message = f"Rate limit exceeded. {rate_limit_error}"
            raise OpenaiModelCallError(message) from rate_limit_error
        except openai.APIError as api_error:
            message = f"OpenAI API error: {api_error}"
            raise OpenaiModelCallError(message) from api_error
