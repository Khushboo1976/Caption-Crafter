from transformers import pipeline
import random
import emoji
# Load the model only once
generator = pipeline('text-generation', model='distilgpt2')

def generate_caption(prompt: str, max_length=50):
    result = generator(prompt, max_length=max_length, num_return_sequences=1)
    caption = result[0]['generated_text'].strip()

    # Add random emojis
    emojis = random.sample(["😊", "✨", "🌟", "🔥", "💬", "💡", "📢", "📸", "🎯", "🌍"], 3)
    caption += " " + " ".join(emojis)

    # Add hashtags
    tags = prompt.lower().split()
    hashtags = [f"#{tag.capitalize()}" for tag in tags if len(tag) > 3][:5]
    caption += "\n" + " ".join(hashtags)
    return caption
