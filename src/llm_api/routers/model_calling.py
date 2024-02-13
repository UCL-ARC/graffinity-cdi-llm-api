"""Define router containing model calling logic."""

import time

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel

from llm_api.backends.bedrock import BedrockCaller, BedrockModelCallError
from llm_api.backends.openai import OpenaiCaller, OpenaiModelCallError
from llm_api.config import BedrockModel, Settings, get_settings

router = APIRouter()


class ModelCallingError(HTTPException):
    """
    Custom exception for failing model calls.

    Args:
        HTTPException (_type_): HTTPException with status code.
    """

    def __init__(self, status_code: int, detail: str | None = None) -> None:
        """
        Class constructor.

        Args:
            status_code (int): HTTP response status code
            detail (str | None, optional):
                Additional exception details. Defaults to None.
        """
        if not detail:
            detail = "Error calling model."
        super().__init__(status_code, detail=detail)


class InputDataSpec(BaseModel):
    """
    Data required in each POST request.

    A Pydantic model to validate HTTP POST requests.

    Args:
        BaseModel (_type_): Pydantic BaseModel

    Attributes:
        user_search (str): A user's search as a string. Required variable.
    """

    user_search: str


@router.post("/call_model_openai")
async def call_model_openai(
    request_body: InputDataSpec,
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> dict:
    """
    Call an OpenAI language model with the provided user search as prompt input.

    Args:
        request_body (InputDataSpec): Request body for post requests, containing user search.
        settings (settings): Injected settings object to provide API keys and model names.
            Is fetched from server-side.

    Raises:
        ModelCallingError: HTTP status code raised in the case of a bad model call, without
            having the API fall over.

    Returns:
        _type_: _description_
    """
    start_time = time.time()
    caller = OpenaiCaller(settings)

    prompt_template = OpenaiCaller.generate_openai_prompt()
    try:
        model_response = await caller.call_model(prompt_template, request_body.user_search)
        model_response.update({"user_search": request_body.user_search})
        end_time = time.time()
        logger.info(f"GPT4: {end_time - start_time}s")
        return model_response  # noqa: TRY300
    except OpenaiModelCallError as model_call_error:
        raise ModelCallingError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calling model. {model_call_error}",
        ) from model_call_error


@router.post("/call_model_bedrock")
async def call_model_bedrock(
    request_body: InputDataSpec,
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> dict:
    """
    Call the Claude v2 Large Language Model via AWS Bedrock with a user search as prompt input.

    Args:
        request_body (InputDataSpec): Request body for post requests, containing user search.
        settings (settings): Injected settings object to provide API keys and model names.
            Is fetched from server-side.

    Raises:
        ModelCallingError: HTTP status code raised in the case of a bad model call, without
            having the API fall over.

    Returns:
        _type_: _description_
    """
    start_time = time.time()
    caller = BedrockCaller(settings)

    prompt_template = BedrockCaller.generate_prompt()
    try:
        model_response = await caller.call_model(prompt_template, request_body.user_search)
        model_response.update({"user_search": request_body.user_search})
        end_time = time.time()
        logger.info(f"Claude 2: {end_time - start_time}s")
        return model_response  # noqa: TRY300
    except BedrockModelCallError as model_call_error:
        raise ModelCallingError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calling model. {model_call_error}",
        ) from model_call_error


@router.post("/call_model_bedrock_instant")
async def call_model_bedrock_instant(
    request_body: InputDataSpec,
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> dict:
    """
    Call the Claude Instant v1.2 Large Language Model via AWS Bedrock with a user search.

    Args:
        request_body (InputDataSpec): Request body for post requests, containing user search.
        settings (settings): Injected settings object to provide API keys and model names.
            Is fetched from server-side.

    Raises:
        ModelCallingError: HTTP status code raised in the case of a bad model call, without
            having the API fall over.

    Returns:
        _type_: _description_
    """
    start_time = time.time()
    caller = BedrockCaller(settings)

    prompt_template = BedrockCaller.generate_prompt()
    try:
        model_response = await caller.call_model(
            prompt_template, request_body.user_search, alternative_model=BedrockModel.CLAUDE_INSTANT
        )
        model_response.update({"user_search": request_body.user_search})
        end_time = time.time()
        logger.info(f"Claude instant v1.2 {end_time - start_time}s")
        return model_response  # noqa: TRY300
    except BedrockModelCallError as model_call_error:
        raise ModelCallingError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calling model. {model_call_error}",
        ) from model_call_error


@router.post("/call_model_bedrock_sync")
def call_model_bedrock_sync(
    request_body: InputDataSpec,
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> dict:
    """
    Call the Claude v2 Large Language Model via AWS Bedrock with a user search as prompt input.

    Args:
        request_body (InputDataSpec): Request body for post requests, containing user search.
        settings (settings): Injected settings object to provide API keys and model names.
            Is fetched from server-side.

    Raises:
        ModelCallingError: HTTP status code raised in the case of a bad model call, without
            having the API fall over.

    Returns:
        _type_: _description_
    """
    start_time = time.time()
    caller = BedrockCaller(settings)

    prompt_template = BedrockCaller.generate_prompt()
    try:
        model_response = caller.call_model_sync(prompt_template, request_body.user_search)
        model_response.update({"user_search": request_body.user_search})
        end_time = time.time()
        logger.info(f"Claude 2: {end_time - start_time}s")
        return model_response  # noqa: TRY300
    except BedrockModelCallError as model_call_error:
        raise ModelCallingError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calling model. {model_call_error}",
        ) from model_call_error


@router.post("/call_model_bedrock_instant_sync")
def call_model_bedrock_instant_sync(
    request_body: InputDataSpec,
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> dict:
    """
    Call the Claude Instant v1.2 Large Language Model via AWS Bedrock with a user search.

    Args:
        request_body (InputDataSpec): Request body for post requests, containing user search.
        settings (settings): Injected settings object to provide API keys and model names.
            Is fetched from server-side.

    Raises:
        ModelCallingError: HTTP status code raised in the case of a bad model call, without
            having the API fall over.

    Returns:
        _type_: _description_
    """
    start_time = time.time()
    caller = BedrockCaller(settings)

    prompt_template = BedrockCaller.generate_prompt()
    try:
        model_response = caller.call_model_sync(
            prompt_template, request_body.user_search, alternative_model=BedrockModel.CLAUDE_INSTANT
        )
        model_response.update({"user_search": request_body.user_search})
        end_time = time.time()
        logger.info(f"Claude instant v1.2 {end_time - start_time}s")
        return model_response  # noqa: TRY300
    except BedrockModelCallError as model_call_error:
        raise ModelCallingError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calling model. {model_call_error}",
        ) from model_call_error
