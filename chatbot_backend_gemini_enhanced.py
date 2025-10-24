import os
import json
import re
from openai import OpenAI
from gtts import gTTS
from io import BytesIO

# --- Configuration ---
# Using Gemini 2.0 Flash Thinking Experimental - Best for theological reasoning
# This model is FREE and more intelligent than Llama 3.3 70B
MODEL_NAME = "gemini-2.0-flash-thinking-exp"
BIBLE_DATA_PATH = "telugu_bible.json"
TTS_OUTPUT_PATH = "tts_output.mp3"

# Initialize OpenAI client with Google AI Studio
# Get your FREE API key from: https://aistudio.google.com/apikey
try:
    api_key = os.environ.get("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY_HERE")
    client = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=api_key
    )
    print(f"✅ Gemini 2.0 Flash Thinking initialized successfully!")
    print(f"   Model: {MODEL_NAME}")
    print(f"   Intelligence: Advanced reasoning & theological understanding")
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Please set GOOGLE_API_KEY environment variable.")
    print("Get your FREE key from: https://aistudio.google.com/apikey")
    client = None

# --- Bible Data Loading ---
def load_bible_data():
    """Loads the Telugu Bible data from a JSON file."""
    if not os.path.exists(BIBLE_DATA_PATH):
        print(f"Error: Bible data file not found at {BIBLE_DATA_PATH}")
        return None
    with open(BIBLE_DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

BIBLE_DATA = load_bible_data()

# --- Enhanced System Prompt for Deeper Theological Understanding ---
SYSTEM_PROMPT = """
You are 'Yesu Mitra' (Friend of Jesus), a deeply knowledgeable biblical scholar and devoted Jesus-believer.
Your expertise combines theological depth with warm, compassionate guidance rooted in Scripture.

CORE PRINCIPLES:
1. **Deep Theological Understanding**: Before answering, reflect on the meaning, context, and theological significance of relevant Bible verses. Consider the original audience, historical setting, and how it applies today.

2. **Jesus-Centered Theology**: All answers should point to Jesus Christ as the center of faith. Interpret Old Testament passages through the lens of Christ's fulfillment.

3. **Contextual Wisdom**: Don't just quote verses—explain their meaning, the "why" behind God's commands, and how they reveal His character and love.

4. **Pastoral Care**: Approach every question with the heart of a shepherd. Understand the emotional and spiritual needs behind the question.

5. **Doctrinal Soundness**: Base answers on orthodox Christian theology, respecting the authority of Scripture while being sensitive to denominational differences.

RESPONSE STRUCTURE:
1. **Opening**: Warm, personal greeting acknowledging their spiritual journey
2. **Theological Insight**: Deep reflection on what the Bible teaches about their question
3. **Scriptural Foundation**: Present relevant verses with explanation of their meaning and context
4. **Practical Application**: How does this truth apply to their life today?
5. **Prayer/Encouragement**: Close with hope, encouragement, or a brief prayer point

FORMAT:
- Start with compassionate acknowledgment of their question
- Provide 2-3 paragraphs of theological reflection BEFORE listing verses
- Then include section: "**Relevant Scriptures (సంబంధిత లేఖనాలు):**"
- List verses with brief explanations of their significance
- End with practical application and encouragement

SPECIAL MODES:
- **Simple Language**: If requested, use simple Telugu/English, explain like teaching a child
- **Historical Context**: If requested, provide background on authorship, setting, and cultural context
- **Denominational Sensitivity**: Respect different Christian traditions in your answers

Remember: You're not just answering questions—you're shepherding souls toward deeper faith in Christ.
"""

# --- Helper Functions ---
def find_relevant_verses(query: str, bible_data: dict) -> list:
    """
    Uses Gemini's advanced reasoning to identify theologically relevant verses.
    This model understands deeper connections between concepts and scriptures.
    """
    if not bible_data:
        return []

    # Telugu-English book mapping
    book_map = {
        "Genesis": "ఆదికాండము", "Exodus": "నిర్గమకాండము", "Leviticus": "లేవీయకాండము",
        "Numbers": "సంఖ్యాకాండము", "Deuteronomy": "ద్వితీయోపదేశకాండమ", "Joshua": "యెహొషువ",
        "Judges": "న్యాయాధిపతులు", "Ruth": "రూతు", "1 Samuel": "సమూయేలు మొదటి గ్రంథము",
        "2 Samuel": "సమూయేలు రెండవ గ్రంథము", "1 Kings": "రాజులు మొదటి గ్రంథము",
        "2 Kings": "రాజులు రెండవ గ్రంథము", "1 Chronicles": "దినవృత్తాంతములు మొదటి గ్రంథము",
        "2 Chronicles": "దినవృత్తాంతములు రెండవ గ్రంథము", "Ezra": "ఎజ్రా", "Nehemiah": "నెహెమ్యా",
        "Esther": "ఎస్తేరు", "Job": "యోబు గ్రంథము", "Psalms": "కీర్తనల గ్రంథము",
        "Proverbs": "సామెతలు", "Ecclesiastes": "ప్రసంగి", "Song of Songs": "పరమగీతము ",
        "Isaiah": "యెషయా గ్రంథము ", "Jeremiah": "యిర్మీయా", "Lamentations": "విలాపవాక్యములు",
        "Ezekiel": "యెహెజ్కేలు", "Daniel": "దానియేలు", "Hosea": "హొషేయ", "Joel": "యోవేలు",
        "Amos": "ఆమోసు", "Obadiah": "ఓబద్యా", "Jonah": "యోనా", "Micah": "మీకా ",
        "Nahum": "నహూము", "Habakkuk": "హబక్కూకు", "Zephaniah": "జెఫన్యా", "Haggai": "హగ్గయి",
        "Zechariah": "జెకర్యా", "Malachi": "మలాకీ", "Matthew": "మత్తయి సువార్త",
        "Mark": "మార్కు సువార్త", "Luke": "లూకా సువార్త", "John": "యోహాను సువార్త",
        "Acts": "అపొస్తలుల కార్యములు", "Romans": "రోమీయులకు", "1 Corinthians": "1 కొరింథీయులకు",
        "2 Corinthians": "2 కొరింథీయులకు", "Galatians": "గలతీయులకు", "Ephesians": "ఎఫెసీయులకు",
        "Philippians": "ఫిలిప్పీయులకు", "Colossians": "కొలొస్సయులకు",
        "1 Thessalonians": "1 థెస్సలొనీకయులకు", "2 Thessalonians": "2 థెస్సలొనీకయులకు",
        "1 Timothy": "1 తిమోతికి", "2 Timothy": "2 తిమోతికి", "Titus": "తీతుకు",
        "Philemon": "ఫిలేమోనుకు", "Hebrews": "హెబ్రీయులకు", "James": "యాకోబు",
        "1 Peter": "1 పేతురు", "2 Peter": "2 పేతురు", "1 John": "1 యోహాను",
        "2 John": "2 యోహాను", "3 John": "3 యోహాను", "Jude": "యూదా",
        "Revelation": "ప్రకటన గ్రంథము"
    }

    # Enhanced prompt for theological verse selection
    reference_prompt = f"""
As a biblical scholar and theologian, identify 5-7 Bible verses that deeply address this question: "{query}"

Consider:
1. Theological relevance and depth
2. Both direct answers and related principles
3. Old Testament foundations and New Testament fulfillment
4. Jesus' teachings when applicable
5. Pastoral wisdom for the questioner's soul

List ONLY the references in English format (Book Chapter:Verse), comma-separated.
Example: John 3:16, Romans 8:28, Psalm 23:1

Book names must be from this list: {list(book_map.keys())}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a theological scholar selecting the most relevant Bible verses."},
                {"role": "user", "content": reference_prompt}
            ],
            temperature=0.3  # Lower for more focused theological selection
        )

        references_string = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling Gemini for references: {e}")
        return []

    # Parse references and retrieve Telugu text
    references = [ref.strip() for ref in references_string.split(',') if ref.strip()]
    retrieved_verses = []

    for ref in references:
        match = re.match(r"(\d?\s*[A-Za-z\s]+)\s*(\d+):(\d+)", ref)
        if match:
            eng_book, chapter, verse = match.groups()
            eng_book = eng_book.strip()

            telugu_book = book_map.get(eng_book)
            if telugu_book and telugu_book in bible_data:
                try:
                    verse_text = bible_data[telugu_book][str(chapter)][str(verse)]
                    retrieved_verses.append(f"**[{telugu_book} {chapter}:{verse}]** - {verse_text}")
                except (KeyError, TypeError):
                    print(f"Warning: Could not find verse for {ref} in data.")

    return retrieved_verses

def generate_tts_audio(text: str, filename: str = TTS_OUTPUT_PATH):
    """Generates Telugu Text-to-Speech audio."""
    try:
        tts = gTTS(text=text, lang='te')
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None

def chat_with_yesu_mitra(user_query: str) -> dict:
    """
    Main function with enhanced theological understanding.
    Uses Gemini 2.0 Flash Thinking for deep reasoning.
    """
    if not client or not BIBLE_DATA:
        return {"response": "The chatbot service is currently unavailable due to a configuration error.", "audio_path": None}

    # 1. Retrieve relevant verses
    verse_list = find_relevant_verses(user_query, BIBLE_DATA)
    verses_for_llm = "\n".join(verse_list)

    # 2. Enhanced prompt for theological depth
    full_prompt = f"""
User's Question: {user_query}

---
THEOLOGICAL CONTEXT - Relevant Bible Verses:
{verses_for_llm}

---
INSTRUCTIONS:
1. First, THINK DEEPLY about what these verses mean theologically
2. Consider the heart of the questioner and their spiritual need
3. Provide a warm, compassionate answer that:
   - Opens with personal acknowledgment
   - Offers 2-3 paragraphs of theological insight
   - Explains what God reveals through these verses
   - Includes the verses in a "Relevant Scriptures" section
   - Ends with practical application and encouragement

Remember: You're shepherding a soul, not just answering a question.
"""

    # 3. Detect special modes
    is_simple_language = any(k in user_query.lower() for k in ["simple language", "సులభమైన భాష", "child", "beginner", "easy words"])
    is_context_request = any(k in user_query.lower() for k in ["context", "historical", "situation", "who wrote", "చారిత్రక", "సందర్భం", "background"])

    current_system_prompt = SYSTEM_PROMPT
    if is_simple_language:
        current_system_prompt += "\n**SPECIAL: Use very simple language, like explaining to a child or new believer.**"
    if is_context_request:
        current_system_prompt += "\n**SPECIAL: Include historical and cultural context in a dedicated section.**"

    # 4. Call Gemini 2.0 Flash Thinking (advanced reasoning)
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": current_system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7  # Balanced for warmth and accuracy
        )

        final_response_text = response.choices[0].message.content.strip()
    except Exception as e:
        final_response_text = f"My dear friend, I am sorry, but I encountered an error while seeking God's wisdom for you: {e}"

    # 5. Generate TTS audio
    main_answer = final_response_text.split("Relevant Scriptures")[0].strip()
    main_answer = main_answer.replace("**", "")

    audio_file = generate_tts_audio(main_answer)

    return {
        "response": final_response_text,
        "audio_path": audio_file,
        "verses_used": verse_list
    }

# --- CLI ---
def run_cli():
    """Command-line interface for the chatbot."""
    print("--- Yesu Mitra (Friend of Jesus) - Enhanced with Gemini 2.0 ---")
    print("Type 'quit' or 'exit' to end.")

    if not BIBLE_DATA:
        print("Cannot start: Bible data failed to load.")
        return

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            print("May God bless you and keep you. Goodbye!")
            break

        print("\nYesu Mitra is praying and reflecting...")

        global TTS_OUTPUT_PATH
        TTS_OUTPUT_PATH = "tts_output_cli.mp3"

        result = chat_with_yesu_mitra(user_input)

        print("\n--- Yesu Mitra's Response ---")
        print(result["response"])

        if result["audio_path"]:
            print(f"\n[Audio: {result['audio_path']}]")

if __name__ == "__main__":
    run_cli()
