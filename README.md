# Discord AI Bot with Memory

A Discord bot powered by a local LLM (Large Language Model) that maintains persistent memory of user interactions. This bot runs language models locally using `llama-cpp-python` for privacy and control, while remembering user facts and preferences across conversations.

## Features

- **Local LLM Integration**: Runs language models locally using `llama-cpp-python` with GPU acceleration support
- **Persistent Memory**: Learns and remembers user facts and preferences across conversations
- **Discord Integration**: Easy-to-use Discord bot with intuitive command interface
- **GPU Acceleration**: Supports offloading all model layers to GPU for faster inference
- **Long Context Window**: 9168 token context window for richer conversations
- **Automatic Response Chunking**: Handles Discord's 2000 character message limit by splitting long responses

## Prerequisites

- Python 3.8+
- Discord bot token
- Hugging Face API token (for downloading models)
- NVIDIA GPU (recommended for performance, CPU fallback available)
- CUDA toolkit (if using GPU acceleration)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd discord_bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Key dependencies:
   - `discord.py` - Discord bot framework
   - `llama-cpp-python` - Local LLM inference
   - `huggingface-hub` - Model downloading
   - `python-dotenv` - Environment variable management

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```
   DISCORD_SECRET=your_discord_bot_token
   REPO_ID=model_repository_id
   FILENAME=model_filename
   CACHE_DIR=path_to_model_cache
   ```

   - `DISCORD_SECRET`: Your Discord bot token (get from [Discord Developer Portal](https://discord.com/developers/applications))
   - `REPO_ID`: Hugging Face model repository (e.g., `mistralai/Mistral-7B-Instruct-v0.1`)
   - `FILENAME`: The model file within the repository (e.g., `mistral-7b-instruct-v0.1.Q4_K_M.gguf`)
   - `CACHE_DIR`: Directory to cache downloaded models

## Usage

1. **Start the bot**
   ```bash
   python discord_bot.py
   ```

2. **In Discord, use the `!speak` command**
   ```
   !speak What's my favorite color?
   ```

The bot will:
- Analyze the message for user facts/preferences
- Generate a response using the local LLM with your saved memories
- Remember relevant information for future conversations
- Handle long responses by splitting them into chunks

## Project Structure

- **discord_bot.py** - Main bot entry point with Discord event handlers and command definitions
- **llm.py** - LLM inference logic, model initialization, and memory analysis
- **memory.py** - User memory persistence using JSON storage
- **memories.json** - Persistent user memory storage (auto-generated)

## How It Works

### Memory System

1. **Message Analysis**: When you send a message, the bot analyzes it to determine if it contains user-specific facts or preferences
2. **Memory Storage**: Relevant information is extracted and stored in `memories.json` with user-specific summaries
3. **Context Injection**: User memories are injected into the system prompt for subsequent interactions
4. **Personalization**: The bot personalizes responses using your stored facts without confusing them as its own

### LLM Integration

- Models are downloaded from Hugging Face and cached locally
- The bot uses the `Llama` class from `llama-cpp-python` for inference
- GPU acceleration is automatically attempted (set to `-1` to offload all layers)
- Response cleaning removes internal thinking tags before sending to Discord

## Configuration

### Model Performance Tuning

In `llm.py`, you can adjust:
- `n_gpu_layers=-1` - Control GPU layer offloading (-1 = all layers)
- `n_ctx=9168` - Context window size (affects memory usage and capability)
- `temperature=0.1` - Lower for consistent, deterministic outputs

### Memory Retention

The memory system stores all extracted facts in `memories.json`. To clear memory for a user, remove their entry from the JSON file.

## Troubleshooting

**Bot doesn't start**
- Check that all environment variables are set correctly in `.env`
- Verify Discord bot token is valid
- Ensure the model file exists in the specified cache directory

**Slow responses**
- Enable GPU acceleration (verify CUDA is installed)
- Reduce `n_ctx` for faster inference
- Use a smaller model variant

**Memory not working**
- Check that `memories.json` is writable
- Verify the LLM is properly analyzing messages (check console debug output)

**Out of memory errors**
- Reduce `n_gpu_layers` value
- Use a smaller model
- Decrease `n_ctx`

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests for improvements.

## License

This project is open source. Please check the LICENSE file for details.

## Disclaimer

This bot uses local LLM models. Ensure you have the necessary permissions and resources to run them. GPU memory requirements vary by model - typically 4-24GB depending on model size.
