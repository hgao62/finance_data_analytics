## 🚀 Running the Project

### Prerequisites

- **Python 3.7.9** installed on your system.
- **Virtual Environment** set up as described in the [Setup](#setup) section.

### Automated Workflow

Depending on your operating system, use the appropriate script to generate data and run the analysis.

- **Windows:**
  - Double-click `run_analysis.bat` in the project root directory.
  - Or execute via Command Prompt:
    ```batch
    run_analysis.bat
    ```

- **Unix-based Systems (Linux/MacOS):**
  - Make the script executable (if not already done):
    ```bash
    chmod +x run_analysis.sh
    ```
  - Run the script:
    ```bash
    ./run_analysis.sh
    ```

### Viewing Results

- **Charts:** Located in the `charts/` directory.
- **Executive Summary:** Open `reports/executive_summary.md` using a Markdown viewer or any text editor that supports Markdown.

### Running Tests

After setting up the environment, run the tests to ensure everything is functioning correctly.

```bash
pytest
