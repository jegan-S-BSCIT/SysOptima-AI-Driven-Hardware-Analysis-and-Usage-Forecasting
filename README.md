# SysOptima: AI-Driven Hardware Analysis and Usage Forecasting

SysOptima is a Python-based **desktop application** built for B.Sc IT final-year project work. It runs completely on the user's local computer and helps analyze system performance, monitor live usage, detect bottlenecks, and predict capability for common workloads such as gaming, video editing, and productivity.

## Desktop Application Focus
- This project is a **local desktop application**.
- It uses a Tkinter GUI and executes on the user's machine.
- It is **not** a web application and does not require cloud deployment.

## Problem Statement
Many users do not know whether their current system can handle modern workloads efficiently. Raw hardware specs are difficult to interpret, and users often struggle to identify the real cause of poor performance.

## Solution Approach
SysOptima solves this by combining hardware inspection, real-time monitoring, benchmarking, diagnostics, and AI-driven explanations in one desktop interface. The application converts technical measurements into understandable scores, bottleneck insights, and practical recommendations.

## Key Features
- **Hardware Detection**
  - Detects CPU, RAM, storage, battery, and GPU details.
- **Real-Time Monitoring**
  - Tracks CPU, memory, disk, and GPU usage live.
- **Lightweight Benchmarking**
  - Runs CPU, memory, and disk benchmark routines.
- **Diagnostics and Bottleneck Detection**
  - Finds weak components and potential system limitations.
- **Performance Prediction**
  - Estimates system capability for gaming, video editing, and productivity tasks.
- **AI-Based Guidance**
  - Generates explanations and recommendations in simple language.

## System Architecture (Simple)
1. **Input Layer**: Collects hardware and live usage data from the local machine.
2. **Processing Layer**: Executes benchmarks, normalizes scores, and runs diagnostics logic.
3. **AI/Prediction Layer**: Applies ML/rule-based logic to estimate workload readiness.
4. **Presentation Layer**: Displays results and recommendations through the Tkinter desktop UI.

## AI Techniques Used
- **Rule-Based Expert Logic**
  - For diagnostics and recommendation generation.
- **Decision Tree Models**
  - For classification-style capability prediction.
- **Regression Models**
  - For score estimation and workload forecasting.

## Technologies Used
- **Language**: Python
- **Desktop GUI**: Tkinter
- **System Monitoring**: psutil, GPUtil
- **Data Handling**: pandas, numpy
- **Machine Learning**: scikit-learn
- **Visualization**: matplotlib

## Installation
### Prerequisites
- Python 3.8 or above
- Windows (recommended for full hardware reporting)

### Steps
```bash
pip install -r requirements.txt
```

## Run the Desktop Application
```bash
python main.py
```

## Project Structure
```text
SysOptima/
├── main.py                    # Desktop application entry point
├── app.py                     # Alternate launcher/support entry
├── requirements.txt           # Python dependencies
├── core/                      # Hardware detection, monitoring, AI assistants
├── benchmark/                 # CPU, memory, disk benchmark modules
├── analysis/                  # Diagnostics, score normalization, predictor logic
├── desktop_ui/                # Main desktop UI windows and views
├── ui/                        # Additional UI components
├── data/                      # Dataset/history/reference files
├── docs/                      # Documentation and project notes
└── README.md                  # Project overview and usage guide
```

## Sample Output (What Results Mean)
- **Performance Scores (0-100)**
  - Overall and component-wise scores for CPU, memory, storage, and GPU.
- **Bottleneck Findings**
  - Identifies which component is limiting performance.
- **Capability Predictions**
  - Indicates expected suitability for gaming, video editing, and productivity.
- **Recommendations**
  - Suggests practical actions such as hardware upgrades or optimization steps.

## Why This Project Is Useful
- Helps users make informed upgrade decisions.
- Translates technical metrics into easy insights.
- Demonstrates practical use of AI in system diagnostics.
- Suitable for academic viva and portfolio presentation.

## License
This project is released under the **MIT License**. See the LICENSE file for details.

## Author
**Jegan S**  
B.Sc Information Technology - Final Year Project
