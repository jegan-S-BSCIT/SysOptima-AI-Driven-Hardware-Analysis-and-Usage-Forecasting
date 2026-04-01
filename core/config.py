"""
Configuration Management
Centralized loader for environment variables.
Supports Perplexity AI, Google Gemini, and local-only modes.
"""
import os
from dotenv import load_dotenv

# Load .env file immediately
load_dotenv()

class Config:
    # ====================================================
    # Perplexity AI Configuration (PRIMARY)
    # ====================================================
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
    PERPLEXITY_MODEL = os.getenv("PERPLEXITY_MODEL", "sonar")
    PERPLEXITY_API_BASE_URL = os.getenv("PERPLEXITY_API_BASE_URL", "https://api.perplexity.ai")
    
    # ====================================================
    # Groq AI Configuration
    # ====================================================
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GROQ_API_BASE_URL = os.getenv("GROQ_API_BASE_URL", "https://api.groq.com/openai/v1")

    # ====================================================
    # Google Gemini Configuration (LEGACY - for compatibility)
    # ====================================================
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
    
    # ====================================================
    # Environment & Debug
    # ====================================================
    APP_ENV = os.getenv("APP_ENV", "production")
    DEBUG = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    # ====================================================
    # AI Settings
    # ====================================================
    AI_MODE = os.getenv("AI_MODE", "perplexity")  # perplexity, gemini, local
    AI_PROVIDER = os.getenv("AI_PROVIDER", "perplexity")
    
    # ====================================================
    # API Settings
    # ====================================================
    LOCAL_API_BASE = os.getenv("LOCAL_API_BASE_URL", "http://localhost:5000")
    
    # ====================================================
    # Methods
    # ====================================================
    
    @classmethod
    def is_perplexity_enabled(cls):
        """Check if Perplexity AI is properly configured"""
        return cls.PERPLEXITY_API_KEY is not None and len(cls.PERPLEXITY_API_KEY) > 10

    @classmethod
    def is_gemini_enabled(cls):
        """Check if Gemini is properly configured (legacy)"""
        return cls.GEMINI_API_KEY is not None and len(cls.GEMINI_API_KEY) > 10

    @classmethod
    def is_groq_enabled(cls):
        """Check if Groq AI is properly configured"""
        return cls.GROQ_API_KEY is not None and len(cls.GROQ_API_KEY) > 10

    @classmethod
    def is_ai_enabled(cls):
        """Check if any AI provider is enabled"""
        return cls.is_perplexity_enabled() or cls.is_gemini_enabled() or cls.is_groq_enabled()

    @classmethod
    def get_model_name(cls):
        """Get active model name based on provider"""
        if cls.AI_MODE == "perplexity":
            return cls.PERPLEXITY_MODEL
        elif cls.AI_MODE == "groq":
            return cls.GROQ_MODEL
        elif cls.AI_MODE == "gemini":
            return "gemini-1.5-flash"
        return "local"

    @classmethod
    def get_ai_provider(cls):
        """Get configured AI provider"""
        return cls.AI_PROVIDER or cls.AI_MODE

print(f"[{Config.APP_ENV.upper()}] Config loaded. AI Mode: {Config.AI_MODE}, Provider: {Config.get_ai_provider()}")
