
def _get_article_sentences_as_text(sentences):
    return "\n ".join(sentence_tuple[0] for sentence_tuple in sentences)


def write_sentences_md_file(file_name, source_sentences, target_sentences, source_id, target_id):
    source_sentence_count = len(source_sentences)
    target_sentence_count = len(target_sentences)
    max_sentence_count = source_sentence_count if source_sentence_count >= target_sentence_count else target_sentence_count
    with open(file_name, 'a') as md_file:
        md_file.write('### ' + source_id[53:] + ' -- ' + target_id[53:] + '\n')
        md_file.write('| EN | DE | \n')
        md_file.write('| ------------- |: -------------: | \n')
        for index in range(max_sentence_count):
            source_sentence = '--' if index >= source_sentence_count else source_sentences[index][0]
            target_sentence = '--' if index >= target_sentence_count else target_sentences[index][0]
            md_file.write('| ' + source_sentence + ' | ' + target_sentence + ' |\n')
