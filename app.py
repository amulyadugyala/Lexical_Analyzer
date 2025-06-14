import streamlit as st
import nltk

# 🔧 Safe download of NLTK resources
@st.cache_data
def setup_nltk():
    resources = {
        'punkt': 'tokenizers/punkt',
        'wordnet': 'corpora/wordnet',
        'omw-1.4': 'corpora/omw-1.4',
        'averaged_perceptron_tagger': 'taggers/averaged_perceptron_tagger'
    }
    for key, path in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(key)

setup_nltk()

# ----- Set page config -----
st.set_page_config(
    page_title="English lexical Analyzer",
    page_icon="📘",
    layout="centered",
)

# ----- Sidebar -----
st.sidebar.title("📘 About This App")
st.sidebar.info(
    """
    This English lexical Analyzer uses NLTK and local Python libraries to:
    - Define words
    - Find synonyms and antonyms
    - Count syllables
    - Provide example usage
    - Tag part of speech in context
    """
)

st.sidebar.markdown("---")
st.sidebar.write("👤 Developed by [AmulyaDugyala]")

# ----- Custom Header -----
st.markdown("""
    <h1 style='text-align: center; color: #2E86AB;'>
        🧠 English lexical Analyzer
    </h1>
    <p style='text-align: center; font-size: 18px; color: gray;'>
        Understand the meaning, usage, and structure of English words - all offline!
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# ----- Input Area -----
word = st.text_input("🔍 Enter a word to analyze:", "").strip()

if word:
    st.markdown(f"### Results for: `{word}`")

    synsets = wordnet.synsets(word)

    if synsets:
        # Definitions
        st.markdown("#### 📖 Definitions")
        for i, syn in enumerate(synsets[:3]):
            st.markdown(f"**{i+1}. ({syn.pos()})** {syn.definition()}")

        # Synonyms & Antonyms (side by side)
        synonyms = {lemma.name() for s in synsets for lemma in s.lemmas()}
        antonyms = {ant.name() for s in synsets for lemma in s.lemmas() for ant in lemma.antonyms()}

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🟢 Synonyms")
            st.write(", ".join(list(synonyms)[:10]) or "None")
        with col2:
            st.markdown("#### 🔴 Antonyms")
            st.write(", ".join(list(antonyms)[:10]) or "None")

        # Example sentences
        examples = []
        for syn in synsets:
            examples.extend(syn.examples())
        st.markdown("#### ✍️ Example Sentences")
        if examples:
            for i, ex in enumerate(examples[:3]):
                st.markdown(f"> {ex}")
        else:
            st.info("No example sentences found.")

    else:
        st.error("❌ Word not found in WordNet.")

    # Syllable Count
    st.markdown("#### 🔢 Syllable Count")
    syllables = textstat.syllable_count(word)
    st.success(f"Estimated syllables: **{syllables}**")

    # POS Tag in a sentence
    st.markdown("#### 🧠 Part of Speech (POS) Tagging")
    example_sentence = f"I think the word {word} is interesting to learn."
    tagged = pos_tag(example_sentence.split())
    word_tags = [f"**{w}** → `{t}`" for w, t in tagged if w.lower() == word.lower()]
    st.write("Context sentence:", example_sentence)
    st.write("Tagged as:", ", ".join(word_tags) or "Not tagged.")
else:
    st.info("👈 Enter a word above to see the analysis.")
