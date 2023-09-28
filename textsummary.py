import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest
from string import punctuation
import speech_recognition as sr




text = '''The fable is made the subject of a poem by the first century CE Greek Poet Bianor,[1] was included in the 2nd century fable collection of pseudo-Dositheus[2] and later appears in the 4th–5th-century Latin verse collection by Avianus.[3] The history of this fable in antiquity and the Middle Ages is tracked in A. E. Wright's Hie lert uns der meister: Latin Commentary and the Germany Fable.[4]

The story concerns a thirsty crow that comes upon a pitcher with water at the bottom, beyond the reach of its beak. After failing to push it over, the bird drops in pebbles one by one until the water rises to the top of the pitcher, allowing it to drink. In his telling, Avianus follows it with a moral that emphasizes the virtue of ingenuity: "This fable shows us that thoughtfulness is superior to brute strength." Other tellers of the story stress the crow's persistence. In Francis Barlow's edition, the proverb 'Necessity is the mother of invention' is applied to the story[5] while an early 20th-century retelling quotes the proverb 'Where there's a will, there's a way'.[6]

Artistic use of the fable may go back to Roman times, since one of the mosaics that has survived is thought to have the story of the crow and the pitcher as its subject.[7] Modern equivalents have included English tiles from the 18th[8] and 19th centuries an American mural by Justin C. Gruelle, created for a Connecticut school These and the illustrations in books of fables had little scope for invention.'''

def audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)  # You can choose other APIs for recognition as well
    return text
def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)

    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    sent_tokens = [sent for sent in doc.sents]

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    select_len = int(len(sent_tokens) * 0.3)
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    
    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))






   
