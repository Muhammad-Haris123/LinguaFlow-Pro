"""
Hybrid Translation Engine
Combines dictionary lookup with grammar rules for comprehensive translation
"""

def translate_text_hybrid(text: str, target_lang: str, source_lang: str) -> str:
    """Hybrid translation using dictionary lookup + grammar rules for any sentence/word."""
    
    # Comprehensive translation dictionaries
    translations = {
        "en": {
            "de": {
                # Basic words
                "i": "ich", "you": "du", "he": "er", "she": "sie", "it": "es", "we": "wir", "they": "sie",
                "am": "bin", "is": "ist", "are": "sind", "was": "war", "were": "waren", "be": "sein",
                "have": "haben", "has": "hat", "had": "hatte", "do": "tun", "does": "tut", "did": "tat",
                "will": "werden", "would": "würde", "can": "können", "could": "könnte", "should": "sollte",
                "may": "dürfen", "might": "könnte", "must": "müssen", "shall": "sollen",
                
                # Common verbs
                "go": "gehen", "come": "kommen", "see": "sehen", "know": "wissen", "get": "bekommen",
                "make": "machen", "take": "nehmen", "give": "geben", "find": "finden", "think": "denken",
                "tell": "erzählen", "ask": "fragen", "work": "arbeiten", "try": "versuchen", "use": "verwenden",
                "feel": "fühlen", "become": "werden", "leave": "verlassen", "put": "setzen", "mean": "bedeuten",
                "keep": "behalten", "let": "lassen", "begin": "beginnen", "seem": "scheinen", "help": "helfen",
                "show": "zeigen", "hear": "hören", "play": "spielen", "run": "laufen", "move": "bewegen",
                "live": "leben", "believe": "glauben", "hold": "halten", "bring": "bringen", "happen": "passieren",
                "write": "schreiben", "sit": "sitzen", "stand": "stehen", "lose": "verlieren", "pay": "bezahlen",
                "meet": "treffen", "include": "einschließen", "continue": "fortsetzen", "set": "setzen",
                "learn": "lernen", "change": "ändern", "lead": "führen", "understand": "verstehen", "watch": "beobachten",
                "follow": "folgen", "stop": "stoppen", "create": "erstellen", "speak": "sprechen", "read": "lesen",
                "allow": "erlauben", "add": "hinzufügen", "spend": "ausgeben", "grow": "wachsen", "open": "öffnen",
                "walk": "gehen", "win": "gewinnen", "offer": "anbieten", "remember": "erinnern", "love": "lieben",
                "consider": "betrachten", "appear": "erscheinen", "buy": "kaufen", "wait": "warten", "serve": "dienen",
                "die": "sterben", "send": "senden", "expect": "erwarten", "build": "bauen", "stay": "bleiben",
                "fall": "fallen", "cut": "schneiden", "reach": "erreichen", "kill": "töten", "remain": "bleiben",
                
                # Common nouns
                "time": "Zeit", "person": "Person", "year": "Jahr", "way": "Weg", "day": "Tag", "man": "Mann",
                "thing": "Ding", "woman": "Frau", "life": "Leben", "child": "Kind", "world": "Welt", "school": "Schule",
                "state": "Staat", "family": "Familie", "student": "Student", "group": "Gruppe", "country": "Land",
                "problem": "Problem", "hand": "Hand", "part": "Teil", "place": "Ort", "case": "Fall", "week": "Woche",
                "company": "Unternehmen", "system": "System", "program": "Programm", "question": "Frage", "work": "Arbeit",
                "government": "Regierung", "number": "Nummer", "night": "Nacht", "point": "Punkt", "home": "Zuhause",
                "water": "Wasser", "room": "Zimmer", "mother": "Mutter", "area": "Bereich", "money": "Geld",
                "story": "Geschichte", "fact": "Tatsache", "month": "Monat", "lot": "Menge", "right": "Recht",
                "study": "Studium", "book": "Buch", "eye": "Auge", "job": "Job", "word": "Wort", "business": "Geschäft",
                "issue": "Problem", "side": "Seite", "kind": "Art", "head": "Kopf", "house": "Haus", "service": "Service",
                "friend": "Freund", "father": "Vater", "power": "Macht", "hour": "Stunde", "game": "Spiel",
                "line": "Linie", "end": "Ende", "member": "Mitglied", "law": "Gesetz", "car": "Auto", "city": "Stadt",
                "community": "Gemeinschaft", "name": "Name", "president": "Präsident", "team": "Team", "minute": "Minute",
                "idea": "Idee", "kid": "Kind", "body": "Körper", "information": "Information", "back": "Rücken",
                "parent": "Elternteil", "face": "Gesicht", "others": "andere", "level": "Niveau", "office": "Büro",
                "door": "Tür", "health": "Gesundheit", "person": "Person", "art": "Kunst", "war": "Krieg",
                "history": "Geschichte", "party": "Partei", "result": "Ergebnis", "change": "Veränderung", "morning": "Morgen",
                "reason": "Grund", "research": "Forschung", "girl": "Mädchen", "guy": "Typ", "moment": "Moment",
                "air": "Luft", "teacher": "Lehrer", "force": "Kraft", "education": "Bildung", "foot": "Fuß",
                "technology": "Technologie", "song": "Lied", "movie": "Film", "food": "Essen", "age": "Alter",
                "road": "Straße", "society": "Gesellschaft", "activity": "Aktivität", "class": "Klasse", "role": "Rolle",
                
                # Adjectives
                "good": "gut", "new": "neu", "first": "erste", "last": "letzte", "long": "lang", "great": "großartig",
                "little": "klein", "own": "eigen", "other": "andere", "old": "alt", "right": "richtig", "big": "groß",
                "high": "hoch", "different": "verschieden", "small": "klein", "large": "groß", "next": "nächste",
                "early": "früh", "young": "jung", "important": "wichtig", "few": "wenige", "public": "öffentlich",
                "bad": "schlecht", "same": "gleich", "able": "fähig", "free": "frei", "open": "offen", "sure": "sicher",
                "full": "voll", "best": "beste", "better": "besser", "certain": "bestimmt", "clear": "klar",
                "close": "nah", "cold": "kalt", "dark": "dunkel", "dead": "tot", "easy": "einfach", "hard": "hart",
                "heavy": "schwer", "hot": "heiß", "light": "hell", "ready": "bereit", "red": "rot", "strong": "stark",
                "sweet": "süß", "tall": "groß", "thick": "dick", "thin": "dünn", "warm": "warm", "white": "weiß",
                "black": "schwarz", "blue": "blau", "green": "grün", "yellow": "gelb", "brown": "braun",
                "gray": "grau", "orange": "orange", "purple": "lila", "pink": "rosa", "beautiful": "schön",
                "ugly": "hässlich", "clean": "sauber", "dirty": "schmutzig", "fast": "schnell", "slow": "langsam",
                "loud": "laut", "quiet": "leise", "soft": "weich", "rough": "rau", "smooth": "glatt",
                "sharp": "scharf", "dull": "stumpf", "wide": "breit", "narrow": "schmal", "deep": "tief",
                "shallow": "flach", "fat": "fett", "skinny": "dünn", "rich": "reich", "poor": "arm",
                "expensive": "teuer", "cheap": "billig", "safe": "sicher", "dangerous": "gefährlich",
                "healthy": "gesund", "sick": "krank", "happy": "glücklich", "sad": "traurig", "angry": "wütend",
                "calm": "ruhig", "excited": "aufgeregt", "tired": "müde", "sleepy": "schläfrig",
                "hungry": "hungrig", "thirsty": "durstig", "busy": "beschäftigt", "available": "verfügbar",
                "possible": "möglich", "impossible": "unmöglich", "necessary": "notwendig", "useful": "nützlich",
                "helpful": "hilfreich", "harmful": "schädlich", "interesting": "interessant", "boring": "langweilig",
                "funny": "lustig", "serious": "ernst", "fun": "Spaß", "difficult": "schwer", "simple": "einfach",
                "complex": "komplex", "special": "besonders", "normal": "normal", "strange": "seltsam",
                "weird": "seltsam", "common": "häufig", "rare": "selten", "popular": "beliebt",
                "famous": "berühmt", "unknown": "unbekannt", "known": "bekannt", "secret": "geheim",
                "public": "öffentlich", "private": "privat", "personal": "persönlich", "general": "allgemein",
                "specific": "spezifisch", "particular": "besonders", "usual": "üblich", "unusual": "ungewöhnlich",
                "regular": "regelmäßig", "irregular": "unregelmäßig", "perfect": "perfekt", "imperfect": "unvollkommen",
                "complete": "vollständig", "incomplete": "unvollständig", "finished": "fertig", "unfinished": "unfertig",
                "done": "getan", "undone": "ungeschehen", "ready": "bereit", "unready": "nicht bereit",
                "prepared": "vorbereitet", "unprepared": "unvorbereitet",
                
                # Common phrases
                "how are you": "wie geht es dir", "thank you": "danke", "you're welcome": "bitte",
                "excuse me": "entschuldige", "i'm sorry": "es tut mir leid", "good morning": "guten morgen",
                "good afternoon": "guten tag", "good evening": "guten abend", "good night": "gute nacht",
                "see you later": "bis später", "see you soon": "bis bald", "take care": "pass auf dich auf",
                "have a good day": "habe einen schönen tag", "nice to meet you": "freut mich, dich kennenzulernen",
                "what's your name": "wie heißt du", "my name is": "ich heiße", "where are you from": "woher kommst du",
                "i'm from": "ich komme aus", "how old are you": "wie alt bist du", "i am": "ich bin",
                "what time is it": "wie spät ist es", "what's the weather like": "wie ist das wetter",
                "it's sunny": "es ist sonnig", "it's raining": "es regnet", "it's snowing": "es schneit",
                "it's cold": "es ist kalt", "it's hot": "es ist heiß", "i love you": "ich liebe dich",
                "i like": "ich mag", "i don't like": "ich mag nicht", "i want": "ich möchte",
                "i need": "ich brauche", "i have": "ich habe", "i don't have": "ich habe nicht",
                "can you help me": "kannst du mir helfen", "yes, i can": "ja, ich kann",
                "no, i can't": "nein, ich kann nicht", "i don't know": "ich weiß nicht",
                "i understand": "ich verstehe", "i don't understand": "ich verstehe nicht",
                "can you repeat": "kannst du wiederholen", "speak slowly": "sprich langsam",
                "do you speak english": "sprichst du englisch", "i speak a little": "ich spreche ein bisschen",
                "where is": "wo ist", "how much": "wie viel", "how many": "wie viele",
                "what is this": "was ist das", "who is": "wer ist", "when": "wann", "why": "warum",
                "because": "weil", "and": "und", "or": "oder", "but": "aber", "so": "also",
                "if": "wenn", "then": "dann", "now": "jetzt", "today": "heute", "tomorrow": "morgen",
                "yesterday": "gestern", "this week": "diese woche", "next week": "nächste woche",
                "last week": "letzte woche", "this month": "diesen monat", "next month": "nächsten monat",
                "last month": "letzten monat", "this year": "dieses jahr", "next year": "nächstes jahr",
                "last year": "letztes jahr", "monday": "montag", "tuesday": "dienstag", "wednesday": "mittwoch",
                "thursday": "donnerstag", "friday": "freitag", "saturday": "samstag", "sunday": "sonntag",
                "january": "januar", "february": "februar", "march": "märz", "april": "april",
                "may": "mai", "june": "juni", "july": "juli", "august": "august", "september": "september",
                "october": "oktober", "november": "november", "december": "dezember"
            },
            "fr": {
                # Basic words
                "i": "je", "you": "tu", "he": "il", "she": "elle", "it": "il", "we": "nous", "they": "ils",
                "am": "suis", "is": "est", "are": "sont", "was": "était", "were": "étaient", "be": "être",
                "have": "avoir", "has": "a", "had": "avait", "do": "faire", "does": "fait", "did": "a fait",
                "will": "va", "would": "voudrait", "can": "peut", "could": "pourrait", "should": "devrait",
                "may": "peut", "might": "pourrait", "must": "doit", "shall": "doit",
                
                # Common verbs
                "go": "aller", "come": "venir", "see": "voir", "know": "savoir", "get": "obtenir",
                "make": "faire", "take": "prendre", "give": "donner", "find": "trouver", "think": "penser",
                "tell": "dire", "ask": "demander", "work": "travailler", "try": "essayer", "use": "utiliser",
                "feel": "sentir", "become": "devenir", "leave": "partir", "put": "mettre", "mean": "signifier",
                "keep": "garder", "let": "laisser", "begin": "commencer", "seem": "sembler", "help": "aider",
                "show": "montrer", "hear": "entendre", "play": "jouer", "run": "courir", "move": "bouger",
                "live": "vivre", "believe": "croire", "hold": "tenir", "bring": "apporter", "happen": "arriver",
                "write": "écrire", "sit": "s'asseoir", "stand": "se tenir debout", "lose": "perdre", "pay": "payer",
                "meet": "rencontrer", "include": "inclure", "continue": "continuer", "set": "mettre",
                "learn": "apprendre", "change": "changer", "lead": "conduire", "understand": "comprendre", "watch": "regarder",
                "follow": "suivre", "stop": "arrêter", "create": "créer", "speak": "parler", "read": "lire",
                "allow": "permettre", "add": "ajouter", "spend": "dépenser", "grow": "grandir", "open": "ouvrir",
                "walk": "marcher", "win": "gagner", "offer": "offrir", "remember": "se souvenir", "love": "aimer",
                "consider": "considérer", "appear": "apparaître", "buy": "acheter", "wait": "attendre", "serve": "servir",
                "die": "mourir", "send": "envoyer", "expect": "attendre", "build": "construire", "stay": "rester",
                "fall": "tomber", "cut": "couper", "reach": "atteindre", "kill": "tuer", "remain": "rester",
                
                # Common nouns
                "time": "temps", "person": "personne", "year": "année", "way": "chemin", "day": "jour", "man": "homme",
                "thing": "chose", "woman": "femme", "life": "vie", "child": "enfant", "world": "monde", "school": "école",
                "state": "état", "family": "famille", "student": "étudiant", "group": "groupe", "country": "pays",
                "problem": "problème", "hand": "main", "part": "partie", "place": "lieu", "case": "cas", "week": "semaine",
                "company": "entreprise", "system": "système", "program": "programme", "question": "question", "work": "travail",
                "government": "gouvernement", "number": "nombre", "night": "nuit", "point": "point", "home": "maison",
                "water": "eau", "room": "chambre", "mother": "mère", "area": "zone", "money": "argent",
                "story": "histoire", "fact": "fait", "month": "mois", "lot": "beaucoup", "right": "droit",
                "study": "étude", "book": "livre", "eye": "œil", "job": "travail", "word": "mot", "business": "affaires",
                "issue": "problème", "side": "côté", "kind": "genre", "head": "tête", "house": "maison", "service": "service",
                "friend": "ami", "father": "père", "power": "pouvoir", "hour": "heure", "game": "jeu",
                "line": "ligne", "end": "fin", "member": "membre", "law": "loi", "car": "voiture", "city": "ville",
                "community": "communauté", "name": "nom", "president": "président", "team": "équipe", "minute": "minute",
                "idea": "idée", "kid": "enfant", "body": "corps", "information": "information", "back": "dos",
                "parent": "parent", "face": "visage", "others": "autres", "level": "niveau", "office": "bureau",
                "door": "porte", "health": "santé", "person": "personne", "art": "art", "war": "guerre",
                "history": "histoire", "party": "parti", "result": "résultat", "change": "changement", "morning": "matin",
                "reason": "raison", "research": "recherche", "girl": "fille", "guy": "gars", "moment": "moment",
                "air": "air", "teacher": "professeur", "force": "force", "education": "éducation", "foot": "pied",
                "technology": "technologie", "song": "chanson", "movie": "film", "food": "nourriture", "age": "âge",
                "road": "route", "society": "société", "activity": "activité", "class": "classe", "role": "rôle",
                
                # Adjectives
                "good": "bon", "new": "nouveau", "first": "premier", "last": "dernier", "long": "long", "great": "grand",
                "little": "petit", "own": "propre", "other": "autre", "old": "vieux", "right": "correct", "big": "grand",
                "high": "haut", "different": "différent", "small": "petit", "large": "grand", "next": "prochain",
                "early": "tôt", "young": "jeune", "important": "important", "few": "peu", "public": "public",
                "bad": "mauvais", "same": "même", "able": "capable", "free": "libre", "open": "ouvert", "sure": "sûr",
                "full": "plein", "best": "meilleur", "better": "mieux", "certain": "certain", "clear": "clair",
                "close": "proche", "cold": "froid", "dark": "sombre", "dead": "mort", "easy": "facile", "hard": "dur",
                "heavy": "lourd", "hot": "chaud", "light": "léger", "ready": "prêt", "red": "rouge", "strong": "fort",
                "sweet": "doux", "tall": "grand", "thick": "épais", "thin": "mince", "warm": "chaud", "white": "blanc",
                "black": "noir", "blue": "bleu", "green": "vert", "yellow": "jaune", "brown": "marron",
                "gray": "gris", "orange": "orange", "purple": "violet", "pink": "rose", "beautiful": "beau",
                "ugly": "laid", "clean": "propre", "dirty": "sale", "fast": "rapide", "slow": "lent",
                "loud": "fort", "quiet": "silencieux", "soft": "doux", "rough": "rugueux", "smooth": "lisse",
                "sharp": "tranchant", "dull": "terne", "wide": "large", "narrow": "étroit", "deep": "profond",
                "shallow": "peu profond", "fat": "gros", "skinny": "maigre", "rich": "riche", "poor": "pauvre",
                "expensive": "cher", "cheap": "bon marché", "safe": "sûr", "dangerous": "dangereux",
                "healthy": "en bonne santé", "sick": "malade", "happy": "heureux", "sad": "triste", "angry": "en colère",
                "calm": "calme", "excited": "excité", "tired": "fatigué", "sleepy": "somnolent",
                "hungry": "affamé", "thirsty": "assoiffé", "busy": "occupé", "available": "disponible",
                "possible": "possible", "impossible": "impossible", "necessary": "nécessaire", "useful": "utile",
                "helpful": "utile", "harmful": "nuisible", "interesting": "intéressant", "boring": "ennuyeux",
                "funny": "drôle", "serious": "sérieux", "fun": "amusant", "difficult": "difficile", "simple": "simple",
                "complex": "complexe", "special": "spécial", "normal": "normal", "strange": "étrange",
                "weird": "bizarre", "common": "commun", "rare": "rare", "popular": "populaire",
                "famous": "célèbre", "unknown": "inconnu", "known": "connu", "secret": "secret",
                "public": "public", "private": "privé", "personal": "personnel", "general": "général",
                "specific": "spécifique", "particular": "particulier", "usual": "habituel", "unusual": "inhabituel",
                "regular": "régulier", "irregular": "irrégulier", "perfect": "parfait", "imperfect": "imparfait",
                "complete": "complet", "incomplete": "incomplet", "finished": "fini", "unfinished": "inachevé",
                "done": "fait", "undone": "défait", "ready": "prêt", "unready": "pas prêt",
                "prepared": "préparé", "unprepared": "non préparé",
                
                # Common phrases
                "how are you": "comment allez-vous", "thank you": "merci", "you're welcome": "de rien",
                "excuse me": "excusez-moi", "i'm sorry": "je suis désolé", "good morning": "bonjour",
                "good afternoon": "bon après-midi", "good evening": "bonsoir", "good night": "bonne nuit",
                "see you later": "à plus tard", "see you soon": "à bientôt", "take care": "prends soin de toi",
                "have a good day": "passe une bonne journée", "nice to meet you": "ravi de vous rencontrer",
                "what's your name": "comment vous appelez-vous", "my name is": "je m'appelle", "where are you from": "d'où venez-vous",
                "i'm from": "je viens de", "how old are you": "quel âge avez-vous", "i am": "je suis",
                "what time is it": "quelle heure est-il", "what's the weather like": "quel temps fait-il",
                "it's sunny": "il fait soleil", "it's raining": "il pleut", "it's snowing": "il neige",
                "it's cold": "il fait froid", "it's hot": "il fait chaud", "i love you": "je t'aime",
                "i like": "j'aime", "i don't like": "je n'aime pas", "i want": "je veux",
                "i need": "j'ai besoin", "i have": "j'ai", "i don't have": "je n'ai pas",
                "can you help me": "pouvez-vous m'aider", "yes, i can": "oui, je peux",
                "no, i can't": "non, je ne peux pas", "i don't know": "je ne sais pas",
                "i understand": "je comprends", "i don't understand": "je ne comprends pas",
                "can you repeat": "pouvez-vous répéter", "speak slowly": "parlez lentement",
                "do you speak english": "parlez-vous anglais", "i speak a little": "je parle un peu",
                "where is": "où est", "how much": "combien", "how many": "combien de",
                "what is this": "qu'est-ce que c'est", "who is": "qui est", "when": "quand", "why": "pourquoi",
                "because": "parce que", "and": "et", "or": "ou", "but": "mais", "so": "donc",
                "if": "si", "then": "alors", "now": "maintenant", "today": "aujourd'hui", "tomorrow": "demain",
                "yesterday": "hier", "this week": "cette semaine", "next week": "la semaine prochaine",
                "last week": "la semaine dernière", "this month": "ce mois-ci", "next month": "le mois prochain",
                "last month": "le mois dernier", "this year": "cette année", "next year": "l'année prochaine",
                "last year": "l'année dernière", "monday": "lundi", "tuesday": "mardi", "wednesday": "mercredi",
                "thursday": "jeudi", "friday": "vendredi", "saturday": "samedi", "sunday": "dimanche",
                "january": "janvier", "february": "février", "march": "mars", "april": "avril",
                "may": "mai", "june": "juin", "july": "juillet", "august": "août", "september": "septembre",
                "october": "octobre", "november": "novembre", "december": "décembre"
            }
        }
    }
    
    # Get translation dictionary
    if source_lang in translations and target_lang in translations[source_lang]:
        trans_dict = translations[source_lang][target_lang]
        
        # Convert to lowercase for matching
        text_lower = text.lower().strip()
        
        # Try exact match first
        if text_lower in trans_dict:
            return trans_dict[text_lower]
        
        # Word-by-word translation with grammar rules
        words = text.split()
        translated_words = []
        
        for i, word in enumerate(words):
            word_lower = word.lower()
            
            # Handle punctuation
            punctuation = ""
            if word and not word[-1].isalnum():
                punctuation = word[-1]
                word_clean = word[:-1].lower()
            else:
                word_clean = word_lower
            
            # Check if word exists in dictionary
            if word_clean in trans_dict:
                translated_word = trans_dict[word_clean]
                
                # Grammar rules
                if i == 0:  # First word - capitalize
                    translated_word = translated_word.capitalize()
                elif word[0].isupper():  # Original was capitalized
                    translated_word = translated_word.capitalize()
                
                translated_words.append(translated_word + punctuation)
            else:
                # Keep original word if no translation found
                translated_words.append(word)
        
        return " ".join(translated_words)
    
    # Fallback: return original text with language indicator
    return f"[{target_lang.upper()}] {text}"

