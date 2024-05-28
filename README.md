### Features
- Text-to-Speech
- Long-term memory
- Blushing
- Egg

---

### Dependencies
```bat
pip install python-dotenv
pip install SpeechRecognition
pip install google-generativeai
pip install torch
pip install num2words
pip install pillow
pip install chromadb
```

---

### Implementation

Response generation
- [Gemini 1.0 API](https://ai.google.dev/gemini-api)
- Replace `GEMINI_API_KEY` in [`env`](src/.env) with your actual api key

GUI
- Python [tkinter](https://docs.python.org/3/library/tkinter.html)

TTs
- Uses the pre-trained Silero [v3_en model](https://models.silero.ai/models/tts/en/)

Long-term memory
- Stores prompts and responses into a vector database using chromadb
- Queries the database and gets the top 3 most similar past conversations to add additional context to the current prompt
- [Reference](https://brain.d.foundation/Engineering/AI/Dealing+with+Long-Term+Memory+in+AI+Chatbot)

---

### Commands
`exit`
- Closes the program

`reset`
- Deletes all conversation history and resets the AI's memory
