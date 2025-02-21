# Streamlit Dashboard

This project is a Streamlit dashboard that utilizes an SQLite database as its backend. The dashboard provides an interactive interface for visualizing and analyzing data stored in the SQLite database.

## Project Structure

```
streamlit-dashboard
├── src
│   ├── app.py          # Main entry point for the Streamlit app
│   ├── database.py     # Database connection and query functions
│   └── utils.py        # Utility functions for data processing
├── data
│   └── database.db     # SQLite database file
├── requirements.txt     # Required Python packages
└── README.md           # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd streamlit-dashboard
   ```

2. **Create a virtual environment (optional but recommended):**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the Streamlit dashboard, execute the following command in your terminal:

```
streamlit run src/app.py
```

This will start the Streamlit server, and you can access the dashboard in your web browser at `http://localhost:8501`.

## Features

- Interactive data visualization
- Data retrieval and manipulation using SQLite
- User-friendly interface for data analysis

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.