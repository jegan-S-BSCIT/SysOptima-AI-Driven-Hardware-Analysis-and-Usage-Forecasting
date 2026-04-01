# Gemini AI Integration Guide for SysOptima Desktop App

## Overview

This guide explains how to integrate the **Gemini AI Assistant** into your existing SysOptima Tkinter desktop application.

---

## 🎯 Key Principles

### 1. **Rule-Based First** (PRIMARY)
- System diagnostics use rule-based logic
- Always try diagnostic rules first
- Only use Gemini if rules don't match

### 2. **Gemini as Fallback** (OPTIONAL)
- Natural language conversation only
- Educational responses
- Never overrides diagnostics
- Gracefully disabled if API unavailable

### 3. **Academic Appropriate**
- Explainable AI (not black-box)
- Transparent decision making
- All logic is traceable
- Perfect for viva/presentation

---

## 🔧 Setup Instructions

### Step 1: Add Gemini API Key to `.env`

Edit your `.env` file:

```bash
# .env

# ... existing variables ...

# Google Gemini API
GEMINI_API_KEY=your-actual-api-key-here
```

**How to get a Gemini API key:**
1. Go to: https://ai.google.dev/
2. Click "Get API Key"
3. Create/select project
4. Copy the API key
5. Paste into `.env` file

### Step 2: Install/Verify Dependencies

```bash
pip install google-generativeai
```

(Already in your requirements.txt)

### Step 3: Import in Your Desktop App

In your `ui/modern_ui.py` or main Tkinter application:

```python
from core.gemini_ai_assistant import HybridAILogic, GeminiAIAssistant
```

---

## 💻 Integration Examples

### Example 1: Simple Chat Interface

```python
from core.gemini_ai_assistant import HybridAILogic

class ChatWidget:
    def __init__(self):
        # Initialize hybrid AI
        self.ai = HybridAILogic()
    
    def on_send_message(self, user_query, system_metrics):
        """Handle user message"""
        # Process through hybrid logic
        response = self.ai.process_query(user_query, system_metrics)
        
        # Display in chat
        self.display_message(f"User: {user_query}")
        self.display_message(response)
```

### Example 2: Adding AI Chat to Existing Tkinter App

```python
import customtkinter as ctk
from core.gemini_ai_assistant import HybridAILogic
import psutil

class AIAssistantTab:
    def __init__(self, parent):
        self.ai = HybridAILogic()
        
        # Create UI
        self.frame = ctk.CTkFrame(parent)
        
        # Chat display
        self.chat_display = ctk.CTkTextbox(
            self.frame, 
            height=300
        )
        self.chat_display.pack(pady=10, padx=10, fill="both", expand=True)
        self.chat_display.configure(state="disabled")
        
        # Input frame
        input_frame = ctk.CTkFrame(self.frame)
        input_frame.pack(pady=5, padx=10, fill="x")
        
        self.input_field = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Ask anything..."
        )
        self.input_field.pack(side="left", fill="x", expand=True, padx=5)
        
        send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            command=self.send_message
        )
        send_btn.pack(side="right", padx=5)
    
    def send_message(self):
        """Send message and get AI response"""
        query = self.input_field.get()
        if not query.strip():
            return
        
        # Get current system metrics
        metrics = {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'gpu_available': True  # Check your GPU detection
        }
        
        # Process query
        response = self.ai.process_query(query, metrics)
        
        # Display in chat
        self.append_chat(f"You: {query}")
        self.append_chat(f"\n{response}\n")
        
        # Clear input
        self.input_field.delete(0, "end")
    
    def append_chat(self, text):
        """Add text to chat display"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", text + "\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")
```

### Example 3: API Connection Status

```python
from core.gemini_ai_assistant import GeminiAIAssistant

def show_api_status(root):
    gemini = GeminiAIAssistant()
    status = gemini.check_api_connection()
    
    message = f"""
    Gemini AI Status:
    - Connected: {status['connected']}
    - Model: {status['model']}
    - Available: {status['available']}
    """
    
    if status['error']:
        message += f"\n- Error: {status['error']}"
    
    print(message)
```

---

## 🧪 Testing

### Method 1: Run Built-in Test

```bash
python core/gemini_ai_assistant.py
```

Output:
```
============================================================
SysOptima Gemini AI Integration Test
============================================================

1. Initializing Gemini Assistant...
   Connected: True
   Model: gemini-2.5-flash
   Available: True

2. Initializing Hybrid AI Logic...
   ✓ Hybrid logic initialized

3. Testing Sample Queries:
...
✓ Integration test complete!
```

### Method 2: Test in Python

```python
from core.gemini_ai_assistant import HybridAILogic

# Initialize
ai = HybridAILogic()

# Test API
response = ai.process_query("hello gemini")
print(response)  # Should show: "✅ Gemini API is working correctly."

# Test rule-based
response = ai.process_query("What about my CPU?")
print(response)  # Should show CPU diagnostic

# Test Gemini fallback
response = ai.process_query("Tell me a joke about computers")
print(response)  # Gemini response with humor
```

---

## 📊 Query Types

### 1. **API Test Queries** (Testing connection)
```
"hello gemini"
"hello google ai"
"test gemini"
"is gemini working"
```
Response: `✅ Gemini API is working correctly.` or error

### 2. **Rule-Based Diagnostic Queries** (Automatic matching)
```
"What's my CPU usage?"
"Tell me about my RAM"
"How's my disk?"
"My GPU status?"
"Why is my computer slow?"
```
Response: Diagnostic information

### 3. **Conversational Queries** (Gemini handles)
```
"Explain what CPU means"
"How do I optimize my system?"
"What's the difference between SSD and HDD?"
"Tell me about computers"
```
Response: Gemini-generated explanation

---

## 🚨 Error Handling

### Common Issues & Solutions

#### Issue 1: `GEMINI_API_KEY not found`
**Solution:**
1. Check `.env` file exists in project root
2. Verify variable name is exactly: `GEMINI_API_KEY`
3. Restart your application

#### Issue 2: `API key authentication failed`
**Solution:**
1. Verify API key is correct from ai.google.dev
2. Check for extra spaces/newlines in `.env`
3. Regenerate new API key if needed

#### Issue 3: `Rate limit exceeded`
**Solution:**
- Normal on free tier
- Add delay between requests
- Use caching for repeated queries

#### Issue 4: `Connection timeout`
**Solution:**
- Check internet connection
- Verify firewall allows Python
- Try again in a few seconds

---

## 🔐 Security Best Practices

✅ **DO:**
- Store API key in `.env` file
- Read API key from environment variable
- Add `.env` to `.gitignore`
- Use minimal API calls
- Cache responses when possible

❌ **DON'T:**
- Hardcode API key in source code
- Commit `.env` to git
- Share API key publicly
- Make unnecessary API calls
- Use API for sensitive data

---

## 📝 Code Comments Explained

### Why Rule-Based First?
```python
# Rule-based responses are:
# 1. Deterministic (always same answer for same query)
# 2. Fast (no network latency)
# 3. Academic-appropriate (explainable)
# 4. No API costs
# Only use Gemini if rules don't match
```

### Why Optional Gemini?
```python
# Gemini is optional because:
# 1. Free tier has rate limits
# 2. Requires internet connection
# 3. API key might be missing
# 4. System should work without it
# Graceful fallback if unavailable
```

### Why Hybrid Logic?
```python
# Hybrid approach provides:
# 1. Best of both worlds (fast + smart)
# 2. Fallback system (robustness)
# 3. Educational (explainable)
# 4. Academic-appropriate
# Priority: Rules > Gemini > Error message
```

---

## 🎓 For Viva Presentation

### Key Points to Explain:

1. **Why Gemini is Optional**
   - Not required for core functionality
   - Gracefully disabled if API unavailable
   - Rule-based system is primary

2. **Hybrid Logic Benefits**
   - Fast rule-based responses (diagnostic)
   - Smart Gemini responses (conversational)
   - No single point of failure
   - Explainable AI (not black-box)

3. **Academic Appropriateness**
   - All decisions are traceable
   - No hidden AI decision-making
   - Transparent system architecture
   - Educational responses

4. **Example Architecture**
   ```
   User Query
       ↓
   API Test? → Show Status
       ↓
   Rule Match? → Return Diagnostic
       ↓
   Gemini Available? → Get Response
       ↓
   Show Error & Help
   ```

---

## 📚 Additional Resources

- **Google Generative AI Docs:** https://ai.google.dev/
- **Gemini API Reference:** https://ai.google.dev/api/python/google/generativeai
- **Best Practices:** https://ai.google.dev/responsible_ai_guidelines

---

## ✅ Integration Checklist

- [ ] Added GEMINI_API_KEY to `.env`
- [ ] Installed google-generativeai package
- [ ] Imported HybridAILogic in main app
- [ ] Created AI chat widget/tab
- [ ] Connected to system metrics
- [ ] Tested "hello gemini" command
- [ ] Tested rule-based queries
- [ ] Tested conversational queries
- [ ] Verified error handling
- [ ] Added to README/documentation

---

**Your SysOptima desktop app now has optional Gemini AI support! 🚀**
