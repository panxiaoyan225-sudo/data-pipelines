from transformers import pipeline

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

sequence_to_classify = "This house comes with 2 bedrooms,a pool."
#sequence_to_classify = "The new electric car has a range of over 400 miles on a single charge."
candidate_labels = ["politics", "technology", "environment", "investemnt","sports"]

# Run the classifier
result = classifier(sequence_to_classify, candidate_labels)

print(result)

print(f"Text: {sequence_to_classify}")
for label, score in zip(result['labels'], result['scores']):
    print(f"{label}: {round(score * 100, 2)}%")