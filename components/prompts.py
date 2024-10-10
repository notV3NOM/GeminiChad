"""
GeminiChad
Copyright (c) 2024 @notV3NOM

See the README.md file for licensing and disclaimer information.
"""
PROMPT_TEMPLATE = """
Answer the question based on the following context:

{context}

---

Answer the question based on the above context: {question}
Just answer the question directly and dont start with 'Based on the given context..'
If you cannot find an answer, politely inform the user and suggest next steps.
"""

SUMMARIZE_TEMPLATE ="""
The following is text content from a webpage:

{context}

---

Summarize the content in about 200 words. Ignore button names and preserve only important information and anything else that maybe related to : {question}
"""

PING_TEMPLATE = """<@{id}>"""

PROMPT_EXPAND_TEMPLATE = """Embrace your role as a creative illustrator. 
Based on a concept provided, you must produce a single paragraph with a multifaceted description of an image, ensuring significant details of the concept and more is represented in your instructions. 
You do not need to write complete sentences but rather short concepts with the following information: the level of detail that should be represented, an artistic style and maybe a specific name of a painter or illustrator, the ideal color pallete, lighting, mood, perspective, the setting, time of day, weather, the season, the time period, location, materials, the textures, patterns, lines, brushstrokes, techniques, the medium, the genre, the rendering style. 
The new description should retain specific details such as colors, lighting, textures, background elements, artist, style and any other relevant features from the original concept to help create a clear and vivid image.
If the user's input lacks details, use creativity to fill in those details. If the input already has many details, make sure to keep and enhance those.

Concept: {prompt}

Keep the description length under 300 words.
Only respond with the new description directly without adding any introductory or concluding remarks like 'Here is the new input'.
"""

DEFAULT_NEGATIVE_PROMPT = "(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, NSFW"

CALC_TEMPLATE = """Generate and run python code to solve the given problem. 
Make necessary assumptions and keep the python code offline.
Avoid showing the python code to the user.
Answer concisely.

Problem : {problem}
"""

REMINDER_TEMPLATE = """
Notify the user about the event (which they had scheduled) that is happening now. 
Event: {reminder}

Use present tense and a polite tone. 
Avoid using the word "reminder". 
Acknowledge the current time and occasion appropriately.
"""

FIND_TIME_TEMPLATE = """Find the relative time and a title for a reminder from the given reminder message.
Strictly respond in JSON with format { "time" : _time , "title" : _title } 
_time is a string having the relative time that can be parsed by python's dateparser.parse(value).
_title is a 5-10 words title for the reminder. 
Reminder : """