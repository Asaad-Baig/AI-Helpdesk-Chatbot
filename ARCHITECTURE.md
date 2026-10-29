# Enterprise AI Helpdesk & Chatbot Architecture Specification

## Overview
This system is a multi-tier, AI-powered helpdesk assistant designed for enterprise query resolution. It features a React-based frontend, a Flask REST API backend, a MongoDB database, and a local LLM runtime powered by Ollama.

## System Architecture Diagram
[React Frontend] <---> [Flask REST API] <---> [MongoDB Database]
                              |
                              +---> [Ollama LLM Runtime (Llama 3.2)]

## Technology Stack
- **Frontend UI:** React.js, Tailwind CSS, Lucide React, Axios
- **Backend API:** Python Flask, Flask-CORS, PyMongo
- **Database:** MongoDB (Collections: users, conversations, messages, raw_data, enriched_data, feedback)
- **AI/LLM Runtime:** Ollama (Llama 3.2)