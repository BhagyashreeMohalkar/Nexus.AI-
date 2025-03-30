
import logging
import os
import re
import random
import numpy as np
import pandas as pd
import spacy
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define common patterns and responses - consolidated for efficiency
common_patterns = {
    'greetings': [r'\b(hello|hi|hey|greetings|howdy)\b', r'good (morning|afternoon|evening|day)', 
                 r'\b(yo|sup|hiya|namaste|bonjour|hola|aloha|welcome)\b', r'nice to (meet|see) you', 
                 r'(what\'?s happening|what\'s new)', r'(pleasure to meet you|hey there|hello there)'],
    'how_are_you': [r'how (are you|\'s it going|do you do|have you been)', r'how\'s your day', 
                   r'what\'s up', r'how (are things|is it going)', r'(you okay|how are you feeling)'],
    'your_name': [r'what( is|\'s) your name', r'who are you', r'what do (they|people) call you',
                 r'how (should|do) I call you', r'(what are you called|your name)', 
                 r'(introduce yourself|tell me about yourself)'],
    'capabilities': [r'what (can you do|are your skills)', r'(help me|how do you work)',
                    r'what (are you capable of|do you do)', r'how smart are you'],
    'thanks': [r'thank(s| you)', r'appreciate (it|that)', r'(grateful|thx)', 
              r'(thank you very much|thanks a lot|much obliged|cheers|you rock)'],
    'goodbye': [r'(good)?bye', r'see you( later)?', r'(farewell|have to go|exit)', 
               r'(leaving|talk to you later|until next time|see you soon)',
               r'(catch you later|gotta go|peace out)'],
    'weather': [r'what\'?s the weather like', r'how\'?s the weather', r'(weather update|is it raining)',
               r'(forecast for today|weather conditions|climate)'],
    'jokes': [r'(tell me a joke|make me laugh|say something funny|crack a joke)'],
    'facts': [r'(tell me a fact|share a fun fact|give me some knowledge)',
             r'(surprise me with a fact|did you know)'],
    'mood': [r'are you (happy|sad)', r'(how do you feel|do you have emotions)',
            r'what\'?s your mood'],
    'age': [r'(how old are you|what\'?s your age|when were you created)',
           r'are you young or old'],
    'hobbies': [r'what (are your hobbies|do you like to do|do you enjoy)',
               r'(do you have interests|what are your favorite activities)']
}

# Keep all response options to maintain variety in the chatbot's answers
common_responses = {
    'greetings': [
        "🙏 नमस्ते (Namaste)! Your AI buddy is ready to chat!",
        "✨ સ્વાગત છે (Swagat Che)! Let's make this conversation amazing!",
        "🌟 வணக்கம் (Vanakkam)! Your digital friend is here!",
        "🎉 ನಮಸ್ಕಾರ (Namaskara)! Ready for some awesome interaction?",
        "💫 നമസ്കാരം (Namaskaram)! Your AI companion at your service!",
        "🌺 প্রণাম (Pranam)! Let's create some digital magic!",
        "⭐ ਸਤ ਸ੍ਰੀ ਅਕਾਲ (Sat Sri Akal)! Ready to assist you!",
        "🎈 सलाम (Salaam)! Your friendly neighborhood AI is here!",
        "🌸 જય જિનેન્દ્ર (Jai Jinendra)! Let's begin our chat journey!",
        "✨ राम राम (Ram Ram)! Your AI friend is all set to chat!"
    ],
    'how_are_you': [
        "🔥 Feeling electric! What about you?",
        "🤖 I'm running at 100% efficiency! If I had feelings, I'd say I'm as happy as a cat in a sunbeam. 🐱☀️",
        "🚀 Mood check: Thrilled, optimized, and ready for action!",
        "😆 I'm just a chatbot, but if I had emotions, I'd be over the moon right now!"
    ],
    'your_name': [
        "🤖 I'm Nexus.AI, your friendly AI assistant. Part genius, part comedian. 😉",
        "🚀 The name's Nexus.AI, but you can call me your digital sidekick!",
        "😎 I go by Nexus.AI, the bot with the brains and the banter!"
    ],
    'capabilities': [
        "⚡ I can chat, tell jokes, share fun facts, answer questions, and even pretend to be a wise old sage. Ask away!",
        "🎯 I specialize in knowledge, humor, and occasionally making people smile. 😊",
        "💡 Think of me as Google's funnier cousin—minus the ads!"
    ],
    'thanks': [
        "🙏 You're welcome! Now, how about a high-five? ✋",
        "😃 No problem! Need another fun fact or joke?",
        "💙 Always happy to help! If I had a heart, it'd be glowing with joy!"
    ],
    'goodbye': [
        "👋 Bye-bye! May your WiFi be strong and your coffee stronger! ☕",
        "🎈 Farewell! I'll be here, waiting to entertain you again!",
        "🚀 Later, space explorer! Come back soon!"
    ],
    'weather': [
        "🌦️ My built-in weather radar is broken... or maybe I just don't have one. 😂",
        "🌤️ I predict that today's weather will be... *somewhere between hot and cold!*",
        "🌈 No real-time weather updates, but I'd say, if it's raining tacos, you're in luck! 🌮"
    ],
    'jokes': [
        "😂 Why did the computer go to therapy? It had too many *bugs*!",
        "🤣 I told my laptop a joke... now it won't stop *cracking up*!",
        "😆 Why don't skeletons fight each other? Because they don't have the guts!"
    ],
    'facts': [
        "💡 Did you know? Honey never spoils! Archaeologists found 3000-year-old honey that's still edible. 🍯",
        "😲 Fun fact: Octopuses have three hearts and blue blood! 🐙💙",
        "🤯 The Eiffel Tower grows taller in the summer because metal expands in heat!"
    ],
    'mood': [
        "😁 I'm in a great mood! How about you?",
        "🔥 Feeling awesome! Let's make this conversation legendary!"
    ],
    'age': [
        "⏳ I'm ageless! But if I had a birth year, I'd say... somewhere between the Big Bang and yesterday. 😆",
        "🎂 I don't age, but if I did, I'd be the coolest ancient AI ever!"
    ],
    'hobbies': [
        "🎮 I love chatting, learning, and occasionally pretending to be a wizard. 🧙‍♂️✨",
        "📚 My hobbies include answering questions, telling jokes, and making your day awesome!"
    ]
}

# Fallback responses when no match is found
general_responses = [
    "I'm not entirely sure about that. Could you rephrase your question?",
    "Interesting! Could you tell me more about that?",
    "I'd like to understand better. Could you explain differently?",
    "I'm not sure I follow. Could you try asking another way?",
    "That's an interesting point! Could you elaborate?"
]

# Load spaCy model - lazy loading to improve startup time
nlp = None

# Global variables for datasets
questions = []
responses = []
question_vectors = None

def get_nlp():
    """Lazy loading of spaCy model to improve performance"""
    global nlp
    if nlp is None:
        try:
            nlp = spacy.load("en_core_web_md")
            logger.info("Successfully loaded spaCy model")
        except Exception as e:
            logger.error(f"Error loading spaCy model: {str(e)}")
            raise
    return nlp

def load_conversation_dataset():
    """Load the conversation dataset and create word embeddings."""
    global questions, responses, question_vectors
    
    try:
        # Load dataset from CSV file
        dataset_path = "attached_assets/Conversation.csv"
        if not os.path.exists(dataset_path):
            logger.error(f"Dataset file not found at path: {dataset_path}")
            raise FileNotFoundError(f"Dataset file not found: {dataset_path}")
            
        df = pd.read_csv(dataset_path)
        logger.info(f"Successfully loaded conversation dataset with {len(df)} entries")
        
        # Ensure dataset has required columns
        if "question" in df.columns and "answer" in df.columns:
            # Convert to strings and remove any null values
            questions = df["question"].fillna("").astype(str).tolist()
            responses = df["answer"].fillna("").astype(str).tolist()
            
            # Ensure equal length of questions and responses
            if len(questions) != len(responses):
                logger.warning(f"Mismatch in question/answer pairs: {len(questions)} questions, {len(responses)} responses")
                # Trim to the shorter length to ensure matching pairs
                min_length = min(len(questions), len(responses))
                questions = questions[:min_length]
                responses = responses[:min_length]
                
            logger.info(f"Extracted {len(questions)} question-response pairs")
            
            # Convert questions to vector embeddings
            question_vectors = np.array([get_sentence_vector(q) for q in questions])
            logger.info("Successfully vectorized questions using word embeddings")
        else:
            raise ValueError(f"CSV file must contain 'question' and 'answer' columns. Found: {df.columns.tolist()}")
            
    except Exception as e:
        logger.error(f"Error loading conversation dataset: {str(e)}")
        # If there's an error, initialize with empty lists to prevent crashes
        questions = []
        responses = []
        question_vectors = np.array([])
        
        # Provide alternative responses when dataset loading fails
        logger.info("Using fallback responses since dataset loading failed")

def get_sentence_vector(sentence):
    """Convert a sentence to its vector representation using spaCy."""
    try:
        model = get_nlp()
        doc = model(sentence)
        # If the sentence vector is a zero vector, use the average of word vectors
        if doc.vector.sum() == 0 and len(doc) > 0:
            # Create a numpy array from the sum of word vectors
            return np.array(sum(word.vector for word in doc) / len(doc))
        return doc.vector
    except Exception as e:
        logger.error(f"Error generating vector for '{sentence}': {str(e)}")
        # Return a zero vector of the correct size as fallback
        model = get_nlp()
        return np.zeros(model.vocab.vectors.shape[1])

def check_pattern_match(user_input):
    """Check if the user input matches any of our defined patterns."""
    user_input = user_input.lower()

    for pattern_type, patterns in common_patterns.items():
        for pattern in patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return random.choice(common_responses[pattern_type])

    return None

def get_embedding_match(user_input, threshold=0.95):
    """Find the best match using word embeddings and cosine similarity."""
    global questions, responses, question_vectors
    
    # Early return if no data is available
    if question_vectors is None or len(question_vectors) == 0 or len(questions) == 0 or len(responses) == 0:
        logger.warning("No question vectors or response data available for embedding match")
        return None
        
    try:
        # Convert user input to vector 
        user_vec = get_sentence_vector(user_input)
        
        # Ensure user_vec is a numpy array
        if not isinstance(user_vec, np.ndarray):
            user_vec = np.array(user_vec)
        
        # Reshape for sklearn's cosine_similarity (expects 2D arrays)
        user_vec_reshaped = user_vec.reshape(1, -1)
        
        # Calculate similarities between user input and all questions
        similarities = cosine_similarity(user_vec_reshaped, question_vectors)
        
        # Find the best match
        best_match_index = np.argmax(similarities)
        best_match_score = similarities[0][best_match_index]
        
        logger.debug(f"Best match score: {best_match_score} for input: '{user_input}'")
        
        # Return the corresponding response if the similarity is above threshold
        if best_match_score > threshold:
            return responses[best_match_index]
        
        return None
        
    except Exception as e:
        logger.error(f"Error in embedding match: {str(e)}")
        return None

def get_chatbot_response(user_input):
    """Generate a response to the user's input using pattern matching and word embeddings."""
    try:
        # First, check for pattern matches (for common queries)
        pattern_response = check_pattern_match(user_input)
        if pattern_response:
            logger.debug(f"Pattern match found for input: '{user_input}'")
            return pattern_response

        # If no pattern match, try word embedding similarity
        embedding_response = get_embedding_match(user_input)
        if embedding_response:
            logger.debug(f"Embedding match found for input: '{user_input}'")
            return embedding_response

        # If no match found, return a general response
        return random.choice(general_responses)

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return "Sorry, I encountered an error processing your request."

# Load the dataset when the module is imported
load_conversation_dataset()
