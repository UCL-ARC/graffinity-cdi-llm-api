"""Define router containing model calling logic."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from llm_api.backends.openai import OpenaiCaller, OpenaiModelCallError
from llm_api.config import Settings, get_settings

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


@router.post("/call_model")
async def call_language_model(
    user_search: InputDataSpec,
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> dict:
    """
    Call a language model with the provided user search as prompt input.

    Args:
        user_search (InputDataSpec): Request body format for post requests.
        settings (settings): Injected settings object to provide API keys and model names.
            Is fetched from server-side.

    Raises:
        ModelCallingError: HTTP status code raised in the case of a bad model call, without
            having the API fall over.

    Returns:
        _type_: _description_
    """
    caller = OpenaiCaller(settings)

    full_prompt = OpenaiCaller.generate_openai_prompt(user_search.user_search)
    try:
        model_response = await caller.call_model(settings.llm_name, full_prompt)
        model_response.update({"user_search": user_search.user_search})
        return model_response  # noqa: TRY300
    except OpenaiModelCallError as model_call_error:
        raise ModelCallingError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calling model. {model_call_error}",
        ) from model_call_error
