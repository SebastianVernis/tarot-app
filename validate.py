#!/usr/bin/env python3
"""
Tarot Místico - Deployment Validation Script
Validates the project structure and configuration before deployment
"""
import os
import sys
import json
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def print_warning(text):
    """Print warning message"""
    print(f"⚠️  {text}")

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print_success(f"Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python version {version.major}.{version.minor} is too old. Need 3.9+")
        return False

def check_file_exists(filepath, required=True):
    """Check if file exists"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print_success(f"{filepath} exists ({size} bytes)")
        return True
    else:
        if required:
            print_error(f"{filepath} not found (required)")
        else:
            print_warning(f"{filepath} not found (optional)")
        return required

def check_json_valid(filepath):
    """Check if JSON file is valid"""
    try:
        with open(filepath, 'r') as f:
            json.load(f)
        print_success(f"{filepath} is valid JSON")
        return True
    except Exception as e:
        print_error(f"{filepath} is invalid: {e}")
        return False

def check_python_syntax(filepath):
    """Check Python file syntax"""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        print_success(f"{filepath} syntax is valid")
        return True
    except SyntaxError as e:
        print_error(f"{filepath} has syntax error: {e}")
        return False

def check_directory_structure():
    """Check required directory structure"""
    required_dirs = ['api', 'routes', 'src', 'public']
    all_exist = True
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            files = len([f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, f))])
            print_success(f"Directory '{dir_name}/' exists ({files} files)")
        else:
            print_error(f"Directory '{dir_name}/' not found")
            all_exist = False
    
    return all_exist

def check_requirements():
    """Check requirements.txt"""
    if not os.path.exists('requirements.txt'):
        print_error("requirements.txt not found")
        return False
    
    with open('requirements.txt', 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print_success(f"requirements.txt has {len(lines)} dependencies")
    
    # Check for critical dependencies
    critical = ['flask', 'flask-cors', 'flask-sqlalchemy', 'flask-jwt-extended']
    missing = []
    
    for dep in critical:
        if not any(dep.lower() in line.lower() for line in lines):
            missing.append(dep)
    
    if missing:
        print_warning(f"Missing critical dependencies: {', '.join(missing)}")
        return False
    
    return True

def check_vercel_config():
    """Check Vercel configuration"""
    if not check_json_valid('vercel.json'):
        return False
    
    with open('vercel.json', 'r') as f:
        config = json.load(f)
    
    # Check builds
    if 'builds' in config and len(config['builds']) > 0:
        print_success(f"Vercel builds configured: {len(config['builds'])}")
    else:
        print_error("No builds configured in vercel.json")
        return False
    
    # Check routes
    if 'routes' in config and len(config['routes']) > 0:
        print_success(f"Vercel routes configured: {len(config['routes'])}")
    else:
        print_warning("No routes configured in vercel.json")
    
    return True

def estimate_deployment_size():
    """Estimate deployment size"""
    total_size = 0
    
    for root, dirs, files in os.walk('.'):
        # Skip archive and git
        dirs[:] = [d for d in dirs if d not in ['.git', '.archive', '__pycache__', 'venv', 'env']]
        
        for file in files:
            filepath = os.path.join(root, file)
            try:
                total_size += os.path.getsize(filepath)
            except:
                pass
    
    size_mb = total_size / (1024 * 1024)
    
    if size_mb < 50:
        print_success(f"Estimated deployment size: {size_mb:.1f} MB (within 50 MB limit)")
        return True
    else:
        print_error(f"Estimated deployment size: {size_mb:.1f} MB (exceeds 50 MB limit)")
        return False

def main():
    """Main validation function"""
    print_header("🔮 Tarot Místico - Deployment Validation")
    
    all_checks = []
    
    # Python version
    print_header("Python Environment")
    all_checks.append(check_python_version())
    
    # Required files
    print_header("Required Files")
    all_checks.append(check_file_exists('vercel.json'))
    all_checks.append(check_file_exists('requirements.txt'))
    all_checks.append(check_file_exists('config.py'))
    all_checks.append(check_file_exists('app.py'))
    all_checks.append(check_file_exists('api/index.py'))
    all_checks.append(check_file_exists('README.md'))
    
    # Optional files
    check_file_exists('.env', required=False)
    check_file_exists('.env.example', required=False)
    
    # Directory structure
    print_header("Directory Structure")
    all_checks.append(check_directory_structure())
    
    # Configuration validation
    print_header("Configuration Validation")
    all_checks.append(check_vercel_config())
    all_checks.append(check_requirements())
    
    # Python syntax
    print_header("Python Syntax Validation")
    all_checks.append(check_python_syntax('api/index.py'))
    all_checks.append(check_python_syntax('config.py'))
    all_checks.append(check_python_syntax('app.py'))
    
    # Deployment size
    print_header("Deployment Size")
    all_checks.append(estimate_deployment_size())
    
    # Summary
    print_header("Validation Summary")
    
    passed = sum(all_checks)
    total = len(all_checks)
    
    if passed == total:
        print_success(f"All {total} checks passed! ✨")
        print("\n🚀 Ready to deploy to Vercel!")
        print("\nNext steps:")
        print("  1. vercel login")
        print("  2. vercel --prod")
        print("  3. Set environment variables in Vercel dashboard")
        return 0
    else:
        print_error(f"{passed}/{total} checks passed")
        print(f"\n❌ Please fix the errors above before deploying")
        return 1

if __name__ == '__main__':
    sys.exit(main())
