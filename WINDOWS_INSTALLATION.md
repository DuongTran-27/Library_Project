# Windows Installation Guide - Online Library Management System

## Prerequisites
- Python 3.8+ installed (download from python.org)
- VS Code or any code editor
- Command line access (PowerShell or CMD)

## Step-by-Step Installation

### Step 1: Verify Python Installation
Open PowerShell and check Python version:
```powershell
python --version  # Should be 3.8 or higher
```

### Step 2: Create Virtual Environment
Navigate to your project folder and create venv:
```powershell
cd d:\library_project
python -m venv venv
```

### Step 3: Activate Virtual Environment
```powershell
venv\Scripts\Activate.ps1
```

Note: If you get an execution policy error, run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Core Dependencies
```powershell
pip install --upgrade pip
pip install Flask Flask-Login Flask-Mail python-dotenv Jinja2
```

### Step 5: Install Optional Dependencies (if needed)
```powershell
# For API support
pip install Flask-RESTful Flask-Cors

# For database ORM (may require compilation on Windows)
pip install Flask-SQLAlchemy SQLAlchemy

# For database migrations
pip install Flask-Migrate Alembic

# For PDF generation
pip install reportlab PyPDF2

# If you have Visual C++ Build Tools installed
pip install greenlet
```

### Step 6: Create .env File
Create a file named `.env` in your project root:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///library.db

# Email Configuration (Optional - for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password_not_regular_password

# Admin Settings
ADMIN_EMAIL=admin@yourlibrary.com
```

### Step 7: Initialize Database
```powershell
python run.py init_db
```

### Step 8: Create Admin Account
```powershell
python run.py create_admin
# Follow prompts to create admin account
```

### Step 9: Create Sample Data (Optional)
```powershell
python run.py create_sample_data
# This adds 3 sample books and 5 categories
```

### Step 10: Run the Application
```powershell
python run.py
```

Output should look like:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 11: Open in Browser
Navigate to: **http://localhost:5000**

Login with your admin credentials created in Step 8.

## Troubleshooting

### Issue: "No module named 'flask'"
**Solution**: Make sure virtual environment is activated
```powershell
venv\Scripts\Activate.ps1
```

### Issue: Port 5000 already in use
**Solution**: Change port in run.py or kill process using port:
```powershell
# Find process on port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with process ID)
taskkill /PID <PID> /F
```

### Issue: "AttributeError: 'NoneType' object has no attribute..."
**Solution**: Run database initialization:
```powershell
python run.py init_db
python run.py create_sample_data
```

### Issue: C++ Compiler not found (if installing advanced packages)
**Solution**: Skip optional packages or install Visual C++ Build Tools:
1. Download from: https://visualstudio.microsoft.com/downloads/
2. Select "Visual Studio Build Tools"
3. Install C++ build tools
4. Retry pip install

## File Structure
```
d:\library_project\
├── venv\                    # Virtual environment (created)
├── app.py                   # Flask app factory
├── config.py                # Configuration
├── models.py                # Database models
├── run.py                   # Entry point
├── .env                     # Environment variables (create this)
├── requirements.txt         # All dependencies
├── requirements-minimal.txt # Core dependencies only
├── routes\                  # API routes
├── services\                # Email, PDF services
├── templates\               # HTML templates
└── library.db               # SQLite database (created at runtime)
```

## API Usage Examples

### Get all books:
```powershell
curl http://localhost:5000/api/books
```

### Search books:
```powershell
curl "http://localhost:5000/api/search?q=Python"
```

### Borrow a book (requires auth):
```powershell
curl -X POST http://localhost:5000/api/borrow/1 `
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Database Reset (if needed)
To completely reset the database:
```powershell
# Delete the database file
Remove-Item library.db -Force

# Recreate it
python run.py init_db
python run.py create_sample_data
```

## Performance Tips

1. **Enable query optimization:**
   - In config.py, set `SQLALCHEMY_ECHO = False` for production

2. **Use production server:**
   - Don't use Flask development server for production
   - Use Gunicorn or uWSGI:
   ```powershell
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

3. **Enable caching:**
   - Install Redis or Memcached
   - Configure in config.py

## Deployment

### To deploy on Windows Server:
1. Install Python on server
2. Clone project
3. Create virtual environment
4. Install dependencies
5. Configure .env for production
6. Use IIS with FastCGI or
7. Use Gunicorn with a reverse proxy (Nginx)

### To deploy on Linux:
Follow similar steps but use:
- `source venv/bin/activate` instead of `Activate.ps1`
- Run setup.sh: `bash setup.sh`

## Support Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- Check README.md, FEATURES.md in project folder
- Review application logs for errors

## Default Test Account
- **Username**: admin (or your created account)
- **Password**: (your chosen password)

You're all set! Happy library managing! 📚
