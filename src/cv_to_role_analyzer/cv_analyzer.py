import json
import os
import click
from cv_to_role_analyzer.llm import LLMClient
from cv_to_role_analyzer.report import AnalysisReport
from cv_to_role_analyzer.utils import PDFProcessor, RoleProcessor


class CVAnalyzer:
    """
    A class for analyzing CVs against job descriptions.

    This class provides core logic for processing CV and job description texts,
    analyzing their match using an LLM-based approach, and generating a structured
    report. Additionally, it includes a CLI entry point for user interaction,
    orchestrating the application's overall process.

    Methods:
        analyze_core(cv_text, role_text):
            Performs the core analysis of a CV against a job description and returns a JSON report.

        analyze_cli(cv, role, output_dir, verbose):
            Command-line interface for analyzing CVs, processing input files, and generating reports.
            This function orchestrates the application's workflow, handling file extraction, analysis,
            and output generation.
    """
    @staticmethod
    def analyze_core(cv_text, role_text):
        """
        Analyzes a CV against a job description (core logic).

        This function uses the LLMClient to analyze the match between the
        provided CV and job role text. The result is converted into a JSON
        string format through the AnalysisReport.

        Args:
            cv_text (str): The text extracted from the CV.
            role_text (str): The text describing the job role.

        Returns:
            str: A JSON string containing the analysis report.
        """
        analysis = LLMClient.analyze_match(cv_text, role_text)
        return AnalysisReport(analysis).to_json()  # Return JSON string

    @staticmethod
    @click.command()
    @click.option(
        "--cv", required=True, help="Path to the CV PDF file."
    )
    @click.option(
        "--role", required=True, help="Path to the job role text file."
    )
    @click.option(
        "--output-dir", default="analysis_results", help="Path to the output directory (optional)."
    )
    @click.option(
        "--verbose", type=click.IntRange(0, 2), default=1,
        help="Verbosity level (0: silent, 1: summary, 2: full JSON)."
    )
    @click.version_option("1.0")
    def analyze_cli(cv, role, output_dir, verbose):
        """
        CV Analyzer: Analyzes CVs against job roles (CLI entry point).

        This function processes the input CV and job description text,
        analyzes the match using the core logic, and generates an analysis
        report. It can optionally save the result to a specified output directory.

        Args:
            cv (str): The path to the CV PDF file.
            role (str): The path to the job role text file.
            output_dir (str, optional): The directory to save the output report.
            verbose (int): The verbosity level of the output.
        """
        try:
            role_text = RoleProcessor.process(role)
            cv_text = PDFProcessor.extract_text(cv)
            if not role_text or not cv_text:
                return 1

            json_report = CVAnalyzer.analyze_core(cv_text, role_text)  # Call core logic

            if output_dir:
                if os.path.isfile(output_dir):
                    click.echo(f"Error: {output_dir} is a file, not a directory.", err=True)
                    return 1  # Return error code 1
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, "analysis_result.json")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(json_report)
                click.echo(f"Analysis saved to {output_path}")

            if verbose > 0:
                click.echo(json_report if verbose == 2 else "Analysis completed successfully!")

        except FileNotFoundError as e:
            click.echo(f"Error: {e}", err=True)
            click.echo("The specified file was not found.", err=True)
            return 1
        except IsADirectoryError as e:
            click.echo(f"Error: {e}", err=True)
            click.echo("A directory was provided where a file was expected.", err=True)
            return 1
        except PermissionError as e:
            click.echo(f"Permission error: {e}", err=True)
            click.echo("You do not have permission to read the input or write to the output directory.", err=True)
            return 1
        except json.JSONDecodeError as e:
            click.echo(f"JSON error: {e}", err=True)
            click.echo("Failed to decode the JSON report.", err=True)
            return 1
        except ValueError as e:
            click.echo(f"Invalid input error: {e}", err=True)
            click.echo("The provided input files may not be in the expected format.", err=True)
            return 1
        except OSError as e:
            click.echo(f"OS error: {e}", err=True)
            click.echo("There was an error when creating the output directory.", err=True)
            return 1
        except Exception as e:
            click.echo(f"An unexpected error occurred: {e}", err=True)
            click.echo("Analysis failed.", err=True)
            return 1

        return 0  # Return success
