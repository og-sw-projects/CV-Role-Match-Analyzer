import pypdf
import click


class RoleProcessor:
    """
    A class responsible for processing job role description files.

    Methods:
        process(role_path): Reads the job role description from a text file and returns it as a string.
    """

    @staticmethod
    def process(role_path):
        """Reads job role description from a text file.

        Args:
            role_path (str): The file path to the job role description text file.

        Returns:
            str: The contents of the role description file as a string, with leading
                 and trailing whitespace removed.

        Raises:
            FileNotFoundError: If the file at the specified path is not found.
            IOError: If an error occurs while reading the file.
        """
        try:
            with open(role_path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            click.echo(f"Error: The file at {role_path} was not found.")
            return None
        except IOError as e:
            click.echo(f"Error reading the file {role_path}: {e}")
            return None


class PDFProcessor:
    """
    A class responsible for extracting text from PDF files.

    Methods:
        extract_text(pdf_path): Extracts text from a given PDF file and returns it as a string.
    """

    @staticmethod
    def extract_text(pdf_path):
        """Extracts text from a given PDF file.

        Args:
            pdf_path (str): The file path to the PDF document.

        Returns:
            str: The extracted text from the PDF, or None if no text could be extracted.

        Raises:
            FileNotFoundError: If the PDF file at the specified path is not found.
            IOError: If an error occurs while reading the PDF file.
        """
        try:
            with open(pdf_path, "rb") as file:
                reader = pypdf.PdfReader(file)
                text = []
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
                return " ".join(text) if text else None
        except FileNotFoundError:
            click.echo(f"Error: The PDF file at {pdf_path} was not found.")
            return None
        except IOError as e:
            click.echo(f"Error reading the PDF file {pdf_path}: {e}")
            return None
