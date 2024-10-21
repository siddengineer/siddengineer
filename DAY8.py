import language_tool_python
import difflib

def correct_grammar(text):
    # Initialize the language tool for English
    tool = language_tool_python.LanguageTool('en-US')
    
    # Get grammar corrections
    matches = tool.check(text)
    
    # Apply the corrections
    corrected_text = language_tool_python.utils.correct(text, matches)
    
    return corrected_text

def highlight_changes(original_text, corrected_text):
    # Create a unified diff
    diff = difflib.ndiff(original_text.splitlines(), corrected_text.splitlines())
    
    # Format the differences for clearer visibility
    changes = []
    for line in diff:
        if line.startswith('- ') or line.startswith('+ '):
            changes.append(line)
    
    return '\n'.join(changes)

# Main function to take user input and correct it
if __name__ == "__main__":
    try:
        # Input paragraph from user
        paragraph = input("Enter the paragraph you want to correct: ")

        # Correct the grammar
        corrected_text = correct_grammar(paragraph)

        # Highlight changes
        changes = highlight_changes(paragraph, corrected_text)

        # Display the original and corrected text
        print("\nOriginal Text:")
        print(paragraph)
        print("\nCorrected Text:")
        print(corrected_text)
        
        # Display changes
        print("\nChanges:")
        print(changes)
        
    except Exception as e:
        print(f"An error occurred: {e}")
