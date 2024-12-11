from flask import Flask, request, render_template_string

app = Flask(__name__)

# AI Tools Database
ai_tools = {
    "writing": {
        "content creation": ["CopyAI", "Rytr", "Grammarly"],
        "editing": ["QuillBot", "Grammarly"],
        "note-taking": ["Notefolio", "Monica"]
    },
    "video": {
        "video editing": ["VEED.IO", "InVideo", "Descript"],
        "text-to-video": ["Fliki", "HeyGen", "Synthesys"]
    },
    "chatbot": {
        "customer support": ["ChatGPT", "Dialogflow", "ChatSonic"],
        "ai research assistant": ["Claude", "Perplexity", "Google Bard"]
    },
    "design": {
        "image generation": ["DALL-E 2", "Midjourney", "Leonardo"],
        "logo design": ["MakeLogo", "LogoAI", "Looka"]
    }
}

# HTML Template with Embedded CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Tool Suggestion</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 60%;
            margin: 50px auto;
            padding: 20px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        input[type="text"] {
            width: 80%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            background-color: #007BFF;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #e9ffe8;
            border: 1px solid #a5d6a7;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Tool Suggestion System</h1>
        <form method="POST">
            <input type="text" name="query" placeholder="Enter your need (e.g., content creation, logo design)" required>
            <button type="submit">Suggest AI Tools</button>
        </form>
        {% if category %}
        <div class="result">
            <h3>Best Tools for {{ subcategory.capitalize() }} ({{ category.capitalize() }})</h3>
            <ul>
                {% for tool in tools %}
                <li>{{ tool }}</li>
                {% endfor %}
            </ul>
        </div>
        {% elif query %}
        <div class="result">
            <p>Sorry, no tools found for your query: <strong>{{ query }}</strong></p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Flask Route
@app.route("/", methods=["GET", "POST"])
def index():
    category, subcategory, tools, query = None, None, [], None
    if request.method == "POST":
        query = request.form["query"].lower()
        for cat, subcats in ai_tools.items():
            if cat in query:  # Match category
                for subcat, tools_list in subcats.items():
                    if subcat in query:  # Match subcategory
                        category, subcategory, tools = cat, subcat, tools_list
                        break
                break
    return render_template_string(
        HTML_TEMPLATE,
        category=category,
        subcategory=subcategory,
        tools=tools,
        query=query
    )

if __name__ == "__main__":
    app.run(debug=True)