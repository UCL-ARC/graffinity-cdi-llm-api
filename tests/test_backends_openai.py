import asyncio
import json

import openai
import pytest
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from llm_api.backends.openai import OpenaiCaller, OpenaiModelCallError

pytest_plugins = ('pytest_asyncio',)

def test_openai_caller_load_settings(mocker, mock_settings):
    mocked_openai_client = mocker.patch(
        "llm_api.backends.openai.OpenaiCaller.get_client"
    )

    caller = OpenaiCaller(mock_settings)
    expected_test_key = mock_settings.openai_api_key.get_secret_value()

    assert caller.settings.openai_api_key.get_secret_value() == expected_test_key
    mocked_openai_client.assert_called_once()


def test_generate_openai_prompt_success():
    user_input = "What day is it today?"

    expected_output = {"role": "user", "content": user_input}

    prompt_output = OpenaiCaller.generate_openai_prompt(user_input)

    expected_prompt_elements = 4
    assert isinstance(prompt_output, list)
    assert len(prompt_output) == expected_prompt_elements
    assert prompt_output[-1]["role"] == "user"
    assert prompt_output[-1] == expected_output


@pytest.mark.asyncio
async def test_call_model_success(mocker, mock_settings):
    caller = OpenaiCaller(mock_settings)
    test_model = "my-test-gpt-model"

    #mocked_client_call = mocker.patch.object(caller.client.chat.completions, "create")

    expected_example_response_string = '{\n    "name": "William Shakespeare",\n \
        "occupation": "Playwright, poet, actor"}'

    future = asyncio.Future()
    future.set_result(ChatCompletion(
        id="test-id",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(
                    content=expected_example_response_string,
                    role="assistant",
                    function_call=None,
                    tool_calls=None,
                ),
            )
        ],
        created=1699546437,
        model=test_model,
        object="chat.completion",
    )
    )
    mocker.patch.object(
        caller.client.chat.completions,
        "create",
        return_value = future
    )

    test_prompt = [
        {"role": "system", "content": "You are a test system"},
        {"role": "system", "content": "Provide a valid JSON response to the user."},
        {"role": "user", "content": "Who is Shakespeare?"},
    ]

    response = await caller.call_model(test_model, test_prompt)

    assert response == json.loads(expected_example_response_string)


def test_call_model_failure_api_connection_error(mocker, mock_settings):
    caller = OpenaiCaller(mock_settings)
    test_model = "my-test-gpt-model"

    mocked_client_call = mocker.patch.object(caller.client.chat.completions, "create")
    expected_error_message = "Unable to connect to OpenAI. Connection error."
    patched_httpx_request = mocker.patch("httpx.Request")
    mocked_client_call.side_effect = openai.APIConnectionError(
        request=patched_httpx_request
    )

    test_prompt = [
        {"role": "system", "content": "You are a test system"},
        {"role": "system", "content": "Provide a valid JSON response to the user."},
        {"role": "user", "content": "Who is Shakespeare?"},
    ]

    with pytest.raises(OpenaiModelCallError) as exception:
        caller.call_model(test_model, test_prompt)

    assert str(exception.value) == expected_error_message


def test_call_model_failure_rate_limit_error(mocker, mock_settings):
    caller = OpenaiCaller(mock_settings)
    test_model = "my-test-gpt-model"

    mocked_client_call = mocker.patch.object(caller.client.chat.completions, "create")
    unique_test_error_message = "This is a test case - rate limit error."
    expected_error_message = f"Rate limit exceeded. {unique_test_error_message}"
    mocked_response = mocker.patch("httpx.Response")

    mocked_client_call.side_effect = openai.RateLimitError(
        unique_test_error_message, response=mocked_response, body=None
    )

    test_prompt = [
        {"role": "system", "content": "You are a test system"},
        {"role": "system", "content": "Provide a valid JSON response to the user."},
        {"role": "user", "content": "Who is Shakespeare?"},
    ]

    with pytest.raises(OpenaiModelCallError) as exception:
        caller.call_model(test_model, test_prompt)

    assert str(exception.value) == expected_error_message


def test_call_model_failure_api_error(mocker, mock_settings):
    caller = OpenaiCaller(mock_settings)
    test_model = "my-test-gpt-model"

    mocked_client_call = mocker.patch.object(caller.client.chat.completions, "create")
    unique_test_error_message = "This is test case - API Error"
    expected_error_message = f"OpenAI API error: {unique_test_error_message}"

    mocked_request = mocker.patch("httpx.Request")

    mocked_client_call.side_effect = openai.APIError(
        unique_test_error_message, request=mocked_request, body=None
    )

    test_prompt = [
        {"role": "system", "content": "You are a test system"},
        {"role": "system", "content": "Provide a valid JSON response to the user."},
        {"role": "user", "content": "Who is Shakespeare?"},
    ]

    with pytest.raises(OpenaiModelCallError) as exception:
        caller.call_model(test_model, test_prompt)

    assert str(exception.value) == expected_error_message
