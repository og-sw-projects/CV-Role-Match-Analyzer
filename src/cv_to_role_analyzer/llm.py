import copy
import json
import os
import re

import click
from dotenv import load_dotenv
from google.genai import Client, errors
from google.genai.types import Content, Part


class LLMClient:
    """
    A client class for interacting with the Gemini API to analyze the match between a CV and a job description.

    This class handles the process of generating an optimized prompt, calling the Gemini API to analyze the match,
    refining the prompt if the response is incomplete, and processing the response.

    Methods:
        analyze_match(cv_text, role_text):
            Analyzes the CV against the job description by generating a prompt, calling the Gemini API, and refining
            the prompt if necessary.

        _generate_prompt(cv_text, role_text):
            Creates an optimized LLM prompt using few-shot learning and structured reasoning.

        _call_llm_api(prompt):
            Calls the Gemini API with the given prompt and parses the response into a dictionary.

        _refine_prompt(prompt, response):
            Refines the prompt if the initial LLM response is incomplete.
    """

    @staticmethod
    def analyze_match(cv_text, role_text):
        """
        Generates an optimized prompt and calls Gemini API.

        Args:
            cv_text (str): The CV text to analyze.
            role_text (str): The job description text.

        Returns:
            dict: The response from the Gemini API containing match score, skill gaps, and recommendations.
        """

        prompt = LLMClient._generate_prompt(cv_text, role_text)
        response = LLMClient._call_llm_api(prompt)

        # If response lacks required fields, retry with a refined prompt
        if not response or not {"match_score", "skill_gap", "recommendations"}.issubset(response.keys()):
            response = LLMClient._call_llm_api(LLMClient._refine_prompt(prompt, response))
            return response

        if len(response["skill_gap"]) > 0 and len(response["recommendations"]) == 0:
            response = LLMClient._call_llm_api(LLMClient._refine_prompt(prompt, response))
            return response

        return response

    @staticmethod
    def _generate_prompt(cv_text, role_text):
        """
        Creates a LLM prompt.

        Args:
            cv_text (str): The CV text to analyze.
            role_text (str): The job description text.

        Returns:
            Content: The optimized LLM prompt.
        """
        prompt = Content(parts=[
            # Role
            Part(text="You are an advanced AI specializing in CV analysis."),
            # Instructions
            Part(text=(
                f"Identify *all* significant skill gaps, even if there are many. Do not omit any important gaps. "
                f"Evaluate the candidate’s CV against the job description and provide the results in JSON format with "
                f"the following keys:"
                f"\n- {repr('match_score')} (integer, 0-100)"
                f"\n- {repr('skill_gaps')} (list of dictionaries, each with {repr('category')} and {repr('gap')} keys)"
                f"\n- {repr('recommendations')} (list of strings)"
                f"\n\nUse structured reasoning before generating the JSON. Ensure the JSON is valid and parsable."
            )),
            # CV Text
            Part(text=f"CV Text: \n{cv_text}"),
            # Role Description
            Part(text=f"Role Description: \n{role_text}"),
        ])

        return prompt

    @staticmethod
    def _call_llm_api(prompt):
        """
        Calls the Gemini API with the given prompt, parses the JSON response, and returns it as a dictionary.

        Args:
            prompt (Content): The prompt content to send to the API.

        Returns:
            dict: The parsed JSON response from the Gemini API, or None if error.
        """
        try:
            # Load environment variables from .env file and get API key from environment
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable not set. Please check your environment "
                                 "configuration.")

            # Initialize Gemini client and generate content
            client = Client(api_key=api_key)
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

            # Extract response text, find JSON object, parse, and return
            response_text = response.candidates[0].content.parts[0].text
            match = re.search(r"{.*}", response_text, re.DOTALL)
            return json.loads(match.group(0))

        except (
                errors.ClientError,
                errors.APIError,
                errors.FunctionInvocationError,
                errors.ExperimentalWarning,
                errors.UnknownFunctionCallArgumentError,
                errors.UnsupportedFunctionError,
        ) as e:
            click.echo(f"GenAI Error: {type(e).__name__}: {e}. Please verify the API request and retry.", err=True)
        except json.JSONDecodeError as e:
            click.echo(f"Error decoding JSON response: {e}. The response may be not in the expected format.", err=True)
        except ValueError as e:
            click.echo(f"Environment Error: {e}. Please ensure your GEMINI_API_KEY is correctly set in your "
                       f"environment.", err=True)
        except Exception as e:  # Catch other potential errors (e.g., network issues)
            click.echo(f"An unexpected error occurred: {e}. Please check your network or API configuration.", err=True)

    @staticmethod
    def _refine_prompt(prompt, response):
        """
        Refines the prompt if the initial LLM response is incomplete.

        Args:
            prompt (Content): The original prompt to refine.
            response (dict): The original response that needs refinement.

        Returns:
            Content: The refined prompt.
        """
        refined_prompt = copy.deepcopy(prompt)
        refined_prompt.parts.append(Part(text="\nEnsure all required fields are included."))
        refined_prompt.parts.append(Part(text=f"\nPrevious response: {response}"))
        return refined_prompt
