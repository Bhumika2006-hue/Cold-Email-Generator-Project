# Cold Email Generator

## Overview
The Cold Email Generator is a web application designed to assist users in generating tailored cold emails for job applications and outreach. The application provides two distinct interfaces: one for students seeking job opportunities and another for college placement officers managing outreach to companies.

## Features
- **User Selection**: Users can choose between a student interface and a college placement officer interface at the start.
- **Job Information Extraction**: The application extracts job postings from specified URLs and presents them to the user.
- **Email Generation**: Based on the extracted job information and user input, the application generates professional cold emails.
- **Portfolio Management**: Users can manage and query a portfolio of relevant links to enhance their email content.

## Project Structure
```
cold-email-generator
├── app
│   ├── main.py                     # Entry point for the Streamlit app
│   ├── studentChains.py            # Handles interactions with the language model for students
│   ├── chains.py                   # Handles interactions with the language model for placement officers
│   ├── portfolio.py                # Manages portfolio data
│   ├── utils.py                    # Utility functions for data processing
│   ├── pages
│   │   ├── student_mode.py         # Interface for students
│   │   └── placement_officer_mode.py # Interface for placement officers
├── resources
│   └── my_portfolio.csv            # Portfolio data in CSV format
├── .env                             # Environment variables
├── .gitignore                       # Files to ignore in version control
├── requirements.txt                 # Dependencies for the application
├── config.py                        # Configuration settings
└── README.md                        # Documentation for the project
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd cold-email-generator
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up your environment variables in the `.env` file.

## Usage
1. Run the application:
   ```
   streamlit run app/main.py
   ```
2. Select your mode (Student or Placement Officer) to begin using the application.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.