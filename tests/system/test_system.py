import json
import os

import pytest
from cv_to_role_analyzer.cv_analyzer import CVAnalyzer


def test_system_analyze_core(mocker):
    """
    System test for the core functionality of the `analyze_core` function in the `cv_analyzer` module.

    This system test evaluates the end-to-end workflow of the application, orchestrated by the `analyze_core`
    function. It ensures that the core functionality of processing CV and job role text is working as expected.

    The test covers:
    1. Successful analysis of CV and job role text, ensuring correct orchestration of the entire pipeline.
    2. Handling of exceptions raised by the `LLMClient` when analyzing a match, verifying proper error handling.

    Args:
        mocker (pytest_mock.MockerFixture): Fixture to mock functions for testing.
    """

    # Mock response to simulate the LLMClient analyze_match function
    mock_response = {
        "match_score": 85,
        "skill_gaps": [{"category": "Tech", "gap": "Java"}],
        "recommendations": ["Learn Java"]
    }
    # Patch the LLMClient.analyze_match method to return mock_response
    mocker.patch("cv_to_role_analyzer.llm.LLMClient.analyze_match", return_value=mock_response)

    # File paths for the test CV and role text
    cv_file_path = "tests/data/test_cv.txt"
    role_file_path = "tests/data/test_role.txt"

    # Check that files exist and are readable
    for file_path in [cv_file_path, role_file_path]:
        assert os.path.exists(file_path), f"File {file_path} does not exist"
        with open(file_path, "r") as f:
            assert f.read(), f"File {file_path} is empty"

    # Read the contents of the CV and role files
    with open(cv_file_path, "r") as f:
        cv_text = f.read()
    with open(role_file_path, "r") as f:
        role_text = f.read()

    # Call the analyze_core function and get the resulting report in JSON format
    report_json = CVAnalyzer.analyze_core(cv_text, role_text)  # Call analyze_core directly
    report = json.loads(report_json)

    # Assert that the returned report matches the mock response
    assert report == mock_response

    # Test with exception in LLMClient.analyze_match to check error handling
    mocker.patch("cv_to_role_analyzer.llm.LLMClient.analyze_match", side_effect=Exception("LLM Error"))

    # Assert that an exception is raised when analyze_match fails
    with pytest.raises(Exception, match="LLM Error"):
        CVAnalyzer.analyze_core(cv_text, role_text)
