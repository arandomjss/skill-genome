import json
import os
from typing import List, Set

nlp = None
kw_model = None
spacy_available = False

try:
    import spacy
    spacy_available = True
except Exception:
    spacy_available = False

try:
    from keybert import KeyBERT
    keybert_available = True
except Exception:
    keybert_available = False

def _load_nlp():
    global nlp
    if nlp is None and spacy_available:
        try:
            nlp = spacy.load("en_core_web_sm")
        except Exception:
            nlp = None
    return nlp

def _load_keybert():
    global kw_model
    if kw_model is None and keybert_available:
        try:
            kw_model = KeyBERT()
        except Exception:
            kw_model = None
    return kw_model

def _load_ontology() -> List[str]:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ontology_path = os.path.join(current_dir, "ontology.json")
    with open(ontology_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("skills", [])

def extract_skills(normalized_text: str, raw_text: str) -> List[str]:
    skills_set: Set[str] = set()
    
    ontology_skills = _load_ontology()
    ontology_lower = [s.lower() for s in ontology_skills]
    
    for skill in ontology_lower:
        if skill in normalized_text:
            skills_set.add(skill)
        words = skill.split()
        if len(words) > 1:
            if all(word in normalized_text for word in words):
                skills_set.add(skill)
    
    nlp_model = _load_nlp()
    if nlp_model is not None:
        try:
            doc = nlp_model(raw_text)
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.lower().strip()
                if len(chunk_text) > 2 and len(chunk_text) < 50:
                    for skill in ontology_lower:
                        if skill in chunk_text or chunk_text in skill:
                            skills_set.add(skill)
        except Exception:
            pass
    
    kw_model = _load_keybert()
    if kw_model is not None:
        try:
            keywords = kw_model.extract_keywords(
                raw_text,
                keyphrase_ngram_range=(1, 2),
                stop_words='english',
                top_n=30
            )
            
            for keyword, _ in keywords:
                keyword_lower = keyword.lower().strip()
                for skill in ontology_lower:
                    if skill in keyword_lower or keyword_lower in skill:
                        skills_set.add(skill)
        except Exception:
            pass
    
    return list(skills_set)
