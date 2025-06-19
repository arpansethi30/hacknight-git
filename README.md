# 🚀 Smart Invest AI - Modern AI-Powered Financial Analysis Platform

<div align="center">

![Smart Invest AI Logo](https://img.shields.io/badge/Smart%20Invest%20AI-AI%20Powered-blue?style=for-the-badge&logo=react)

**A cutting-edge financial analysis platform combining real-time market data, AI sentiment analysis, and comprehensive fundamental insights**

## 🏆 Hackathon Achievement

**Winner at GitHub Hack Night - June 18, 2025 🎉**

<div align="center">

![Hackathon Winner](https://img.shields.io/badge/🏆%20Winner-GitHub%20Hack%20Night-gold?style=for-the-badge)
![Daft Prize](https://img.shields.io/badge/🥇%20Daft-$50%20Top%20Prize-success?style=flat-square)
![FriendliAI Prize](https://img.shields.io/badge/🥇%20FriendliAI-$50%20Best%20Use%20Prize-success?style=flat-square)

</div>

Smart Invest AI was recognized as a **winning project** at the prestigious **GitHub Hack Night** hosted at the GitHub San Francisco office. The project earned **two top prizes**:

- 🏅 **$50 Daft Top Prize** - For exceptional use of Daft's advanced data processing capabilities in financial analysis
- 🏅 **$50 FriendliAI Best Use Prize** - For innovative integration of FriendliAI's LLM for sentiment analysis

### 🎤 Event Highlights
The hackathon featured lightning talks and insights from leading AI companies:
- **Weaviate** - Vector database solutions
- **FriendliAI** - LLM model deployment and optimization
- **Arize AI** - ML observability and monitoring
- **Hypermode** - AI infrastructure platform
- **Daft by Eventual** - Next-generation data processing

*Thank you to all the sponsors and organizers for an incredible event that showcased the power of modern AI technologies!*

---

[![Next.js](https://img.shields.io/badge/Next.js-15.3.4-black?style=flat&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.0-38bdf8?style=flat&logo=tailwind-css)](https://tailwindcss.com/)

</div>

## ✨ Features

### 🎨 **Modern UI/UX Design**
- **Light-themed modern interface** with white/grey color scheme
- **Floating glassmorphism navbar** with smooth animations
- **Curved edges and rounded corners** throughout the design
- **Responsive design** optimized for all screen sizes
- **Smooth transitions** and hover effects
- **Background blur effects** and subtle gradients

### 🤖 **AI-Powered Analysis**
- **FriendliAI Integration**: Advanced sentiment analysis using meta-llama-3.1-8b-instruct
- **Real-time sentiment scoring** for market news and articles
- **Confidence indicators** and sentiment distribution analysis
- **Natural language processing** for financial content understanding

### 📊 **Comprehensive Data Processing**
- **Daft Integration**: Powerful data processing for fundamental analysis
- **Real-time stock data** via yfinance integration
- **Technical indicators**: RSI, MACD, moving averages, volatility metrics
- **Financial ratios**: P/E, P/B, ROE, market cap analysis
- **Risk assessment** and sector comparison tools

### 📰 **Live Market Intelligence**
- **Real-time news integration** via NewsAPI
- **Multi-source data aggregation** for comprehensive insights
- **Smart caching system** for optimal performance
- **Live price updates** and market data feeds

## 🏗️ **Architecture**

### **Frontend (Next.js 15 + TypeScript)**
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Modern floating navbar layout
│   │   ├── page.tsx            # Homepage with hero & features
│   │   └── globals.css         # Custom styling & animations
│   └── components/
│       └── StockAnalysis.tsx   # Comprehensive analysis component
├── package.json
└── tailwind.config.js
```

### **Backend (FastAPI + Python 3.12)**
```
backend/
├── api/
│   └── routes.py              # REST API endpoints
├── core/
│   └── config.py              # Environment configuration
├── data/
│   ├── stock_processor.py     # Real-time stock data
│   ├── news_processor.py      # News API integration
│   └── fundamental_processor.py # Daft-powered analysis
├── llm/
│   └── sentiment_analyzer.py  # FriendliAI integration
├── models/
│   └── schemas.py             # Pydantic data models
└── main.py                    # FastAPI application
```

## 🔧 **Technology Stack**

| Category | Technology | Purpose |
|----------|------------|---------|
| **Frontend** | Next.js 15.3.4 | React framework with App Router |
| **Styling** | Tailwind CSS 4 | Modern utility-first CSS |
| **Language** | TypeScript 5 | Type-safe development |
| **Backend** | FastAPI | High-performance Python API |
| **AI/ML** | FriendliAI | LLM-powered sentiment analysis |
| **Data Processing** | Daft | Advanced DataFrame operations |
| **Market Data** | yfinance | Real-time stock information |
| **News Data** | NewsAPI | Financial news aggregation |
| **Environment** | Python 3.12 | Modern Python runtime |

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.12+
- Node.js 18+
- npm or yarn

### **Backend Setup**
```bash
# Clone the repository
git clone <repository-url>
cd hacknight-git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env_template.txt .env
# Add your API keys (NewsAPI, FriendliAI)

# Start backend server
cd backend
python -m uvicorn main:app --reload --port 8001
```

### **Frontend Setup**
```bash
# Install frontend dependencies
cd frontend
npm install

# Start development server
npm run dev
```

### **Access the Application**
- **Frontend**: http://localhost:3000 (or port shown in terminal)
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

## 📋 **API Endpoints**

### **Core Endpoints**
- `GET /api/v1/health` - Health check
- `GET /api/v1/stock/{symbol}` - Real-time stock data
- `GET /api/v1/stocks/multiple` - Multiple stocks data
- `GET /api/v1/news/{symbol}` - Financial news

### **AI-Powered Analysis**
- `GET /api/v1/sentiment/{symbol}` - FriendliAI sentiment analysis
- `GET /api/v1/fundamentals/{symbol}` - Daft fundamental analysis
- `GET /api/v1/analysis/technical/{symbol}` - Technical indicators
- `GET /api/v1/analysis/complete/{symbol}` - Comprehensive analysis

### **Advanced Features**
- `GET /api/v1/comparison/sector/{symbol}` - Peer comparison
- `GET /api/v1/analysis/comprehensive/{symbol}` - Multi-source insights

## 🎯 **Key Features Showcase**

### **1. Hero Section**
- Gradient text effects with "AI-Powered Financial Analysis"
- Technology stack pills display
- Call-to-action buttons with hover animations

### **2. Live Market Dashboard**
- Real-time stock price cards with color-coded changes
- Volume indicators and percentage changes
- Loading states with skeleton animations

### **3. AI Sentiment Analysis**
- FriendliAI-powered news sentiment scoring
- Confidence indicators and sentiment distribution
- Color-coded sentiment badges (Bullish/Bearish/Neutral)

### **4. Fundamental Analysis**
- Daft-processed financial ratios and metrics
- Technical indicators with color-coded values
- Risk assessment and volatility analysis

### **5. Comprehensive Recommendations**
- AI-generated buy/sell/hold recommendations
- Confidence scoring with progress bars
- Key factors and reasoning explanations

## 🎨 **Design System**

### **Color Palette**
- **Primary**: Blue gradients (#3b82f6 to #8b5cf6)
- **Background**: Light grays (#fafafa, #f8fafc)
- **Cards**: Pure white (#ffffff) with subtle shadows
- **Text**: Dark grays (#0a0a0a, #64748b)
- **Accents**: Green/Red for positive/negative indicators

### **Typography**
- **Font**: Inter (Clean, modern sans-serif)
- **Sizes**: Responsive scale from 12px to 72px
- **Weights**: 400 (regular) to 700 (bold)

### **Components**
- **Cards**: Rounded-2xl with shadow-lg and hover effects
- **Buttons**: Gradient backgrounds with rounded-lg
- **Navbar**: Glassmorphism with backdrop-blur
- **Icons**: Heroicons for consistency

## 🏆 **Hackathon Sponsor Integration**

✅ **FriendliAI** ($50 prize target)
- Real sentiment analysis using meta-llama-3.1-8b-instruct
- Async client integration with proper error handling
- Live API calls with fallback mechanisms

✅ **Daft** ($50 prize target)
- DataFrame operations for fundamental analysis
- Technical indicator calculations
- Statistical data processing

✅ **Live Data Sources**
- yfinance for real-time stock data
- NewsAPI for financial news aggregation
- Comprehensive caching system

## 📱 **Responsive Design**

The application is fully responsive with:
- **Mobile-first approach** using Tailwind CSS
- **Flexible grid layouts** that adapt to screen size
- **Touch-friendly interactions** on mobile devices
- **Optimized performance** across all devices

## 🔮 **Future Enhancements**

- **Interactive charts** with real-time price movements
- **Portfolio tracking** and performance analytics
- **Advanced filtering** and search capabilities
- **Real-time notifications** for price alerts
- **Social features** for sharing insights
- **Machine learning predictions** for price forecasting

## 🤝 **Contributing**

We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">

**Built with ❤️ for the Hackathon**

*Showcasing the power of modern web technologies, AI integration, and beautiful design*

</div> 