# 🔮 Tarot Místico

**Professional Tarot Reading Platform with AI-Powered Interpretations**

A modern, scalable web application for tarot card readings, astrology calculations, and mystical insights powered by Google's Gemini AI.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/tarot-mistico)

---

## ✨ Features

### 🎴 Tarot Readings
- **Multiple Spread Types**: Single card, 3-card, Celtic Cross, and more
- **AI Interpretations**: Powered by Google Gemini for deep, personalized insights
- **Reading History**: Save and review past readings
- **Beautiful UI**: Modern, responsive design with theme support

### 🌟 Astrology (Optional)
- **Birth Chart Calculations**: Precise planetary positions
- **House Systems**: Multiple house calculation methods
- **Astrological Aspects**: Detailed planetary relationships
- **AI Analysis**: Gemini-powered chart interpretations

### 👤 User Management
- **JWT Authentication**: Secure user sessions
- **Freemium Model**: Free tier with premium upgrades
- **Subscription Management**: Flexible pricing tiers
- **Theme Persistence**: Dark/light mode preferences

---

## 🚀 Quick Deploy to Vercel

### Prerequisites
- [Vercel Account](https://vercel.com/signup) (free)
- [Google Gemini API Key](https://makersuite.google.com/app/apikey) (free tier available)

### One-Click Deploy

1. **Click the Deploy button** above or run:
   ```bash
   vercel --prod
   ```

2. **Set Environment Variables** in Vercel Dashboard:
   ```bash
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-here
   GEMINI_API_KEY=your-gemini-api-key-here
   DATABASE_URL=postgresql://... # Optional, uses SQLite if not set
   ```

3. **Done!** Your app is live at `https://your-app.vercel.app`

---

## 🛠️ Local Development

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/tarot-mistico.git
cd tarot-mistico

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Run development server
python app.py
```

Visit `http://localhost:5000`

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
GEMINI_API_KEY=your-gemini-api-key-here

# Optional
DATABASE_URL=sqlite:///tarot.db  # Or PostgreSQL URL
FLASK_ENV=development
PORT=5000
```

---

## 📁 Project Structure

```
tarot-mistico/
├── api/
│   └── index.py          # Vercel serverless entry point
├── routes/
│   ├── auth_routes.py    # Authentication endpoints
│   ├── user_routes.py    # User management
│   ├── reading_routes.py # Tarot reading logic
│   ├── subscription_routes.py
│   └── astrology_routes.py
├── src/
│   ├── models.py         # Database models
│   ├── auth.py           # JWT authentication
│   ├── tarot_reader.py   # Tarot card logic
│   ├── gemini_service.py # AI integration
│   └── astrology_calculator.py
├── public/
│   ├── tarot_web.html    # Frontend UI
│   └── tarot_web.js      # Frontend logic
├── app.py                # Local development server
├── config.py             # Configuration
├── requirements.txt      # Python dependencies
├── vercel.json           # Vercel configuration
└── README.md             # This file
```

---

## 🔧 Configuration

### Vercel Settings

The `vercel.json` file is pre-configured for optimal performance:

- **Runtime**: Python 3.11
- **Memory**: 1024 MB
- **Timeout**: 30 seconds
- **Region**: US East (iad1)
- **Max Lambda Size**: 50 MB

### Database Options

1. **SQLite** (Default): Automatic, no setup required
2. **PostgreSQL**: Set `DATABASE_URL` environment variable
3. **In-Memory**: For testing only

---

## 📊 API Endpoints

### Health & Info
- `GET /api/health` - Health check
- `GET /api/info` - API information

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout

### Readings
- `POST /api/readings/draw` - Draw tarot cards
- `GET /api/readings/history` - Get reading history
- `GET /api/readings/:id` - Get specific reading

### User
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update profile
- `PUT /api/user/theme` - Update theme preference

### Subscription
- `GET /api/subscription/status` - Get subscription status
- `POST /api/subscription/upgrade` - Upgrade subscription

### Astrology (Optional)
- `POST /api/astrology/birth-chart` - Calculate birth chart
- `POST /api/astrology/interpret` - Get AI interpretation

---

## 🧪 Testing

### Health Check
```bash
curl https://your-app.vercel.app/api/health
```

### Test Reading
```bash
curl -X POST https://your-app.vercel.app/api/readings/draw \
  -H "Content-Type: application/json" \
  -d '{"spread_type": "single", "question": "What does today hold?"}'
```

---

## 🔐 Security

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: Bcrypt with salt
- **CORS Protection**: Configured origins only
- **Environment Variables**: Secrets never committed
- **SQL Injection Protection**: SQLAlchemy ORM
- **Rate Limiting**: Built-in protection

---

## 📈 Scaling

### Vercel Serverless
- **Auto-scaling**: Handles traffic spikes automatically
- **Global CDN**: Fast static asset delivery
- **Edge Network**: Low latency worldwide
- **Zero Config**: No server management

### Database Scaling
- **PostgreSQL**: Recommended for production
- **Connection Pooling**: Optimized for serverless
- **Read Replicas**: For high-traffic apps

---

## 🐛 Troubleshooting

### Build Fails
- Check Python version (3.11 required)
- Verify all dependencies in `requirements.txt`
- Check Vercel build logs

### API Errors
- Verify environment variables are set
- Check Gemini API key is valid
- Review Vercel function logs

### Database Issues
- Ensure `DATABASE_URL` is correct
- Check database connection limits
- Verify migrations are applied

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/tarot-mistico/issues)
- **Email**: support@tarotmistico.com
- **Documentation**: [Full Docs](https://docs.tarotmistico.com)

---

## 🌟 Acknowledgments

- **Google Gemini**: AI-powered interpretations
- **Vercel**: Serverless hosting platform
- **Flask**: Python web framework
- **Tarot Community**: Card meanings and spreads

---

**Made with ❤️ and ✨ by the Tarot Místico Team**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/tarot-mistico)
