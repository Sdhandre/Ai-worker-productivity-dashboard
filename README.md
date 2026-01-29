#AI-Powered Worker Productivity Dashboard

## Overview

This project is a production-style full-stack web application that simulates how a manufacturing factory can use AI-powered CCTV systems to monitor worker activity and compute productivity metrics.

The system ingests structured AI-generated events, stores them in a database, computes time-based and production-based metrics, and displays them in a clear dashboard for factory monitoring.

No computer vision or machine learning models are built in this project. The focus is on event ingestion, metric computation, system design, and scalability.

Live Demo & Repository

Live Web Application:
https://ai-worker-productivity-dashboard.vercel.app

Backend API (Swagger):
https://ai-worker-productivity-dashboard-g2ji.onrender.com/docs

GitHub Repository:
https://github.com/Sdhandre/Ai-worker-productivity-dashboard


Edge → Backend → Dashboard Architecture

High-Level Flow
AI CCTV Cameras (Edge)
        ↓
Structured Events (JSON)
        ↓
FastAPI Backend
        ↓
SQLite Database
        ↓
Metrics Computation Layer
        ↓
React Dashboard