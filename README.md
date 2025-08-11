# QMS Event Management System

A comprehensive Quality Management System (QMS) for tracking and managing quality events with AI assistance powered by Google Gemini.

## Features

- **Event Management**: Create, view, edit, and track quality events
- **AI Assistant**: Integrated AI assistance for event analysis, risk assessment, and recommendations
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- **Real-time Data**: FastAPI backend with SQLite database
- **Event Types**: Support for deviations, investigations, CAPAs, and more

## Tech Stack

### Frontend
- React 18 with Vite
- Redux Toolkit for state management
- React Router for navigation
- Tailwind CSS for styling

### Backend
- FastAPI (Python)
- SQLAlchemy ORM
- SQLite database
- Google Gemini AI integration
- Alembic for database migrations

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sawanb22/qms2.git
cd qms2
```

2. Set up the backend:
```bash
cd qms-backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the `qms-backend` directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Initialize the database:
```bash
python init_db.py
```

5. Set up the frontend:
```bash
cd ../qms-frontend
npm install
```

### Running the Application

1. Start the backend server:
```bash
cd qms-backend
uvicorn main:app --reload
```

2. Start the frontend development server:
```bash
cd qms-frontend
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

## Project Structure

```
qms2/
├── qms-backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── event.py
│   ├── alembic/
│   ├── main.py
│   ├── database.py
│   └── requirements.txt
├── qms-frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── features/
│   │   ├── app/
│   │   └── styles/
│   ├── public/
│   └── package.json
└── README.md
```

## API Endpoints

- `GET /api/events` - Get all events
- `POST /api/events` - Create a new event
- `GET /api/events/{id}` - Get event by ID
- `PUT /api/events/{id}` - Update event
- `POST /api/ai/assist` - AI assistance endpoint

## Design Choices and Assumptions

### Architecture Decisions
- **Monorepo Structure**: Frontend and backend are kept in separate directories within the same repository for easier development and deployment
- **SQLite Database**: Chosen for simplicity and ease of setup; can be easily migrated to PostgreSQL for production
- **React + FastAPI**: Modern, performant stack with strong typing support and excellent developer experience
- **Inline Styling**: Used inline styles with Tailwind-inspired design for component-level styling control

### Assumptions Made
- **Single User System**: No authentication/authorization implemented (can be added for multi-user scenarios)
- **Local Development**: Configured for local development with localhost URLs
- **Event Schema**: Comprehensive event model covering typical QMS requirements (deviations, CAPAs, investigations)
- **AI Integration**: Assumes Gemini API key is available for AI features

### Technical Choices
- **State Management**: Redux Toolkit for predictable state management
- **Date Handling**: Automatic parsing of date strings to Python date objects for database compatibility
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **CORS Configuration**: Enabled for local development across different ports

## AI Features and Interaction

### Integrated AI Assistant
The application includes a sophisticated AI assistant powered by Google Gemini 2.5 that provides:

#### Available AI Tools
1. **Event Analysis**: "Summarize this event" - Provides comprehensive event summaries
2. **Risk Assessment**: "Analyze risk level" - Evaluates event severity and potential impact
3. **Investigation Guidance**: "Suggest investigation steps" - Recommends systematic investigation approaches
4. **Historical Analysis**: "Find similar past events" - Identifies patterns and trends
5. **Action Recommendations**: "Recommend corrective actions" - Suggests appropriate CAPA measures
6. **Report Generation**: "Draft a report for this event" - Creates structured event reports
7. **Completeness Check**: "List missing information" - Identifies gaps in event documentation

#### How to Interact with AI
1. **Event Detail View**: 
   - Navigate to any event detail page
   - AI assistant panel appears on the right side
   - Use quick action buttons for common tasks
   - Type custom questions in the chat input

2. **Event List View**:
   - AI assistant analyzes all events in the system
   - Provides system-wide insights and trends
   - Helps with bulk analysis and reporting

#### AI Capabilities
- **Context-Aware**: AI has access to complete event data including dates, types, status, and descriptions
- **Real-time Analysis**: Instant responses to queries about events
- **Natural Language**: Accepts questions in plain English
- **Multi-Event Analysis**: Can analyze patterns across multiple events
- **Compliance Focus**: Trained specifically for QMS and life sciences compliance

#### Sample AI Interactions
```
User: "What are the high-risk events that need immediate attention?"
AI: "Based on the current events, I've identified 2 high-risk items..."

User: "Generate a summary report for event ID 5"
AI: "Event Summary Report - Title: [Event Title]..."

User: "What trends do you see in our CAPA effectiveness?"
AI: "Analyzing the CAPA events, I notice..."
```

## API Endpoints

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
