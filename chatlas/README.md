# ChatLas - AI Analytics Assistant

ChatLas is an intelligent analytics assistant that provides natural language access to your DuckDB data through both terminal and web interfaces.

## 🚀 Quick Start

### Prerequisites
- Backend server running on `http://localhost:8000`
- OpenAI API key in `.env` file

### Setup
```bash
# Create environment file
echo "OPENAI_API_KEY=your_key_here" > .env

# Install dependencies (if not already done)
pip install -r ../requirements.txt
```

### Usage

#### Terminal Interface
```bash
python main.py
```

#### Web Interface
```bash
python run_shiny.py
# Open http://localhost:8080
```

## 🤖 AI Capabilities

ChatLas understands natural language queries and automatically:
- **Selects appropriate API endpoints** via MCP integration
- **Processes and analyzes data** using advanced utilities
- **Chains multiple operations** for complex insights
- **Handles errors gracefully** with fallback options

### Example Queries

**Basic Data Retrieval:**
- "What product categories do we have?"
- "Show me the latest sales transactions"
- "List our top customers"

**Advanced Analytics:**
- "Compare sales performance across all product categories"
- "Analyze customer distribution by city and country"
- "What's the difference between weekend and weekday sales?"

**Complex Insights:**
- "Generate comprehensive business insights from all available data"
- "Show me pricing analysis for each product category"
- "Who are our best customers and what do they typically buy?"

## 🔧 Technical Architecture

### AI Model
- **OpenAI GPT-4o** for natural language understanding
- **Streaming responses** for real-time interaction
- **Tool calling** with automatic function selection

### Tool Categories

**MCP Tools (from FastAPI):**
- `get_products`, `get_customers`, `get_dates` - Dimension data
- `get_sales`, `get_sales_by_customer` - Transaction data
- `get_sales_by_category`, `get_top_customers` - Analytics
- `execute_sql`, `get_sql_tables` - Custom queries

**Data Processing Tools:**
- `get_unique_values` - Extract unique field values
- `summarize_numeric_field` - Statistical summaries
- `count_by_field` - Value frequency analysis
- `filter_data`, `group_by_field`, `sort_data` - Data manipulation

**Advanced Analysis Tools:**
- `extract_unique_categories` - Process product categories
- `analyze_products_data` - Product statistical analysis
- `analyze_customer_data` - Customer demographic analysis
- `analyze_sales_data` - Sales pattern analysis
- `compare_categories` - Multi-category performance comparison
- `generate_insights` - Comprehensive business intelligence

### Architecture Benefits

1. **Automatic Tool Discovery** - FastAPI endpoints become AI tools via MCP
2. **Type Safety** - Parameter validation preserved from FastAPI to AI
3. **Modular Design** - Chainable tools for complex workflows
4. **Error Resilience** - Graceful handling of connection issues
5. **Real-time Streaming** - Live responses in both interfaces

## 📁 File Structure

```
chatlas/
├── main.py              # Terminal chat interface (async)
├── shiny_app.py         # Web application (Shiny Core format)
├── run_shiny.py         # Web app launcher (uvicorn)
├── .env                 # Environment variables (create this)
└── tools/
    ├── data_utils.py    # Data processing utilities
    └── chain_tools.py   # Advanced analysis functions
```

## 🛠️ Development

### Adding New Tools

1. **For API-based tools**: Add new FastAPI endpoints with `operation_id`
2. **For processing tools**: Add functions to `data_utils.py`
3. **For complex analysis**: Add functions to `chain_tools.py`

### Tool Function Requirements

```python
def your_tool_function(param: Type) -> ReturnType:
    """
    Clear description of what this tool does.

    Args:
        param: Description of parameter
    """
    # Implementation here
    return result
```

- **Docstring required** - Used by AI for tool selection
- **Type hints required** - Ensures proper parameter handling
- **Function name ≤64 chars** - OpenAI tool name limit
- **Error handling** - Return error messages, don't raise exceptions

### Testing

Both interfaces connect to the same backend and use the same tools:

```bash
# Test terminal interface
python main.py

# Test web interface
python run_shiny.py
```

## 🔍 Troubleshooting

**"MCP connection timed out"**
- Ensure backend server is running on port 8000
- Check `http://localhost:8000/health` responds with `{"status": "healthy"}`

**"Cannot use async tools in synchronous chat"**
- Make sure you're using the correct async/sync methods
- Terminal uses async, web app handles async internally

**"Tool name too long"**
- Function names must be ≤64 characters
- Use concise but descriptive names

**Web app won't start**
- Check port 8080 is available
- Ensure all dependencies installed: `pip install -r ../requirements.txt`

## 🌟 Tips for Best Results

1. **Be specific in queries** - "Top 5 customers by sales amount" vs "show customers"
2. **Ask for analysis** - "Compare and analyze..." gets better insights
3. **Chain requests** - "Show categories, then analyze the Electronics category"
4. **Use natural language** - The AI understands conversational queries
5. **Ask for explanations** - "Explain the weekend vs weekday sales pattern"

---

**ChatLas makes data analytics as easy as having a conversation!** 🚀