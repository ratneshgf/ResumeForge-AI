#!/usr/bin/env python3
"""
ResumeForge AI - Automated Setup Script

This script automates the setup process for ResumeForge AI backend.
Run this after installing Python dependencies to download required NLP models.

Usage:
    python setup.py
"""

import subprocess
import sys
import os


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_success(text):
    """Print success message"""
    print(f"✓ {text}")


def print_error(text):
    """Print error message"""
    print(f"✗ {text}")


def print_info(text):
    """Print info message"""
    print(f"ℹ {text}")


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print_error(f"Python {version.major}.{version.minor} detected. Python 3.9+ required.")
        return False
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def download_spacy_model():
    """Download spaCy language model"""
    print_header("Downloading spaCy Model")
    
    try:
        print_info("Downloading en_core_web_md model (this may take a few minutes)...")
        subprocess.run(
            [sys.executable, "-m", "spacy", "download", "en_core_web_md"],
            check=True
        )
        print_success("spaCy model downloaded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to download spaCy model: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False


def download_nltk_data():
    """Download NLTK data packages"""
    print_header("Downloading NLTK Data")
    
    try:
        import nltk
        
        print_info("Downloading stopwords...")
        nltk.download('stopwords', quiet=True)
        print_success("Stopwords downloaded")
        
        print_info("Downloading punkt tokenizer...")
        nltk.download('punkt', quiet=True)
        print_success("Punkt tokenizer downloaded")
        
        return True
    except ImportError:
        print_error("NLTK not installed. Run: pip install nltk")
        return False
    except Exception as e:
        print_error(f"Failed to download NLTK data: {e}")
        return False


def create_storage_directories():
    """Create required storage directories"""
    print_header("Creating Storage Directories")
    
    directories = [
        "storage/uploads",
        "storage/temp",
        "storage/output"
    ]
    
    try:
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print_success(f"Created {directory}")
        return True
    except Exception as e:
        print_error(f"Failed to create directories: {e}")
        return False


def check_env_file():
    """Check if .env file exists and warn about API keys"""
    print_header("Checking Environment Configuration")
    
    if not os.path.exists(".env"):
        print_info("No .env file found. Creating from .env.example...")
        try:
            if os.path.exists(".env.example"):
                with open(".env.example", "r") as src:
                    content = src.read()
                with open(".env", "w") as dst:
                    dst.write(content)
                print_success("Created .env file from template")
            else:
                print_error(".env.example not found")
                return False
        except Exception as e:
            print_error(f"Failed to create .env file: {e}")
            return False
    
    print_info("\nIMPORTANT: Configure your .env file with API keys:")
    print_info("  - GEMINI_API_KEY or OPENAI_API_KEY (REQUIRED for AI features)")
    print_info("  - RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET (for payments)")
    print_info("\nSee SETUP_GUIDE.md for details on getting API keys.")
    
    return True


def verify_dependencies():
    """Verify critical dependencies are installed"""
    print_header("Verifying Dependencies")
    
    required_packages = [
        ("fastapi", "FastAPI"),
        ("spacy", "spaCy"),
        ("sentence_transformers", "Sentence Transformers"),
        ("sklearn", "scikit-learn"),
        ("nltk", "NLTK"),
        ("docx", "python-docx"),
        ("fitz", "PyMuPDF"),
    ]
    
    all_installed = True
    
    for package, display_name in required_packages:
        try:
            __import__(package)
            print_success(f"{display_name} installed")
        except ImportError:
            print_error(f"{display_name} not installed")
            all_installed = False
    
    if not all_installed:
        print_info("\nInstall missing packages with:")
        print_info("  pip install -r requirements.txt")
    
    return all_installed


def print_next_steps():
    """Print next steps for user"""
    print_header("Setup Complete!")
    
    print("Next steps:")
    print()
    print("1. Configure your .env file with API keys:")
    print("   - Edit backend/.env")
    print("   - Add GEMINI_API_KEY or OPENAI_API_KEY")
    print("   - Add RAZORPAY credentials (optional)")
    print()
    print("2. Start the backend:")
    print("   uvicorn app.main:app --reload")
    print()
    print("3. Test the API:")
    print("   Visit http://localhost:8000/docs")
    print()
    print("4. Set up the frontend:")
    print("   cd ../frontend")
    print("   npm install")
    print("   npm run dev")
    print()
    print("For detailed instructions, see SETUP_GUIDE.md")
    print()


def main():
    """Main setup routine"""
    print_header("ResumeForge AI - Automated Setup")
    print("This script will set up all required dependencies and models.")
    print()
    
    # Step 1: Check Python version
    if not check_python_version():
        print("\nSetup failed. Please upgrade Python and try again.")
        return 1
    
    # Step 2: Verify dependencies
    if not verify_dependencies():
        print("\nSetup failed. Please install missing dependencies and try again.")
        return 1
    
    # Step 3: Download spaCy model
    if not download_spacy_model():
        print("\nWarning: spaCy model download failed. ATS scoring may not work.")
    
    # Step 4: Download NLTK data
    if not download_nltk_data():
        print("\nWarning: NLTK data download failed. Some features may not work.")
    
    # Step 5: Create storage directories
    if not create_storage_directories():
        print("\nWarning: Failed to create storage directories.")
    
    # Step 6: Check/create .env file
    if not check_env_file():
        print("\nWarning: Environment configuration may be incomplete.")
    
    # Print next steps
    print_next_steps()
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
