# FBReaperV1 - Streamlit Frontend

A comprehensive and modern Streamlit-based frontend for the FBReaperV1 Facebook OSINT Dashboard. This frontend provides an intuitive, interactive interface for monitoring, controlling, and analyzing Facebook data collection activities.

## 🚀 Features

### 📊 Dashboard
- **Real-time Statistics**: Live metrics for posts, comments, reactions, and scraper sessions
- **Advanced Analytics**: Sentiment analysis, engagement metrics, and trend visualization
- **Interactive Charts**: Time series data, sentiment distribution, and keyword analysis
- **Auto-refresh**: Configurable automatic data updates
- **Mock Data Support**: Demo mode for testing and demonstration

### 🤖 Scraper Control
- **Real-time Monitoring**: Live scraper status and progress tracking
- **Advanced Controls**: Start, stop, pause, and emergency stop functionality
- **Session Management**: Comprehensive session history and metrics
- **Error Logging**: Detailed error tracking and troubleshooting
- **Performance Metrics**: Success rates, response times, and throughput analysis

### 📝 Post Search & Browse
- **Advanced Filtering**: Search by keywords, authors, hashtags, and sentiment
- **Date Range Filtering**: Filter posts by time periods
- **Sorting Options**: Sort by date, engagement, sentiment, and more
- **Pagination**: Efficient browsing of large datasets
- **Export Functionality**: Download data in CSV and JSON formats
- **Data Visualization**: Sentiment distribution and timeline analysis

### 🕸️ Network Graph Visualization
- **Interactive Networks**: Dynamic network graphs with multiple layout algorithms
- **Advanced Analysis**: Community detection, centrality metrics, and path analysis
- **Customizable Visualization**: Node sizing, edge styling, and physics options
- **Multiple Network Types**: Post, user, hashtag, and full network analysis
- **Export Capabilities**: Save network visualizations and analysis results

### ⚙️ Settings & Configuration
- **System Status**: Real-time monitoring of backend, database, and scraper services
- **Application Settings**: Theme, language, timezone, and performance configurations
- **Data Management**: Retention policies, backup settings, and export preferences
- **Maintenance Tools**: Cache clearing, statistics reset, and system restart

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Java 17+ (for backend)
- Node.js 18+ (for React frontend - optional)
- Docker (for infrastructure services)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd facebook-osint-dashboard
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend services** (if not already running):
   ```bash
   # Start infrastructure services
   docker-compose up -d
   
   # Start Java backend
   cd backend-java
   mvn spring-boot:run
   ```

4. **Launch the Streamlit frontend**:
   ```bash
   streamlit run app.py
   ```

5. **Access the application**:
   - Streamlit Frontend: http://localhost:8501
   - Java Backend: http://localhost:8080
   - Neo4j Database: http://localhost:7474
   - Kafka UI: http://localhost:8081

## 📋 Configuration

### Backend Connection
The frontend automatically connects to the Java backend at `http://localhost:8080`. You can change this in the sidebar configuration:

1. Navigate to the sidebar
2. Find the "Configuration" section
3. Update the "Backend URL" field
4. Click outside the field to save

### Environment Variables
Create a `.env` file in the root directory for custom configurations:

```env
BACKEND_URL=http://localhost:8080
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
```

## 🎯 Usage Guide

### Dashboard Overview
1. **View Statistics**: The dashboard shows key metrics including total posts, comments, users, and scraper sessions
2. **Monitor Trends**: Charts display data over time, sentiment distribution, and engagement metrics
3. **Auto-refresh**: Enable automatic updates to keep data current
4. **Export Data**: Download statistics and charts for reporting

### Scraper Management
1. **Start Scraping**: Enter keywords and configure parameters in the scraper control panel
2. **Monitor Progress**: Track real-time progress, success rates, and error logs
3. **Control Sessions**: Stop, pause, or restart scraping sessions as needed
4. **View History**: Access detailed session logs and performance metrics

### Data Exploration
1. **Search Posts**: Use advanced filters to find specific content
2. **Browse Data**: Navigate through posts with pagination and sorting
3. **Analyze Sentiment**: View sentiment analysis results and trends
4. **Export Results**: Download filtered data in various formats

### Network Analysis
1. **Select Posts**: Choose posts for network analysis
2. **Configure Visualization**: Adjust layout, node sizing, and display options
3. **Explore Networks**: Interact with network graphs to discover relationships
4. **Analyze Communities**: Identify and explore community structures

## 🔧 Advanced Features

### Custom Styling
The application uses custom CSS for enhanced visual appeal:
- Gradient backgrounds and modern card designs
- Hover effects and smooth transitions
- Responsive layout for different screen sizes
- Dark mode support (planned feature)

### Data Visualization
- **Plotly Charts**: Interactive charts with zoom, pan, and hover features
- **PyVis Networks**: Dynamic network graphs with physics simulation
- **Custom Metrics**: Real-time metrics with delta indicators
- **Export Options**: Save charts as images or interactive HTML

### Error Handling
- **Graceful Degradation**: Application continues to work even with backend issues
- **Mock Data**: Demo mode provides sample data for testing
- **Error Logging**: Detailed error messages and troubleshooting information
- **Connection Monitoring**: Real-time status of all system components

### Performance Optimization
- **Caching**: Intelligent caching of frequently accessed data
- **Lazy Loading**: Load data on demand to improve performance
- **Pagination**: Efficient handling of large datasets
- **Background Processing**: Non-blocking operations for better UX

## 🐛 Troubleshooting

### Common Issues

1. **Backend Connection Failed**
   - Ensure the Java backend is running on the correct port
   - Check firewall settings and network connectivity
   - Verify the backend URL in the configuration

2. **No Data Displayed**
   - Check if the scraper has collected any data
   - Verify database connectivity
   - Enable mock data mode for testing

3. **Network Graph Not Loading**
   - Ensure all required Python packages are installed
   - Check browser console for JavaScript errors
   - Try the fallback visualization option

4. **Performance Issues**
   - Reduce the number of posts per page
   - Disable auto-refresh for large datasets
   - Clear browser cache and restart the application

### Debug Mode
Enable debug mode by setting the environment variable:
```bash
export STREAMLIT_DEBUG=true
streamlit run app.py
```

### Logs
Check the Streamlit logs for detailed error information:
```bash
streamlit run app.py --logger.level=debug
```

## 🔒 Security Considerations

- **API Security**: All API calls use HTTPS when available
- **Data Privacy**: No sensitive data is stored in the frontend
- **Access Control**: Implement authentication for production use
- **Rate Limiting**: Respect API rate limits to avoid service disruption

## 🚀 Deployment

### Production Deployment
1. **Set up a production server** with Python 3.8+
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure environment variables** for production settings
4. **Set up a reverse proxy** (nginx recommended)
5. **Enable SSL/TLS** for secure connections
6. **Configure monitoring** and logging

### Docker Deployment
```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Cloud Deployment
- **Heroku**: Use the provided `Procfile` and `runtime.txt`
- **AWS**: Deploy using Elastic Beanstalk or ECS
- **Google Cloud**: Use App Engine or Compute Engine
- **Azure**: Deploy using App Service or Container Instances

## 📈 Performance Monitoring

### Metrics to Monitor
- **Response Times**: API call latency and page load times
- **Memory Usage**: Application memory consumption
- **CPU Usage**: Processing overhead and resource utilization
- **Error Rates**: Failed requests and application errors
- **User Activity**: Page views, session duration, and feature usage

### Monitoring Tools
- **Streamlit Built-in**: Use Streamlit's built-in monitoring
- **Prometheus**: Custom metrics collection
- **Grafana**: Visualization and alerting
- **Sentry**: Error tracking and performance monitoring

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -am 'Add new feature'`
5. **Push to the branch**: `git push origin feature/new-feature`
6. **Submit a pull request**

### Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd facebook-osint-dashboard

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run the application in development mode
streamlit run app.py --server.runOnSave=true
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit Team**: For the amazing framework
- **Plotly**: For interactive visualizations
- **PyVis**: For network graph capabilities
- **NetworkX**: For network analysis algorithms
- **Pandas**: For data manipulation and analysis

## 📞 Support

For support and questions:
- **Issues**: Create an issue on GitHub
- **Documentation**: Check the project wiki
- **Community**: Join our Discord server
- **Email**: Contact the development team

---

**Note**: This frontend is designed to work with the FBReaperV1 backend system. Ensure all backend services are properly configured and running before using the frontend.