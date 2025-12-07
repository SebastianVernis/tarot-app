# 🔮 Tarot App - Mystical Card Reading Platform

A modern, full-stack web application for Tarot card readings with AI-powered interpretations, user authentication, and subscription management.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/tarot-app)

## ✨ Features

- **🎴 Tarot Readings**: Multiple spread types (Single Card, 3-Card, Celtic Cross, etc.)
- **🤖 AI Interpretations**: Powered by Google Gemini AI for personalized readings
- **👤 User Authentication**: Secure JWT-based authentication system
- **💳 Subscription Management**: Free and Premium tiers with reading limits
- **📊 Reading History**: Track and review past readings
- **🎨 Theme Support**: Light/Dark mode with persistent preferences
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 22+ (for Vercel CLI)
- PostgreSQL (optional, SQLite used by default)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd tarot-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

### Deploy to Vercel

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Validate build**
   ```bash
   ./scripts/build.sh
   ```

4. **Deploy**
   ```bash
   vercel --prod
   ```

5. **Set environment variables**
   ```bash
   vercel env add SECRET_KEY
   vercel env add JWT_SECRET_KEY
   vercel env add GEMINI_API_KEY
   vercel env add DATABASE_URL  # Optional
   ```

## 📁 Project Structure

```
tarot-app/
├── api/                    # Vercel serverless functions
│   └── index.py           # WSGI entry point
├── routes/                # Flask route blueprints
│   ├── auth.py           # Authentication routes
│   ├── tarot.py          # Tarot reading routes
│   └── subscription.py   # Subscription routes
├── docs/                  # Documentation
│   ├── VERCEL_QUICK_START.md
│   ├── DEPLOYMENT_READY_VERCEL.md
│   └── ...
├── scripts/               # Build and deployment scripts
│   ├── build.sh          # Validation script
│   ├── deploy.sh         # Deployment script
│   └── deploy-vercel.sh  # Vercel-specific deployment
├── assets/                # Images and static assets
├── app.py                # Main Flask application
├── config.py             # Configuration management
├── auth.py               # Authentication logic
├── tarot_web.html        # Frontend HTML
├── tarot_web.js          # Frontend JavaScript
├── requirements.txt      # Python dependencies
├── vercel.json           # Vercel configuration
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key for sessions | ✅ Yes |
| `JWT_SECRET_KEY` | JWT token signing key | ✅ Yes |
| `GEMINI_API_KEY` | Google Gemini API key for AI interpretations | ✅ Yes |
| `DATABASE_URL` | PostgreSQL connection string | ❌ No (SQLite default) |
| `FLASK_ENV` | Environment (development/production) | ❌ No |

### Database

- **Development**: SQLite (automatic, no setup required)
- **Production**: PostgreSQL recommended (set `DATABASE_URL`)
- **Vercel**: In-memory SQLite (stateless, for testing only)

## 📚 Documentation

- **[Quick Start Guide](docs/VERCEL_QUICK_START.md)** - Get started in 3 steps
- **[Deployment Guide](docs/DEPLOYMENT_READY_VERCEL.md)** - Complete deployment instructions
- **[Build Guide](docs/VERCEL_BUILD_GUIDE.md)** - Comprehensive build documentation
- **[API Documentation](docs/COMO_USAR.txt)** - API endpoints and usage

## 🧪 Testing

### Run Build Validation
```bash
./scripts/build.sh
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/api/health

# Get tarot cards
curl http://localhost:5000/api/tarot/cards
```

### Test Frontend
Open `http://localhost:5000` in your browser and test:
- User registration/login
- Card readings (all spread types)
- Theme switching
- Reading history

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Flask-JWT-Extended** - Authentication
- **Google Gemini AI** - AI interpretations

### Frontend
- **Vanilla JavaScript** - No framework dependencies
- **HTML5/CSS3** - Modern, responsive design
- **Fetch API** - RESTful API communication

### Deployment
- **Vercel** - Serverless deployment platform
- **PostgreSQL** - Production database (optional)

## 📊 Features Status

| Feature | Status | Notes |
|---------|--------|-------|
| Tarot Readings | ✅ Complete | All spread types working |
| User Authentication | ✅ Complete | JWT-based auth |
| Subscription System | ✅ Complete | Free/Premium tiers |
| Reading History | ✅ Complete | Full CRUD operations |
| AI Interpretations | ✅ Complete | Gemini AI integration |
| Theme Support | ✅ Complete | Light/Dark modes |
| Astrology Features | ❌ Disabled | Heavy dependencies (250MB+) |

## 🚨 Known Limitations

- **Astrology features disabled** on Vercel due to heavy dependencies (pyswisseph, numpy, matplotlib)
- **In-memory database** on Vercel (stateless) - use PostgreSQL for production
- **Cold start latency** on serverless functions (~2-3 seconds)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/tarot-app/issues)
- **Documentation**: See `docs/` directory
- **Build Problems**: Run `./scripts/build.sh` for diagnostics

## 🎉 Acknowledgments

- Tarot card interpretations powered by Google Gemini AI
- Card images and symbolism from traditional Rider-Waite deck
- Built with ❤️ for the mystical community

---

**Ready to deploy?** Run `./scripts/build.sh` then `vercel --prod` 🚀
