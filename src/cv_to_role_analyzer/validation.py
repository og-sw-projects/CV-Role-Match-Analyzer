import os


class AnalysisRequest:
    """
    A class to handle the validation and processing of CV and job description inputs.

    Methods:
        validate(cv, role_text): Validates that the CV and job description files exist.
        process(cv, role_text): Validates the inputs and processes the data into a dictionary.
    """

    @staticmethod
    def validate(cv, role_text):
        """Validates input parameters to ensure that the CV and role description files exist.

        Args:
            cv (str): Path to the CV file.
            role_text (str): Path to the job description file.

        Raises:
            FileNotFoundError: If either the CV or role description file does not exist.
        """
        if not os.path.exists(cv):
            raise FileNotFoundError(f"The CV file {cv} does not exist.")
        if not os.path.exists(role_text):
            raise FileNotFoundError(f"The job description {role_text} does not exist.")

    @staticmethod
    def process(cv, role_text):
        """Validates the input files and processes them into a dictionary.

        Args:
            cv (str): Path to the CV file.
            role_text (str): Path to the job description file.

        Returns:
            dict: A dictionary containing the paths of the CV and role description files.

        Raises:
            FileNotFoundError: If validation of the input files fails.
        """
        AnalysisRequest.validate(cv, role_text)
        return {"cv": cv, "role_text": role_text}
