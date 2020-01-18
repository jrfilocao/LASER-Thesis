#!/usr/bin/python3

import spacy
from spacy import displacy
import pt_core_news_sm
import de_core_news_sm
import en_core_web_sm
from fuzzywuzzy import fuzz, process

TOKEN_SORT_RATIO_THRESHOLD = 70

NLP_PT = pt_core_news_sm.load()
NLP_DE = de_core_news_sm.load()
NLP_EN = en_core_web_sm.load()

MODELS= {'de': NLP_DE,
         'en': NLP_EN,
         'pt': NLP_PT,
}


def _get_nlp_model(language):
    return MODELS[language]


def _get_named_entities(text, language):
    nlp_model = _get_nlp_model(language)
    named_entities = nlp_model(text).ents
    return named_entities


def _get_similar_named_entities(source_named_entities, target_named_entities):
    similar_named_entities = set()
    for source_named_entity in source_named_entities:
        for target_named_entity in target_named_entities:
            token_sort_ratio = fuzz.token_sort_ratio(source_named_entity.text, target_named_entity.text)

            if token_sort_ratio > TOKEN_SORT_RATIO_THRESHOLD:
                similar_named_entity_pair = SimilarNamedEntityPair(source_named_entity.text, target_named_entity.text, token_sort_ratio)
                similar_named_entities.add(similar_named_entity_pair)
    return similar_named_entities


def get_similar_entities_in_crosslingual_texts(source_text, source_language, target_text, target_language):
    source_named_entities = _get_named_entities(source_text, source_language)
    target_named_entities = _get_named_entities(target_text, target_language)

    return _get_similar_named_entities(source_named_entities, target_named_entities)


class SimilarNamedEntityPair:
    def __init__(self, source_text, target_text, ratio):
        self.source_text = source_text
        self.target_text = target_text
        self.ratio = ratio

    def __repr__(self):
        return self.source_text + ' ' + self.target_text + ' ' + str(self.ratio)

    def __str__(self):
        return self.source_text + ' ' + self.target_text + ' ' + str(self.ratio)

    def __hash__(self):
        return hash((self.source_text, self.target_text, self.ratio))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.source_text == other.source_text and self.target_text == other.target_text and self.ratio == other.ratio


if __name__ == "__main__":


    # doc_pt = nlp_pt('O atacante brasileiro deixou o clube espanhol para se juntar ao PSG com um contrato de 5 anos, em uma transferência recorde de 222 milhões de euros em 2017.. '
    #           '– Neymar pode deixar o PSG se houver uma oferta que atenda a todos. '
    #           'Mas, até o momento, não sabemos se alguém quer comprá-lo ou a que preço. '
    #           'Tudo isso não é feito em um dia, isso é certo – disse Leonardo ao jornal Le Parisien.. '
    #           '– Está claro para todos (que ele quer sair), mas, no futebol, você diz uma coisa hoje e outra amanhã… É incrível, mas é assim.')
    #
    # doc_de = nlp_de('Leonardo: Neymar kann PSG verlassen.  darf den französischen Meister Paris Saint-Germain bei einer entsprechenden Offerte verlassen. '
    #              'Das hat der zu PSG zurückgekehrte Sportdirektor Leonardo in einem Interview der Zeitung Le Parisien klargestellt. '
    #              'Sein derzeit noch verletzter brasilianischer Landsmann hatte am Montag unentschuldigt beim Trainingsauftakt des französischen Meisters gefehlt.. '
    #              'Neymar kann PSG verlassen, wenn es ein für alle Welt überzeugendes Angebot gibt. Aber bis zum heutigen Tag wissen wir weder, '
    #              'wer ihn kaufen möchte noch zu welchem Preis, sagte Leonardo. Ein Angebot für den 27-Jährigen habe man noch nicht erhalten, sagte Leonardo, '
    #              'bestätigte aber sehr oberflächliche Kontakte zu Neymars Ex-Club FC Barcelona. '
    #              'Von dort war der Angreifer vor zwei Jahren für die Rekordsumme von 222 Millionen Euro zu PSG gewechselt..  '
    #              'saß am Sonntag noch in Rio  beim Copa-América-Triumph der  Nationalmannschaft im Maracanã-Stadion auf der Tribüne. '
    #              'Weil  nicht zum Trainingsauftakt seines Vereins erschien, könnte er nun bestraft werden. '
    #              'Wir werden die zu treffenden Maßnahmen prüfen, wie wir das für alle Angestellten machen würden, sagte Leonardo.. '
    #              'Neymar fehlt unentschuldigt bei PSG-Training. fehlte am Montag ohne Entschuldigung beim Trainingsauftakt von . '
    #              'In einem offiziellen Statement schrieb der Klub um Trainer Thomas Tuchel: '
    #              'PSG stellt fest, dass Neymar Jr. nicht zur besprochenen Zeit am abgemachten Ort erschienen ist.')

    text_pt = (
        'O presidente americano, Donald Trump, voltou a criticar nesta segunda-feira (8) a gestão do Brexit pela primeira-ministra britânica, '
        'Theresa May, afirmando que ela é responsável pelo atual desastre e celebrando sua partida, '
        'em um contexto de tensão diplomática entre os dois países.. '
        'Sou muito crítico da forma como o Reino Unido e a primeira-ministra Theresa May geriram o Brexit, disse Trump.. '
        'O presidente americano afirmou ter dito a May como agir, mas que ela tinha decidido adotar outro caminho.. '
        'Que desastre ela e seus representantes criaram, afirmou Trump em um tuíte no qual anunciou que não terá mais contato com'
        ' o embaixador britânico em Washington após o vazamento de mensagens em que o diplomata classificava seu governo de torpe e inepto.. '
        'Eu não conheço o embaixador, mas ele não querido e nem bem-vindo nos Estados Unidos. '
        'Não teremos mais contatos com ele, afirmou Trump, dois dias após a publicação pela imprensa de comentários do '
        'embaixador britânico em Washington, Kim Darroch.. May classificou os vazamentos como totalmente inaceitáveis e afirmou ter total confiança em Darroch, '
        'que chegou a Washington em janeiro de 2016, antes da vitória de Trump nas eleições presidenciais..')


    text_de = ('Das Außenminister erklärte, die Ansichten von Botschaftern stimmten nicht unbedingt '
                    'mit denen von Ministern oder der Regierung überein. Aber wir bezahlen sie dafür, dass sie ehrlich sind, '
                    'genau wie der US-Botschafter hier seine Lesart der Politik und Persönlichkeiten von Westminster nach Hause schicken wird, '
                    'hieß es in einer Mitteilung des Ministeriums.. '
                    'Der umstrittene Brexit-Party-Politiker und Trump-Vertraute Nigel Farage forderte den Rücktritt des Botschafters. '
                    'Kim Darroch ist für den Job völlig ungeeignet und je früher er weg ist, desto besser, schrieb er auf Twitter.. '
                    'US-Präsident Donald Trump hat nach dem Bekanntwerden kritischer Memos des britischen Botschafters in Washington '
                    'seine Missachtung für den Diplomaten ausgedrückt. Wir werden uns nicht mehr mit ihm befassen, schrieb Trump am Montag auf Twitter. '
                    'Er kenne den Botschafter nicht, aber er sei nicht beliebt.. '
                    'Die britische Zeitung Mail on Sunday hatte aus geheimen Memos des Botschafters Kim Darroch zitiert.')

    similar_entities = get_similar_entities_in_crosslingual_texts(text_pt, 'pt', text_de,'de')
    print(similar_entities)