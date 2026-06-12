# Django AI Assistant

An AI-powered chatbot built with Django and Google Gemini API that provides Django-focused assistance through contextual conversations. The application supports chat history management, token-based usage tracking, subscription plans, and a responsive chat interface.

## Features

* AI-powered chatbot using Google Gemini API
* Context-aware conversations with chat history
* User authentication and protected chat access
* UUID-based conversation management
* Token usage tracking and limits
* Free, Standard, and Pro subscription plans
* Weekly token reset system
* Markdown response formatting
* HTML sanitization for secure rendering
* AJAX-powered real-time chat interface
* Error handling for API rate limits and service failures

## Tech Stack

* Python
* Django
* Google Gemini API
* JavaScript (AJAX)
* HTML
* CSS

## How It Works

1. Users log in to access the chatbot.
2. A new conversation is created automatically when a user sends the first message.
3. Previous messages are included as context for AI responses.
4. Google Gemini API generates responses based on conversation history.
5. Responses are formatted and sanitized before being displayed.
6. Token usage is tracked against the user's subscription plan.
7. Weekly token limits are automatically reset.

## Subscription System

### Free Plan

* Limited token usage
* Weekly token reset

### Standard Plan

* Increased token allowance
* Weekly token reset

### Pro Plan

* Highest token allowance
* Weekly token reset

## Security Features

* Login-protected chat access
* Ownership validation for conversations
* HTML sanitization using NH3
* Secure token usage tracking
* API exception handling
* Protected access to subscription data

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd django-ai-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Configure Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key
```

### Run Server

```bash
python manage.py runserver
```

## Future Improvements

* Stripe subscription integration
* Conversation search functionality
* Conversation deletion and archiving
