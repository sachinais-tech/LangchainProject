# YouTube Script Creator 🎬

A powerful YouTube script generation application built with Streamlit, LangChain, and Ollama. Create engaging, well-structured YouTube scripts with AI assistance.

## Features

- 🎯 **Customizable Script Generation**: Create scripts tailored to your video topic, audience, and style
- ⚙️ **Multiple Configuration Options**: 
  - Select from various Ollama models (llama2, mistral, codellama, phi, neural-chat)
  - Choose video length (5-30 minutes)
  - Select script style (Casual, Professional, Entertaining, etc.)
  - Customize tone and language
- 📝 **Rich Input Options**:
  - Video topic/title
  - Target audience
  - Key points to cover
  - Additional notes and requirements
- ✨ **Smart Features**:
  - Optional hook/introduction
  - Optional call-to-action/outro
  - Optional timestamps
- 💾 **Export Functionality**: Download generated scripts as text files

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running
   - Download from: https://ollama.ai/
   - Install at least one model: `ollama pull llama2` (or any other model)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is running:
```bash
ollama serve
```

3. Pull a model (if you haven't already):
```bash
ollama pull llama2
# or
ollama pull mistral
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. The app will open in your default web browser (usually at `http://localhost:8501`)

3. Fill in the form:
   - Enter your video topic/title
   - Specify target audience (optional)
   - Add key points to cover
   - Select your preferences in the sidebar
   - Click "Generate YouTube Script"

4. Review and download your generated script!

## Configuration

### Available Ollama Models
- `llama2` - General purpose model
- `mistral` - High-performance model
- `codellama` - Code-focused model
- `phi` - Efficient small model
- `neural-chat` - Conversational model

Make sure the model you select is installed in Ollama before using it.

### Script Styles
- **Casual and Conversational**: Friendly, relaxed tone
- **Professional and Educational**: Formal, informative
- **Entertaining and Humorous**: Fun, engaging
- **Inspirational and Motivational**: Uplifting, encouraging
- **Technical and Detailed**: Precise, comprehensive

## Troubleshooting

### Ollama Connection Error
If you see an error about Ollama not being available:
1. Make sure Ollama is installed and running
2. Check that `ollama serve` is running in a terminal
3. Verify the model name is correct and installed

### Model Not Found
If the selected model isn't available:
1. Pull the model: `ollama pull <model-name>`
2. Wait for the download to complete
3. Refresh the app and try again

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Technologies Used

- **Streamlit**: Web application framework
- **LangChain**: LLM integration framework
- **Ollama**: Local LLM runtime
- **LangChain Community**: Community integrations including Ollama

## License

This project is open source and available for personal and commercial use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Note**: The quality of generated scripts depends on the Ollama model you choose and how detailed your input is. Be specific with your topic and key points for best results!

