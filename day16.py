import re

# List of abusive words (extend as needed)
abusive_words = ['abuse1', 'abuse2', 'curseword', 'badword']

# Lambda function to check if the comment contains abusive words
is_abusive = lambda comment: any(re.search(r'\b' + re.escape(word) + r'\b', comment.lower()) for word in abusive_words)

# Lambda function to mask abusive words (optional if you want to replace abusive words with ****)
mask_abusive = lambda comment: re.sub(r'\b(' + '|'.join(map(re.escape, abusive_words)) + r')\b', '****', comment, flags=re.IGNORECASE)

# Real-time comment processing function
def process_comment(comment):
    if is_abusive(comment):
        print("This comment is blocked due to abusive content.")
        return False  # Indicate the comment is blocked
    else:
        print("Comment allowed:", comment)
        return True  # Indicate the comment is allowed

# YouTube-style comment filter with optional masking
def youtube_comment_filter(comment, mask=False):
    if mask:  # Mask abusive words instead of blocking the whole comment
        filtered_comment = mask_abusive(comment)
        print("Filtered comment:", filtered_comment)
        return filtered_comment
    else:
        process_comment(comment)

# Simulate some comments being posted
comments = [
    "This is an amazing video!",
    "You are such a curseword!",
    "Thanks for sharing!",
    "I think abuse1 should not be allowed here."
]

# Run through each comment
for comment in comments:
    youtube_comment_filter(comment, mask=True)  # Use mask=True to mask abusive words
