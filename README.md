# FBReaperV1 Streamlit Analytics Dashboard

A comprehensive Streamlit-based full-stack application that integrates with a Java Spring Boot backend for social media data scraping, analysis, and visualization.

## 🚀 Features

- **📊 Dashboard Statistics**: Real-time metrics and charts showing data collection statistics
- **🤖 Scraper Control**: Start/stop scraping sessions and monitor status
- **📝 Post Search**: Browse and search through collected posts with pagination
- **🕸️ Network Graph**: Interactive network visualization using link analysis
- **🔄 Real-time Updates**: Auto-refresh capabilities and live status monitoring
- **🎨 Modern UI**: Clean, responsive interface with Streamlit theming

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/REST    ┌──────────────────┐
│   Streamlit     │◄──────────────►│  Java Spring     │
│   Frontend      │                 │  Boot Backend    │
│                 │                 │                  │
│ - Dashboard     │                 │ - API Endpoints  │
│ - Scraper Ctrl  │                 │ - Data Services  │
│ - Post Search   │                 │ - Neo4j Database │
│ - Network Graph │                 │ - Kafka Queue    │
└─────────────────┘                 └──────────────────┘
```

## 📋 Prerequisites

- Python 3.8+
- Java 11+ (for Spring Boot backend)
- Neo4j Database
- Kafka (optional, for real-time messaging)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fbreaperv1-streamlit
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Java Spring Boot Backend

Ensure your Java Spring Boot backend is running on `http://localhost:8080`:

```bash
# Navigate to your backend directory
cd backend-java

# Build and run the Spring Boot application
./mvnw spring-boot:run
```

### 4. Run the Streamlit Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📖 Usage

### Dashboard Page
- View real-time statistics about collected data
- Monitor post and comment counts
- Analyze trends over time
- View top keywords and recent activity

### Scraper Control Page
- Start new scraping sessions with keywords
- Monitor scraper status and progress
- View session history
- Configure scraping parameters

### Post Search Page
- Browse all collected posts
- Search by keywords, author, or hashtags
- Sort posts by various criteria
- View comments for specific posts
- Paginate through large datasets

### Network Graph Page
- Select posts for network analysis
- Visualize relationships between users, posts, and hashtags
- Analyze network metrics (density, clustering, etc.)
- Detect communities and shortest paths

## 🔧 Configuration

### Backend URL
You can configure the backend URL in the sidebar:
- Default: `http://localhost:8080`
- Change this if your backend runs on a different port or host

### Auto-refresh
Enable auto-refresh in the sidebar to automatically update data every 30 seconds.

## 📊 API Endpoints

The application integrates with these backend endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/scraper/scrapeByKeyword` | POST | Start scraper with keyword |
| `/api/scraper/start` | POST | Start general scraper |
| `/api/data/posts` | GET | Get all posts |
| `/api/data/comments` | GET | Get all comments |
| `/api/data/stats` | GET | Get statistics |
| `/api/posts/{id}` | GET | Get specific post |
| `/api/comments/{id}` | GET | Get specific comment |
| `/api/link-analysis/{postId}` | GET | Get link analysis |

## 🗂️ Project Structure

```
fbreaperv1-streamlit/
├── app.py                 # Main Streamlit application
├── api_client.py          # API client for backend communication
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── pages/                # Streamlit page modules
    ├── __init__.py
    ├── dashboard.py      # Dashboard statistics page
    ├── scraper_control.py # Scraper control page
    ├── post_search.py    # Post search and browse page
    └── network_graph.py  # Network visualization page
```

## 🔍 Troubleshooting

### Backend Connection Issues
- Ensure your Java Spring Boot backend is running on `http://localhost:8080`
- Check that the backend is accessible via browser or curl
- Verify firewall settings and port availability

### Missing Dependencies
- Run `pip install -r requirements.txt` to install all dependencies
- Ensure you have Python 3.8+ installed

### Network Graph Issues
- The network graph requires posts to be available in the database
- Link analysis may take time for large datasets
- Ensure the backend link analysis service is working

### Data Not Loading
- Check backend logs for errors
- Verify database connectivity
- Ensure scraping sessions have collected data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the troubleshooting section above
- Review backend logs for errors
- Ensure all services are running correctly
- Verify network connectivity between frontend and backend