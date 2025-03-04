import pytest
import json
from cv_to_role_analyzer.cv_analyzer import analyze_core


@pytest.mark.parametrize(
    "mock_response, cv_text, role_text, raises_exception, exception_message",
    [
        (  # Test case 1: Successful match
            {"match_score": 85, "skill_gaps": [{"category": "Tech", "gap": "Java"}], "recommendations": ["Learn Java"]},
            "Mock CV Text",
            "Mock Role Text",
            False,  # Does not raise an exception
            None,
        ),
        (  # Test case 2: Different match
            {"match_score": 92, "skill_gaps": [], "recommendations": ["Improve communication"]},
            "Mock CV Text",
            "Mock Role Text",
            False,
            None,
        ),
        (  # Test case 3: Empty CV
            {"match_score": 0, "skill_gaps": [], "recommendations": ["Provide a CV"]},
            "",
            "Mock Role Text",
            False,
            None,
        ),
        (  # Test case 4: Empty Role
            {"match_score": 0, "skill_gaps": [], "recommendations": ["Provide a job description"]},
            "Mock CV Text",
            "",
            False,
            None,
        ),
        (  # Test case 5: Special characters in CV
            {"match_score": 70, "skill_gaps": [], "recommendations": ["Review CV for special characters"]},
            "Mock CV Text with !@#$%^&*()",
            "Mock Role Text",
            False,
            None,
        ),
        (  # Test case 6: LLM error (exception case)
            None,  # No mock response for exception
            "Mock CV Text",
            "Mock Role Text",
            True,  # Raises an exception
            "LLM Error",  # Exception message
        ),
    ],
)
def test_analyze_core(mocker, mock_response, cv_text, role_text, raises_exception, exception_message):
    """
    Unit test for the `analyze_core` function in the `cv_analyzer` module.

    This test checks various scenarios of analyzing a CV and job role text:
    1. Successful analysis with valid responses.
    2. Handling of exceptions when the `LLMClient.analyze_match` raises an error.

    Args:
        mocker (pytest_mock.MockerFixture): Fixture to mock functions for testing.
        mock_response (dict): Mocked response from the LLMClient when no exception occurs.
        cv_text (str): CV text to be analyzed.
        role_text (str): Role description text to be analyzed.
        raises_exception (bool): Flag indicating if an exception should be raised.
        exception_message (str): Exception message to be matched when `raises_exception` is True.

    Raises:
        Exception: If `raises_exception` is True, an exception with `exception_message` is raised.
    """
    if raises_exception:
        # Mocking LLMClient to raise an exception
        mocker.patch("cv_to_role_analyzer.llm.LLMClient.analyze_match", side_effect=Exception(exception_message))
        with pytest.raises(Exception, match=exception_message):
            analyze_core(cv_text, role_text)
    else:
        # Mocking LLMClient to return a mock response
        mocker.patch("cv_to_role_analyzer.llm.LLMClient.analyze_match", return_value=mock_response)
        # Call the analyze_core function and assert the result
        report_json = analyze_core(cv_text, role_text)
        report = json.loads(report_json)
        assert report == mock_response
