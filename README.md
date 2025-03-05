# CV-to-Role Match Analyzer

## Project Overview

The core functionality of the CV-to-Role Match Analyzer revolves around comparing the skills and qualifications presented in a CV with the requirements outlined in a job description.  This comparison goes beyond simple keyword matching and aims to provide a more nuanced understanding of the candidate's fit.

The output JSON file includes the following key information:

*   **Numerical Match Score (0-100):** A quantitative measure representing the overall compatibility between the CV and the job description.  A higher score indicates a better match.
*   **Categorized Skill Gaps:** Identification of specific skills and qualifications mentioned in the job description that are missing or underrepresented in the CV. These gaps are categorized for clarity (Education, Work Experience, Skills, Certifications).
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
*   Libraries/Frameworks: PyPDF2, Pandas

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
Option A: Using a `.env` File
Create a `.env` file in the project root directory:
```bash
GEMINI_API_KEY=your_api_key_here
```

Option B: Operating System Environment Variable
Set the environment variable directly in your operating system:
Windows (Command Prompt):
```bash
set GOOGLE_API_KEY=your_api_key_here
```
Windows (PowerShell):
```bash
$env:GOOGLE_API_KEY="your_api_key_here"
```
macOS/Linux:
```bash
export GOOGLE_API_KEY=your_api_key_here
```

## Usage Example

#### Sample input files are provided in the `samples/` directory:
- `samples/sample_cv.pdf`: A synthetic CV for testing
- `samples/sample_role.txt`: A sample job description

#### Example usage with sample files:
```bash
# Analyze a CV against a job description
cv-analyzer --cv ./sample_cv.pdf --role ./sample_role.txt

# Analyze with an output directory to store the results as .json
cv-analyzer --cv ./sample_cv.pdf --role ./sample_role.txt --output-dir ./analysis_results

# Analyze with verbose output
cv-analyzer --cv ./sample_cv.pdf --role ./sample_role.txt --verbose 2
```



## Requirements Engineering

#### Functional Feature Requirements:
- **Input Processing (Functional Suitability - Functional Completeness)**
  - FR1.1: The system shall accept PDF format CVs as input files up to 10MB in size.
  - FR1.2: The system shall accept role descriptions as text input up to 2000 characters.
  - FR1.3: The system shall successfully extract text from PDF CVs with 100% text content preservation.
- **Analysis Processing (Functional Suitability - Functional Appropriateness)**
  - FR2.1: The system shall extract and categorize CV components into:
    - Education (degrees, institutions, dates).
    - Work experience (roles, companies, dates, responsibilities).
    - Skills (technical, soft skills).
    - Certifications.
  - FR2.2: The system shall identify from role descriptions:
    - Required education.
    - Required experience level.
    - Required skills (minimum 80% accuracy).
    - Required certifications.
- **Matching Analysis (Functional Suitability - Functional Correctness)**
  - FR3.1: The system shall generate a numerical match score (0-100).
  - FR3.2: The system shall identify all skill gaps and categorize them as:
    - Critical (required but missing).
    - Important (preferred but missing).
    - Nice-to-have (mentioned but missing).
- **Output Generation (Functional Suitability - Functional Completeness)**
  - FR4.1: The system shall generate a JSON report containing:
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
  - AC2: Consistent scoring (±5% variance for same inputs).
- **Skill Gap Identification**
  - AC3: 90% accuracy in identifying critical gaps.
#### [LLM Interaction Documentation](./chats/requirements_engineering_LLM_interactions.txt)

## Architecture
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
- PDF processing and text extraction.
- Data structuring and analysis.
- Large Language Model (LLM) API integration.
- Command-line interface management.
- Data validation.

#### Team Member Responsibilities
The project is divided into two main areas of responsibility:
- Data Handling and Interface: This area encompasses managing input data (CV and role description), interacting with the file system, and providing the command-line interface.
- Analysis and LLM Integration: This area focuses on integrating with the LLM API, developing the analysis algorithms, and generating the final report.

Both team members share responsibility for code review, documentation, integration testing, and performance optimization.
#### [LLM Interaction Documentation](./chats/architecture_LLM_chats.txt)

## Design
#### CRC Description of Key Classes:
- **CVAnalyzer**
  - *Responsibilities*
    - Coordinates the overall analysis process
    - Extracts text from CV PDFs
    - Processes role descriptions
    - Generates match analysis reports
    - Manages LLM interactions for analysis
  - *Collaborators*
    - AnalysisReport
    - SkillGap
    - LLM Client (external)
    - PDF Processor (external)
- **AnalysisReport**
  - *Responsibilities*
    - Holds analysis results (match score, gaps, recommendations)
    - Converts analysis data to JSON format
    - Validates score ranges (0-100)
    - Maintains structured representation of analysis results
  - *Collaborators*
    - SkillGap
    - JSON library (external)
- **SkillGap**
  - *Responsibilities*
    - Represents a single identified skill gap
    - Stores gap category and description
    - Associates gap with importance level (critical/important/nice-to-have)
  - *Collaborators*
    - SkillGapType
- **SkillGapType**
  - *Responsibilities*
    - Defines valid gap importance levels
    - Ensures type safety for gap classifications
    - Provides string representation of gap types
  - *Collaborators*
    - None (Pure enumeration)
#### [LLM Interaction Documentation](./chats/design_LLM_interactions.txt)

## Coding & Testing

### Coding
- **Code Quality:** Adherence to clean coding practices and PEP 8.
- **Project File Structure:**
  
| File Name | Description |
|-----------|-------------|
| `main.py` | Entry point for the project |
| `utils.py` | Utility functions |
| `config.json` | Configuration settings |

### Testing
- **Automated Unit Test:** (Inline description & link to test file)
- **System-level Functional Test:** (Inline description & link to test file)
- [LLM Interaction Documentation](link-to-llm-docs)

