# 📝 Blogger - AI-Powered Content Generation Studio

A sophisticated multi-agent AI system that generates high-quality, SEO-optimized blog content through an iterative review and refinement process.

## ✨ Features

- **Multi-Agent Workflow**: Writer → Editor → Marketer collaboration
- **Quality Assurance**: Automated content review with configurable quality thresholds
- **Iterative Refinement**: Automatic revision cycles based on editor feedback
- **Multi-LLM Support**: Seamlessly switch between Ollama, Google Gemini, and OpenAI
- **Flexible Output**: Publish to screen or save as Markdown files
- **SEO Optimization**: Generates metadata, tags, and optimized URL slugs
- **Professional Profiles**: Consistent AI behavior through role-based instructions
- **Comprehensive Logging**: Debug and info logging throughout the workflow

## 🏗️ Architecture

```
Blog Studio
├── Writer Agent      → Generates blog content
├── Editor Agent      → Reviews and provides feedback
├── Marketer Agent    → Creates SEO metadata
└── Publisher         → Outputs content (Screen/Markdown)

LLM Layer
├── Ollama          → Local model execution
├── Gemini          → Google's generative AI
└── OpenAI          → OpenAI's GPT models

Utilities
├── Extractor       → Parses sections and JSON from LLM responses
├── Logger          → Colored console logging with time tracking
├── Pen             → Terminal color utilities
└── Profiles        → Agent personalities and instructions
```

## 📋 Prerequisites

- **Python 3.10+**
- **pip** or package manager
- **One of**:
  - Ollama running locally (for local models)
  - Google Gemini API key
  - OpenAI API key

## 🚀 Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd blogger
```

### 2. Install dependencies
```bash
pip install -r requirements.pip
```

### 3. Configure environment variables
Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Or manually create `.env` with the following configuration:

```env
# ===== LLM Provider Configuration =====
WRITER_LLM=ollama://llama2:13b
EDITOR_LLM=ollama://llama2:13b
MARKETER_LLM=ollama://llama2:13b

# ===== Global LLM Settings (applies to all providers) =====
CONNECTION_TIMEOUT_SECONDS=15         # Network connection timeout for any LLM provider
OPERATION_TIMEOUT_SECONDS=30          # Maximum time to wait for LLM response

# ===== Ollama Configuration (required only if using Ollama) =====
OLLAMA_API_BASE_URL=http://localhost:11434

# ===== Google Gemini Configuration (required only if using Gemini) =====
GEMINI_API_KEY=your-gemini-api-key-here

# ===== OpenAI Configuration (required only if using OpenAI) =====
OPENAI_API_KEY=your-openai-api-key-here

# ===== Blog Generation Settings =====
BLOG_REVIEW_LIMIT=5
MINIMUM_QUALITY_SCORE=4.5

# ===== Logging =====
LOG_LEVEL=INFO                        # DEBUG for verbose output, INFO for normal

# ===== Debug Options =====
CURL_VERBOSE=false                    # Set to true to see HTTP request/response details
```

## 📖 Usage

### Basic Usage

```bash
python cli.py
```

This will:
1. Generate a blog post for the configured topic
2. Run through iterative review cycles
3. Create SEO metadata
4. Publish the final content to screen

### Customizing Content

Edit `cli.py` to change the blog topic and language:

```python
blog_topic = "Your topic here"
blog_language = "English"  # or any other language
```

### Configuring LLM Providers

Set the environment variables to use different LLMs:

```bash
# Use Ollama local models
export WRITER_LLM=ollama://llama2:13b
export EDITOR_LLM=ollama://llama2:13b
export MARKETER_LLM=ollama://llama2:13b

# Or use Google Gemini
export WRITER_LLM=google://gemini-pro
export EDITOR_LLM=google://gemini-pro
export MARKETER_LLM=google://gemini-pro

# Or use OpenAI
export WRITER_LLM=openai://gpt-4
export EDITOR_LLM=openai://gpt-4
export MARKETER_LLM=openai://gpt-4
```

### Adjusting Quality Settings

```bash
# Minimum quality score (0-5)
export MINIMUM_QUALITY_SCORE=4.5

# Maximum revision attempts
export BLOG_REVIEW_LIMIT=5
```

### Enabling Debug Logging

```bash
export LOG_LEVEL=DEBUG
export CURL_VERBOSE=true
```

## 📁 Project Structure

```
blogger/
├── cli.py                          # Main entry point
├── requirements.pip                # Python dependencies
├── .env                           # Environment configuration (create from .env.example)
│
├── studio/                         # Multi-agent orchestration
│   ├── studio.py                  # Main workflow coordinator
│   ├── writer_agent.py            # Content generation agent
│   ├── editor_agent.py            # Content review agent
│   └── marketer_agent.py          # SEO metadata generation agent
│
├── llm/                           # LLM provider abstraction
│   ├── llm.py                     # Base LLM class
│   ├── factory.py                 # LLM provider factory
│   ├── ollama.py                  # Ollama provider
│   ├── gemini.py                  # Google Gemini provider
│   └── openai.py                  # OpenAI provider
│
├── profiles/                       # Agent personality configurations
│   ├── profiles.py                # Profile registry
│   ├── writers/
│   │   ├── alice.py              # Writer profile (Alice)
│   │   └── profile.py            # Writer profile base class
│   ├── editors/
│   │   ├── bob.py                # Editor profile (Bob)
│   │   └── profile.py            # Editor profile base class
│   └── marketers/
│       ├── carol.py              # Marketer profile (Carol)
│       └── profile.py            # Marketer profile base class
│
├── publisher/                      # Output handlers
│   ├── publisher.py               # Base publisher class
│   ├── screen.py                  # Console output publisher
│   └── markdown.py                # Markdown file publisher
│
├── extractor/                      # Content parsing utilities
│   ├── section.py                 # Extract marked sections from text
│   ├── json_object.py             # Extract JSON objects from text
│   └── __init__.py
│
├── logger/                         # Logging utilities
│   └── logger.py                  # Colored console logger
│
├── pen/                           # Terminal utilities
│   └── pen.py                     # ANSI color codes
│
└── tests/                         # Unit tests
    ├── test_extractor.py
    ├── test_llm_factory.py
    ├── test_logger.py
    └── test_pen.py
```

## 🔧 Workflow

### 1. **Writing Phase**
- WriterAgent receives the blog topic and language
- Generates a comprehensive blog post following professional guidelines
- Focuses on SEO optimization and reader engagement

### 2. **Review Phase**
- EditorAgent reviews the draft
- Provides scores in three dimensions:
  - **Proofreading**: Grammar, spelling, punctuation
  - **Content Quality**: Structure, depth, engagement
  - **Effectiveness & Alignment**: Requirement coverage, audience fit
- Returns feedback for improvement

### 3. **Revision Loop**
- If quality score < threshold and not marked as "flawless":
  - WriterAgent revises content based on feedback
  - EditorAgent reviews the revised version
  - Repeats until content passes quality threshold or max revisions reached

### 4. **Marketing Phase**
- MarketerAgent generates SEO metadata:
  - Optimized title (≤60 chars)
  - Meta description (≤160 chars)
  - URL slug (SEO-friendly)
  - Cover image prompt
  - 5 relevant tags/keywords

### 5. **Publishing**
- Content is formatted and published
- Available outputs:
  - **ScreenPublisher**: Display on console
  - **MarkdownPublisher**: Save as `.md` file

## 🎯 Agent Profiles

### Alice (Writer)
- **Role**: Professional blog content creator
- **Focus**: High-quality, engaging, SEO-optimized content
- **Style**: Clear, concise, professional yet friendly
- **Output**: Markdown-formatted blog posts (1800-2500 words)

### Bob (Editor)
- **Role**: Content quality assurance specialist
- **Focus**: Proofreading, clarity, effectiveness
- **Style**: Constructive and detailed feedback
- **Output**: Quality scores and specific improvement suggestions

### Carol (Marketer)
- **Role**: SEO and marketing strategist
- **Focus**: Metadata optimization for search visibility
- **Style**: Data-driven, audience-focused
- **Output**: JSON metadata with SEO-optimized tags and descriptions

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

Run specific test file:

```bash
python -m pytest tests/test_extractor.py -v
```

## 🔌 LLM Provider Setup

### Using Ollama (Local Models)

1. **Install Ollama**: https://ollama.ai/
2. **Start Ollama server**:
   ```bash
   ollama serve
   ```
3. **Pull a model**:
   ```bash
   ollama pull llama2:13b
   ```
4. **Configure in `.env`**:
   ```env
   WRITER_LLM=ollama://llama2:13b
   OLLAMA_API_BASE_URL=http://localhost:11434
   ```

### Using Google Gemini

1. **Get API Key**: https://makersuite.google.com/app/apikey
2. **Available Models**: https://ai.google.dev/models
   - Popular models: `gemini-pro`, `gemini-1.5-pro`, `gemini-1.5-flash`
   - [View full list of Gemini models →](https://ai.google.dev/models)
3. **Configure in `.env`**:
   ```env
   WRITER_LLM=google://gemini-pro
   GEMINI_API_KEY=your-api-key
   ```

### Using OpenAI

1. **Get API Key**: https://platform.openai.com/api-keys
2. **Available Models**: https://platform.openai.com/docs/models
   - Latest models: `gpt-4`, `gpt-4-turbo`, `gpt-4o`, `gpt-3.5-turbo`
   - [View full list of OpenAI models →](https://platform.openai.com/docs/models)
3. **Configure in `.env`**:
   ```env
   WRITER_LLM=openai://gpt-4
   OPENAI_API_KEY=your-api-key
   ```

## 📊 Configuration Reference

### Global Settings (Apply to All Providers)

| Variable | Default | Description |
|----------|---------|-------------|
| `CONNECTION_TIMEOUT_SECONDS` | `15` | Network connection timeout for **any LLM provider** (seconds) |
| `OPERATION_TIMEOUT_SECONDS` | `30` | Maximum response time for **any LLM provider** (seconds) |
| `LOG_LEVEL` | `INFO` | Logging verbosity: `DEBUG` (verbose) or `INFO` (normal) |
| `CURL_VERBOSE` | `false` | Set to `true` to see detailed HTTP request/response logs |

### LLM Provider Selection

| Variable | Default | Description |
|----------|---------|-------------|
| `WRITER_LLM` | `ollama://llama2:13b` | LLM for content generation (`ollama://`, `google://`, or `openai://`) |
| `EDITOR_LLM` | `ollama://llama2:13b` | LLM for content review |
| `MARKETER_LLM` | `ollama://llama2:13b` | LLM for metadata generation |

### Provider-Specific Settings

**Ollama** (required only if using `ollama://` providers)
| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_API_BASE_URL` | — | Base URL of Ollama server (e.g., `http://localhost:11434`) |

**Google Gemini** (required only if using `google://` providers)
| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | — | Your Google Gemini API key |

**OpenAI** (required only if using `openai://` providers)
| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | Your OpenAI API key |

### Blog Generation Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `BLOG_REVIEW_LIMIT` | `5` | Maximum number of revision cycles |
| `MINIMUM_QUALITY_SCORE` | `4.5` | Minimum required quality score (0-5 scale) |

## 🐛 Troubleshooting

### "Connection refused" errors
- **Ollama**: Ensure Ollama server is running on the configured URL
- **Check**: `curl http://localhost:11434/api/tags`

### "API key invalid" errors
- Verify API keys in `.env` are correct
- Check API key has required permissions

### Low quality scores
- Increase `OPERATION_TIMEOUT_SECONDS` for more thoughtful LLM responses
- Verify LLM model is appropriate for the task
- Try with a more capable model (e.g., `gpt-4` instead of `gpt-3.5-turbo`)

### Timeout errors
- Increase `CONNECTION_TIMEOUT_SECONDS` and `OPERATION_TIMEOUT_SECONDS`
- Check network connectivity
- Reduce simultaneous requests

### Memory issues with Ollama
- Use a smaller model: `ollama://llama2:7b`
- Allocate more system resources to Ollama

## 💡 Best Practices

1. **Start with a good LLM**: More capable models produce better initial drafts
2. **Adjust quality thresholds**: Set `MINIMUM_QUALITY_SCORE` based on your needs
3. **Monitor timeouts**: Larger models need more time
4. **Use consistent models**: Using the same model for all agents reduces inconsistency
5. **Review logs**: Enable `LOG_LEVEL=DEBUG` when troubleshooting
6. **Test locally first**: Use Ollama before moving to cloud APIs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

[Add your license information here]

## 📧 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Happy blogging!** 🚀

Generated with ❤️ for the Blogger project
