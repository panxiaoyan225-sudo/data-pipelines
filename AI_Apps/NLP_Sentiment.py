# The 'transformers' library from Hugging Face introduces a modern approach to Natural Language Processing (NLP)
# using Transformer models. Transformers are neural network architectures that excel at understanding context,
# relationships, and meaning in text. They're the backbone of state-of-the-art AI like BERT, GPT, and others.
# The library makes it easy to use these powerful models for various language tasks.

from transformers import pipeline

# The pipeline abstraction lets you quickly apply these advanced models to common AI tasks.
# Here, we use the sentiment-analysis pipeline, which uses a pre-trained model capable of reading text and
# inferring whether it expresses positive, negative, or neutral emotions.

classifier = pipeline("sentiment-analysis")

# A set of example user comments to analyze.
comments = [
    "I absolutely love this new update, it's so fast!",
    "This is the worst experience I've ever had with an app.",
    "It's okay, but the colors are a bit strange."
]

# The sentiment classifier predicts the emotional tone for each comment.
results = classifier(comments)

# Display each comment alongside the AI's sentiment verdict and its confidence.
for i, text in enumerate(comments):
    label = results[i]['label']
    score = results[i]['score']
    print(f"Comment: {text}")
    print(f"AI Verdict: {label} ({score:.2%} confidence)\n")