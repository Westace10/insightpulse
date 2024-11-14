# Streamlit Sensor Data Analysis and Chat App

An interactive application built with Streamlit to analyze and generate insights from real-time sensor data. This app leverages data retrieval, natural language processing, and data visualization to provide users with actionable insights through an intuitive, chat-based interface.

## Key Features

### 1. Insight Generation
The **Insight Generation** feature helps users visualize real-time and historical sensor data for various environmental factors, such as temperature, humidity, air quality, and CO2 levels. Interactive charts and insights allow users to:
- Track environmental changes.
- Detect patterns or anomalies in data.
- Gain a better understanding of environmental conditions.

### 2. RAG (Retrieval-Augmented Generation) Chat
With **Retrieval-Augmented Generation (RAG)**, users can interact with sensor data conversationally. This feature allows users to ask questions and receive meaningful, context-aware responses about sensor data. For example, users can query:
- "What was the highest temperature recorded this week?"
- "How has the air quality varied over the last month?"

The RAG-based chat leverages **LangChain** and **AWS Bedrock** for natural language processing, ensuring accurate and relevant answers based on sensor data.

## Importance of This App

Real-time environmental data is crucial for monitoring and improving health, safety, and environmental conditions. This app:
- **Supports Data-Driven Decisions**: Enables better decision-making based on real-time and historical data.
- **Enhances Environmental Awareness**: Provides insights that encourage proactive environmental management.
- **Supports Research and Education**: Ideal for students, researchers, and environmental scientists working with real-world data.

## Technologies and Tools Used

This app integrates the following tools and technologies:

### MongoDB Atlas
**MongoDB Atlas** is used to store sensor data in the cloud. MongoDB's flexible schema allows for easy storage and retrieval of sensor data, while its cloud-native capabilities support scalability and management.

### MongoDB Vector
**MongoDB Vector Search** is used to store vector embeddings of text and sensor data, enabling efficient similarity-based queries. This allows the RAG system to retrieve the most relevant data when answering user questions.

### AWS Bedrock
**AWS Bedrock** provides foundational language models for natural language generation, enabling the RAG model to create accurate and contextually relevant responses based on sensor data.

### LangChain
**LangChain** is a framework for integrating large language models (LLMs) with external data. It supports the RAG chat system by managing the retrieval and language generation process, connecting MongoDB data with AWS Bedrock to answer user queries.

### Streamlit
**Streamlit** is used for the app’s user interface, offering an easy-to-use, interactive experience. With Streamlit, users can visualize insights, interact with the RAG chat, and view real-time sensor data seamlessly.

## Folder Structure

The project is organized as follows:

```plaintext
.
├── api                     # Backend API folder
│   ├── routes              # API routes
│   ├── services            # Services for data processing
│   ├── config.py           # Configuration for the API
│   ├── main.py             # Main API entry point
│   └── sensor_data.txt     # Sample sensor data file
├── components              # Streamlit component modules
│   ├── insight_display.py  # Displays insights in the app
│   ├── sensor_charts.py    # Visualizations for sensor data
│   └── sensor_form.py      # Form to input sensor data
├── .gitignore              # Files and directories to ignore in git
├── README.md               # Project documentation
├── app.py                  # Main Streamlit application file
├── requirements.txt        # Project dependencies
└── utils.py                # Utility functions for the app
```

### Folder Descriptions

- **`/api`**: Contains backend API components for data processing, including routes, services, and configurations.
  - **`routes`**: API endpoint definitions.
  - **`services`**: Business logic and data processing services.
  - **`config.py`**: Configuration for the API, including environment settings.
  - **`main.py`**: Entry point for running the API.
  - **`sensor_data.txt`**: Example sensor data for testing.
- **`/components`**: Modules for different UI components in Streamlit.
  - **`insight_display.py`**: Displays calculated insights based on sensor data.
  - **`sensor_charts.py`**: Generates charts for data visualization.
  - **`sensor_form.py`**: Handles user input for sensor data.
- **`app.py`**: Main Streamlit app that integrates all components.
- **`utils.py`**: Helper functions to support the app’s functionality.

## Getting Started

### Prerequisites
- Python 3.8 or above
- MongoDB Atlas account
- AWS account with Bedrock access

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/streamlit_sensor_app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd streamlit_sensor_app
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **MongoDB Atlas**: Set up your MongoDB Atlas account and database.
2. **AWS Bedrock**: Configure AWS credentials for Bedrock access. Ensure permissions are correctly set.
3. **Environment Variables**: Add environment variables in a `.env` file:
   ```plaintext
   MONGODB_URI=<Your MongoDB Atlas URI>
   AWS_ACCESS_KEY_ID=<Your AWS Access Key ID>
   AWS_SECRET_ACCESS_KEY=<Your AWS Secret Access Key>
   ```

### Running the App

Start the Streamlit app locally:
```bash
streamlit run app.py
```

Access the app at `http://localhost:8501`.

## Usage

1. **Insight Generation**: View real-time and historical data visualizations under the Insight section.
2. **RAG Chat**: Use the chat interface to ask questions about the sensor data and get context-aware responses.

## Future Enhancements

- **Extended Data Types**: Add support for additional environmental sensors, such as light intensity and noise levels.
- **Customizable Reports**: Enable users to export data insights as reports.
- **Enhanced NLP**: Improve the RAG chat to handle more complex queries.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! Feel free to submit pull requests or open issues for discussion.

## Acknowledgments

This app is built with open-source technologies and cloud services, including MongoDB Atlas, AWS Bedrock, LangChain, and Streamlit.