import spacy
from spacy.matcher import PhraseMatcher
from rapidfuzz import process, fuzz
import string

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize phrase matcher
matcher = PhraseMatcher(nlp.vocab)

# Intent Mapping with Variations
response_map = {
    "hello": ["hello", "hi", "hey", "greetings"],  # Add "hello" and "hi" here
    "admission_process": [
        "admission", "apply", "how to join", "entry process", "enrollment", "admission details",
        "enroll", "how to enroll", "admission procedure", "application process", "how to get admission",
        "admission steps", "admission requirements", "how to apply for admission"
    ],
    "courses": [
        "available courses", "programs", "what courses", "diploma courses", "list of courses", "all courses",
        "what are the courses", "which courses are available", "what programs are offered", "tell me about the courses",
        "course list", "what can I study", "what are the programs", "what are the diploma courses"
    ],
    "facilities": [
        "amenities", "infrastructure", "what facilities", "hostel", "library", "sports complex", "campus facilities",
        "what are the facilities", "what amenities are available", "tell me about the facilities", "college infrastructure",
        "what does the college offer", "what are the campus facilities"
    ],
    "about_college": [
        "college info", "institute details", "tell me about the college", "overview", "about institute",
        "what is the college about", "information about the college", "describe the college"
    ],
    "examinations": [
        "exam", "test", "semester exams", "exam schedule", "marks", "exam details",
        "when are the exams", "exam timetable", "how are exams conducted"
    ],
    "contact": [
        "phone", "address", "email", "contact details", "how to reach", "contact info",
        "where is the college located", "how to contact the college", "college address"
    ],
    "course_duration": [
        "course duration", "how long courses", "length of diploma", "years of study", "diploma period",
        "how many years are the courses", "duration of programs", "how long are the diploma courses"
    ],
    "academic_calendar": [
        "year schedule", "term dates", "important dates", "university calendar", "college timetable",
        "when does the academic year start", "academic schedule", "college calendar"
    ],
    "eligibility_criteria": [
        "requirements", "who can apply", "qualification needed", "admission requirements", "eligibility conditions",
        "what are the eligibility criteria", "who is eligible", "what qualifications are needed"
    ],
    "required_documents": [
        "documents", "what papers needed", "admission papers", "certificates", "required documents",
        "what documents are required", "list of documents for admission", "what certificates are needed"
    ],
    "entrance_exam": [
        "exam needed", "entry test", "do I need an exam", "test required", "admission test",
        "is there an entrance exam", "what is the admission test", "entrance exam details"
    ],
    "principal": [
        "head of college", "college leader", "who is the principal", "head of institute", "principal details",
        "name of the principal", "who leads the college", "principal information"
    ],
    "placement": [
        "jobs", "recruitment", "career opportunities", "internships", "hiring", "campus placements",
        "what are the placement opportunities", "does the college provide placements", "placement details"
    ],
    "scope_after_diploma": [
        "career after diploma", "what after diploma", "higher studies", "job opportunities", "future scope",
        "what can I do after diploma", "options after diploma", "career options after diploma"
    ],
    "exit": ["exit", "bye", "goodbye", "see you", "quit"]  # Add "exit", "bye", and "goodbye" here
}

# Predefined Responses for Each Intent
responses_data = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi! Welcome to PVP Polytechnic Chatbot. How can I assist you?",
    "admission_process": "Our admission process is open! Visit our admissions page for details.",
    "courses": (
        "We offer diploma courses:\n1. Civil Engineering\n2. Mechanical Engineering\n3. Automobile Engineering\n"
        "4. Computer Science & Engineering\n5. Information Science & Engineering\n6. Electrical & Electronics Engineering\n"
        "7. Electronics & Communication Engineering\n8. Electronics Instrumentation & Control Engineering\n"
        "9. Apparel Design & Fabrication Technology"
    ),
    "facilities": "Our college offers a library, hostel, sports complex, and state-of-the-art labs.",
    "about_college": "PVP Polytechnic is a premier technical institute offering high-quality diploma education.",
    "examinations": "For exam timetables and rank lists, visit the 'Examinations' section on our website.",
    "contact": (
        "📍 Address: Dr. AIT Campus, Near Jnanabharathi, Mallathahalli, Bengaluru - 560 056, Karnataka, India.\n"
        "📞 Phone: 080-23211559\n📧 Email: info@pvppolytechnic.org"
    ),
    "course_duration": "Most diploma courses are of 3 years duration.",
    "academic_calendar": "The academic calendar is available in the 'Academics' section on our website.",
    "eligibility_criteria": (
        "✅ General Diploma: Passed 10th (SSC) with at least 35% marks in Science & Mathematics.\n"
        "✅ Direct Second-Year Entry: Passed HSC or ITI (relevant trade) for lateral entry into the second year."
    ),
    "required_documents": (
        "📌 10th Marksheet\n📌 School Leaving Certificate\n📌 Domicile Certificate (if applicable)\n"
        "📌 Caste Certificate (for reserved categories)\n📌 Aadhaar Card\n📌 Passport-size photos"
    ),
    "entrance_exam": "No, admission is merit-based for diploma courses. However, for some special categories, there might be an internal assessment or interview.",
    "principal": (
        "The Principal of PVP Polytechnic is Rajashekara M N.\n"
        "📧 Email: principal@pvppolytechnic.org\n📞 Phone: 080-23211559\n"
        "For more details, visit: [PVP Polytechnic](https://www.pvppolytechnic.org/)"
    ),
    "placement": "We have a dedicated placement cell that assists students with internships and job placements.",
    "scope_after_diploma": (
        "After a diploma, you can:\n\n"
        "**🎓 Higher Studies:** B.Tech (Lateral Entry), Certifications (CCNA, AWS, AI, CAD, etc.).\n"
        "**🏛️ Govt Jobs:** Railways (RRB JE), PSUs (BHEL, NTPC, ISRO), SSC JE, PWD, Police.\n"
        "**🏢 Private Jobs:** IT, Automobile, Manufacturing, Construction, and Electronics industries.\n"
        "**💼 Business/Freelancing:** Start workshops, IT consulting, CAD designing, or MSME businesses."
    ),
    "exit": "Goodbye! Have a great day. If you have more questions, feel free to ask anytime."  # Response for exit, bye, goodbye
}

# Create a dictionary of valid words/phrases for spell correction
valid_words = []
for variations in response_map.values():
    valid_words.extend(variations)

# Add patterns to the phrase matcher
for intent, variations in response_map.items():
    patterns = [nlp(variation) for variation in variations]
    matcher.add(intent, patterns)

# Normalize user input
def normalize_input(user_input):
    user_input = user_input.translate(str.maketrans("", "", string.punctuation))
    return user_input.lower()

# Correct spelling using RapidFuzz
def correct_spelling(user_input):
    corrected_input, score, _ = process.extractOne(user_input, valid_words, scorer=fuzz.token_set_ratio)
    if score > 70:  # Adjust threshold as needed
        return corrected_input
    return user_input  # Return original input if no good match is found

# Get intent using spaCy's phrase matcher
def get_intent(user_input):
    doc = nlp(user_input)
    matches = matcher(doc)
    if matches:
        match_id, start, end = matches[0]
        return nlp.vocab.strings[match_id]
    return None

# Get response based on intent or fuzzy matching
def get_response(user_input):
    user_input = normalize_input(user_input)
    corrected_input = correct_spelling(user_input)  # Correct spelling
    intent = get_intent(corrected_input)
    if intent:
        return responses_data[intent]
    else:
        best_match = process.extractOne(corrected_input, response_map.keys(), scorer=fuzz.token_set_ratio)
        if best_match[1] > 50:  # Lower threshold to 50
            return responses_data[best_match[0]]
        else:
            return "I'm sorry, I didn't understand that. Can you please rephrase?"