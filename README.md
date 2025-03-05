# CV-to-Role Match Analyzer

## Project Overview

The core functionality of the CV-to-Role Match Analyzer revolves around comparing the skills and qualifications presented in a CV with the requirements outlined in a job description.  This comparison goes beyond simple keyword matching and aims to provide a more nuanced understanding of the candidate's fit.

The output JSON file includes the following key information:

*   **Numerical Match Score (0-100):** A quantitative measure representing the overall compatibility between the CV and the job description.  A higher score indicates a better match.
*   **Categorized Skill Gaps:** Identification of specific skills and qualifications mentioned in the job description that are missing or underrepresented in the CV.
*   **Specific Improvement Recommendations:**  Actionable suggestions for the candidate to improve their CV and better align it with the target role.  These recommendations might include highlighting relevant projects, acquiring new skills, or rephrasing existing experience.

#### Key Features

*   **Automated Analysis:**  Eliminates the need for manual CV screening, saving recruiters valuable time.
*   **Objective Evaluation:**  Provides a data-driven approach to candidate assessment, reducing bias and promoting fairness.
*   **Detailed Insights:**  Offers granular information about skill gaps and areas for improvement, facilitating more targeted feedback.
*   **JSON Output:**  Enables easy integration with other recruitment systems and tools.
*   **PDF Input:** Accepts CVs and Job Descriptions in the commonly used PDF format.

#### Target Audience

This tool is beneficial for:

*   **Recruiters:**  Quickly identify qualified candidates and prioritize their applications.
*   **Hiring Managers:**  Gain a deeper understanding of candidate strengths and weaknesses.
*   **Job Seekers:**  Identify areas where their CV can be improved to better match target roles.

#### Technical Stack

*   Programming Language: Python
*   Libraries/Frameworks: click, google-genai, python-dotenv, pytest, pypdf

## Installation Guide

#### Prerequisites
- Python 3.8+
- pip (Python package manager)
- A Gemini API Key (Instructions for obtaining provided below)

#### Obtaining a Gemini API Key
1. Visit https://ai.google.dev/gemini-api/docs/api-key
2. Click "Get a Gemini API key in Google AI Studio"
3. Click "Create API Key"
4. Copy the generated key
5. Prepare to use the key in your project setup

#### Installation
1. Clone the Repository
```bash
git clone https://github.com/og-sw-projects/CV-to-Role-Match-Analyzer.git
cd CV-to-Role-Match-Analyzer
```
2. Create a Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
3. Install Dependencies
```bash
pip install .
```

4. Set Up API Key

You have two options for providing the Gemini API key:
- *Option A*: Create a `.env` file in the project root directory:
```bash
GEMINI_API_KEY=your_api_key_here
```

- *Option B*: Set the environment variable directly in your operating system:
```bash
# If on Windows Command Prompt
set GOOGLE_API_KEY=your_api_key_here

# If on Windows PowerShell
$env:GOOGLE_API_KEY="your_api_key_here"

# If on macOS/Linux
export GOOGLE_API_KEY=your_api_key_here
```
## Usage

#### Sample input files are provided in the [samples/](./samples) directory:
- [samples/sample_cv.pdf](./samples/sample_cv.pdf): A synthetic CV for testing
- [samples/sample_role.txt](./samples/sample_role.txt): A sample job description

#### Example usage with sample files:
```bash
# Analyze a CV against a job description
cv-analyzer --cv ./sample_cv.pdf --role ./sample_role.txt

# Analyze with an output directory to store the results as .json
cv-analyzer --cv ./sample_cv.pdf --role ./sample_role.txt --output-dir ./analysis_results

# Analyze with verbose output
cv-analyzer --cv ./sample_cv.pdf --role ./sample_role.txt --verbose 2
```

## Project Phases - Requirements Engineering

#### Functional Feature Requirements:
- **Input Processing (Functional Suitability - Functional Completeness)**
  - FR1.1: The system shall accept PDF format CVs as input files up to 10MB in size.
  - FR1.2: The system shall accept role descriptions as text input up to 2000 characters.
  - FR1.3: The system shall successfully extract text from PDF CVs with 100% text content preservation.
- **Matching Analysis (Functional Suitability - Functional Correctness)**
  - FR2.1: The system shall generate a numerical match score (0-100).
- **Output Generation (Functional Suitability - Functional Completeness)**
  - FR3.1: The system shall generate a JSON report containing:
    - Overall match score.
    - Categorized skill gaps.
    - Specific improvement recommendations.
#### Non-Functional Feature Requirements:
- **Performance Efficiency (Time Behavior)**
  - NFR1.1: The system shall complete analysis within 30 seconds.
- **Reliability (Maturity)**
  - NFR2.1: The system shall maintain 95% accuracy in requirement identification.
- **Security (Confidentiality)**
  - NFR3.1: The system shall not persist any CV data beyond the analysis session.
#### Acceptance Criteria:
- **PDF Processing**
  - AC1: Complete text extraction with preserved formatting for PDFs of sizes 1KB to 10MB.
- **Match Score Accuracy**
  - AC2: Consistent scoring (±10% variance for same inputs).
- **Skill Gap Identification**
  - AC3: 90% accuracy in identifying critical gaps.
#### [Requirements Engineering LLM Interactions Documentation](./chats/requirements_engineering_LLM_interactions.txt)

## Projet Phases - Architecture
#### Command-line Interface Specification
```bash
# Main analysis command
cvanalyzer analyze --cv <path_to_pdf> --role <path_to_txt>

# Optional parameters
cvanalyzer analyze --cv <path_to_pdf> --role <path_to_txt> --output-dir <path>
cvanalyzer analyze --cv <path_to_pdf> --role <path_to_txt> --verbose [0|1|2]

# Utility commands
cvanalyzer --help
cvanalyzer --version
```
#### File System Interactions
The system interacts with files in the following manner:
- Input Files:
  - CV: PDF format.
  - Role Description: Text file.
- Output Files:
  - Analysis Report: JSON format containing match score, skill gaps, and recommendations. Output directory can be specified via command line. If not specified, a default output location will be used.
- Temporary Files:
  - The system utilizes temporary files during analysis. These files are automatically managed and cleaned up by the system.

#### Third-Party Libraries
The system leverages third-party libraries for specific functionalities:
- `click` - Command-line interface management.
- `google-genai` - Large Language Model (LLM) API integration.
- `python-dotenv` - Environment variables management.
- `pytest` - Testing
- `pytest-mock` - Mock for testing
- `pypdf` - PDF processing and text extraction.

#### Team Member Responsibilities
The project is divided into two main areas of responsibility:
- Data Handling and Interface: This area encompasses managing input data (CV and role description), interacting with the file system, and providing the command-line interface.
- Analysis and LLM Integration: This area focuses on integrating with the LLM API, developing the analysis algorithms, and generating the final report.

Both team members share responsibility for code review, documentation, integration testing, and performance optimization.
#### [Architecture LLM Interactions Documentation](./chats/architecture_LLM_chats.txt)

## Project Phases - Design
#### CRC Description of Key Classes:
- **CVAnalyzer**
  - *Responsibilities*
    - Perform the core analysis of a CV against a job description.
    - Process input files and orchestrate the application workflow via the CLI.
    - Handle file I/O for saving analysis reports in JSON format.
  - *Collaborators*
    - LLMClient: Used for analyzing the match between the CV and the job description.
    - RoleProcessor: Used to process the job description file.
    - PDFProcessor: Used to extract text from the CV (PDF).
    - AnalysisReport: Used to generate and format the analysis result into a JSON string.
- **LLMClient**
  - *Responsibilities*
    - Interact with the Gemini API to analyze the CV and job description match.
    - Generate optimized prompts for the LLM and handle responses.
    - Refine prompts and responses if initial results are incomplete.
  - *Collaborators*
    - None
- **AnalysisReport**
  - *Responsibilities*
    - Represents the results of a CV and job description analysis.
    - Store and format the match score, skill gaps, and recommendations.
    - Convert the analysis data into a JSON string.
  - *Collaborators*
    - None
- **RoleProcessor**
  - *Responsibilities*
    - Process the job role description text from a file.
  - *Collaborators*
    - None
- **PDFProcessor**
  - *Responsibilities*
    - Extract text from a PDF file (CV).
  - *Collaborators*
    - None
- **AnalysisRequest**
  - *Responsibilities*
    - Validate the existence of the CV and job description files.
    - Process the input files into a dictionary format.
  - *Collaborators*
    - None

#### [Design LLM Interactions Documentation](./chats/design_LLM_interactions.txt)

## Project Phases - Coding & Testing

### Coding
  
| File Name | Description |
|-----------|-------------|
| `cv_analyzer.py` | ontains the core logic for analyzing CVs and job descriptions, orchestrating the overall flow of analysis, and managing the command-line interface using Click. |
| `llm.py` | Manages the interaction with the Gemini API for analyzing the match between the CV and job description using an LLM-based approach. |
| `report.py` | Responsible for formatting and outputting the analysis results in a structured format (e.g., JSON), representing the CV-job description match. |
| `utils.py` | Contains helper functions for tasks like file handling, text extraction, and other common operations that support the core functionality. |
| `validation.py` | Validates the input paths (CV and job description files), ensuring that files exist and are in the correct format before analysis. |

### Testing
- **Automated Unit Test** [test_analyze_match.py](./tests/unit/test_analyze_match.py): A unit test for the `analyze_match` function in the `LLMClient` class. This test checks various scenarios of matching CV and job role text including successful match with valid responses and handling of exceptions when `LLMClient.analyze_match` raises an error.

- **System-level Functional Test** [test_system.py](./tests/system/test_system.py): A system test for the core functionality of the `analyze_core` function in the `CVAnalyzer` class. This system test evaluates the end-to-end workflow of the application, orchestrated by the `analyze_core` function. It ensures that the core functionality of processing CV and job role text is working as expected.

#### [Testing LLM Interactions Documentation](./chats/testing_LLM_interactions.txt)

