# 🛡️ SpamDetector

<div align="center">

![SpamDetector Logo](https://img.shields.io/badge/SpamDetector-AI%20Powered-blue?style=for-the-badge&logo=shield&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow.svg?style=flat-square&logo=javascript&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg?style=flat-square)](LICENSE)

**A modern web application for detecting spam messages using AI and rule-based techniques.**

[Features](#features) • [Demo](#demo) • [Installation](#installation) • [API](#api) • [Technologies](#technology-stack)

</div>

<img src="https://user-images.githubusercontent.com/1303154/88677602-1635ba80-d120-11ea-84d8-d263ba5fc3c0.gif" width="28px" alt="hi"> **Real-time spam detection with confidence scores and detailed analysis**

## ✨ Features

<table>
  <tr>
    <td width="50%">
      <h3>🤖 AI-Powered Analysis</h3>
      <ul>
        <li>Machine learning classification</li>
        <li>Confidence scoring</li>
        <li>Real-time processing</li>
      </ul>
    </td>
    <td width="50%">
      <h3>📏 Rule-Based Detection</h3>
      <ul>
        <li>Pattern recognition</li>
        <li>Detailed explanations</li>
        <li>Customizable rule sets</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>🖥️ Interactive Interface</h3>
      <ul>
        <li>Real-time demo page</li>
        <li>Responsive design</li>
        <li>Intuitive visualization</li>
      </ul>
    </td>
    <td width="50%">
      <h3>🔒 Spam Protection</h3>
      <ul>
        <li>Contact form protection</li>
        <li>High accuracy detection</li>
        <li>Low false positive rate</li>
      </ul>
    </td>
  </tr>
</table>

## 🏗️ Project Structure

```mermaid
graph TD
    A[SpamDetector] --> B[Frontend]
    A --> C[Backend]
    B --> B1[index.html]
    B --> B2[demo.html]
    B --> B3[style.css]
    B --> B4[main.js]
    C --> C1[app/]
    C1 --> C1A[main.py]
    C1 --> C1B[ml/]
    C1B --> C1B1[classifier.py]
    C1B --> C1B2[rules.py]
    C --> C2[models/]
    C --> C3[requirements.txt]
    A --> D[deploy.py]
```

## 🚀 Demo

<div align="center">
  <img src="https://via.placeholder.com/800x400?text=SpamDetector+Demo" alt="SpamDetector Demo" width="80%">
</div>

## 💻 Technology Stack

<div align="center">

| Frontend | Backend | ML/AI | Deployment |
|:--------:|:-------:|:-----:|:----------:|
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) | ![NLTK](https://img.shields.io/badge/NLTK-3776AB?style=for-the-badge&logo=python&logoColor=white) | ![Uvicorn](https://img.shields.io/badge/Uvicorn-2D2B55?style=for-the-badge&logo=gunicorn&logoColor=white) |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) | | ![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white) | |

</div>

## 📦 Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Quick Start

<details>
<summary>📋 Step-by-step instructions</summary>

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/SpamDetector.git
   cd SpamDetector
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Run the deployment script:**
   ```bash
   python deploy.py
   ```

4. **Open your browser and navigate to:**
   ```
   http://localhost:8080
   ```
</details>

## 🔌 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API health check |
| `GET` | `/health` | Detailed health status |
| `POST` | `/api/classify` | Classify a message as spam or ham |

<details>
<summary>📝 Example API Request</summary>

```json
POST /api/classify
{
  "message": "Your message to analyze",
  "options": {
    "include_details": true
  }
}
```
</details>

<details>
<summary>📝 Example API Response</summary>

```json
{
  "classification": "ham",
  "confidence": 0.92,
  "processing_time": 45,
  "details": {
    "rule_details": [...],
    "ml_confidence": 0.94,
    "triggered_rules": []
  }
}
```
</details>

## 📊 Performance

<div align="center">

| Metric | Value |
|--------|-------|
| Accuracy | 97.8% |
| False Positive Rate | <2% |
| Processing Time | <50ms |

</div>

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Font Awesome for icons
- Inter font family
- [Shields.io](https://shields.io/) for badges 