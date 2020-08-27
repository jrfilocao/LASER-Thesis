select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'de'
and named_entities_score is not null
and number_of_similar_sentences > 5
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id

/app/LASER-Thesis/tasks/news_uni_leipzig/input_files/2019-07-10_en_article_635   | /app/LASER-Thesis/tasks/news_uni_leipzig/input_files/2019-07-09_de_article_1127
/app/LASER-Thesis/tasks/news_uni_leipzig/input_files/2019-07-10_en_article_635   | /app/LASER-Thesis/tasks/news_uni_leipzig/input_files/2019-07-09_de_article_1351


ANDERSEN Global has announced the debut of the Andersen name in United Kingdom with the establishment of Andersen Tax LLP.
 Andersen Tax LLP in the UK joins the global organization as the first member firm in the UK and is led by Partners George McCracken, Julian Nelberg, and Paul Lloyds..
 The team specializes in inbound and outbound cross-border income and estate planning as well as personal tax services to alternative asset managers..
 George McCracken joins Andersen Tax LLP with more than 40 years of experience advising both ultra-high net worth individuals and larger companies on complex international tax matters..
 He was formerly the Head of Tax at Arthur Andersen in Scotland and later worked for both Deloitte and Grant Thornton.
 Julian Nelberg and Paul Lloyds join Andersen Tax LLP from PwC.. Julian has more than 22 years of experience and the reputation of being one of the best in his field.
 He is joined by Paul Lloyds who has more than 13 years of experience and was named a Rising Star by Spears Wealth in 2016..
 Unlike a lot of firms, we are not focused on quick, impersonal, cookie-cutter solutions for clients, said George.
 We have long focused on helping our clients find concrete, sustainable solutions to their needs..
 Joining the Andersen family only broadens our ability to develop seamless, quality solutions and provide our clients with best-in-class service.
 We have had a close working relationship with the professionals of Andersen Global for some time now, and we are excited to be adopting the name and formally joining forces with the other member firms of Andersen Global..
 Increasing complexities in tax legislation around the world have only increased the necessity for clients to have the best and most trusted advisors with reach in every global region, said Mark.
 The establishment of Andersen Tax in the UK by George, Paul and Julian is an important milestone for us and will serve as a beachhead for further growth in the UK..
 Andersen Global is an international association of legally separate, independent member firms comprised of tax and legal professionals around the world.
 Established in 2013 by U.S. member firm Andersen Tax LLC, Andersen Global now has over 4,500 professionals worldwide and a presence in over 144 locations through its member firms and collaborating firms..
 – July 10, 2019 @ 19:37 GMT |. (Visited 8 times, 9 visits today).


 Andersen Global ist stolz darauf, mit der Gründung von Andersen Tax LLP das Debüt des Firmennamens Andersen in Großbritannien bekanntzugeben.
 Andersen Tax LLP in Großbritannien wird als erste Mitgliedsfirma in Großbritannien in die globale Organisation aufgenommen und wird von den Partnern George McCracken, Julian Nelberg und Paul Lloyds geführt.
 Das Team ist spezialisiert auf die grenzüberschreitende Einkommens- und Nachlassplanung im In- und Outbound-Bereich sowie auf persönliche Steuerdienstleistungen für alternative Vermögensverwalter. .
 George McCracken kommt mit mehr als 40 Jahren Erfahrung zu Andersen Tax LLP, wo er sowohl vermögende Privatpersonen als auch größere Unternehmen in komplexen internationalen Steuerfragen berät.
 Zuvor war er Leiter der Steuerabteilung bei Arthur Andersen in Schottland und arbeitete später sowohl für Deloitte als auch für Grant Thornton.
 Julian Nelberg und Paul Lloyds wechseln von PwC zu Andersen Tax LLP.
 Julian hat mehr als 22 Jahre Erfahrung und den Ruf, einer der Besten auf seinem Gebiet zu sein.
 Er wird von Paul Lloyds unterstützt, der über mehr als 13 Jahre Erfahrung verfügt und 2016 von  zum Rising Star ernannt wurde. .
 Im Gegensatz zu vielen anderen Unternehmen konzentrieren wir uns nicht auf schnelle, unpersönliche Standard-Lösungen für Kunden, sagte George.
 Wir konzentrieren uns seit langem darauf, unseren Kunden zu helfen, konkrete und nachhaltige Lösungen für ihre Bedürfnisse zu finden.
 Der Beitritt zur Andersen-Familie erweitert unsere Fähigkeit, nahtlose und qualitativ hochwertige Lösungen zu entwickeln und unseren Kunden einen erstklassigen Service zu bieten.
 Wir arbeiten seit einiger Zeit eng mit den Fachleuten von Andersen Global zusammen und freuen uns, den Namen zu übernehmen und uns offiziell mit den anderen Mitgliedsfirmen von Andersen Global zusammenzuschließen. .
 Die zunehmende Komplexität der Steuergesetzgebung auf der ganzen Welt hat die Notwendigkeit für die Kunden, die besten und vertrauenswürdigsten Berater mit einer weltweiten Abdeckung zu haben, nur noch erhöht, so Mark Vorsatz, Vorstandsvorsitzender von Andersen Global und CEO von Andersen Tax LLC.
 Die Gründung von Andersen Tax in Großbritannien durch George, Paul und Julian ist ein wichtiger Meilenstein für uns und wird als Ausgangspunkt für weiteres Wachstum in Großbritannien dienen. .
 Andersen Global ist ein internationaler Verband rechtlich eigenständiger und unabhängiger Mitgliedsfirmen, dem Steuer- und Rechtsexperten aus aller Welt angehören.
 Andersen Global wurde im Jahr 2013 von der US-amerikanischen Mitgliedsfirma Andersen Tax LLC gegründet, beschäftigt derzeit über 4.500 Fachkräfte weltweit und ist über seine Mitgliedsfirmen und Kooperationspartner an über 144 Standorten vertreten. .
 Die Ausgangssprache, in der der Originaltext veröffentlicht wird, ist die offizielle und autorisierte Version.
 Nur die Sprachversion, die im Original veröffentlicht wurde, ist rechtsgültig.
 Gleichen Sie deshalb Übersetzungen mit der originalen Sprachversion der Veröffentlichung ab. .

 -[ RECORD 1 ]---+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 source_sentence | ANDERSEN Global has announced the debut of the Andersen name in United Kingdom with the establishment of Andersen Tax LLP.
 target_sentence | Andersen Global ist stolz darauf, mit der Gründung von Andersen Tax LLP das Debüt des Firmennamens Andersen in Großbritannien bekanntzugeben.
 -[ RECORD 2 ]---+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 source_sentence | Andersen Global is an international association of legally separate, independent member firms comprised of tax and legal professionals around the world.
 target_sentence | Andersen Global ist ein internationaler Verband rechtlich eigenständiger und unabhängiger Mitgliedsfirmen, dem Steuer- und Rechtsexperten aus aller Welt angehören.
 -[ RECORD 3 ]---+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 source_sentence | He was formerly the Head of Tax at Arthur Andersen in Scotland and later worked for both Deloitte and Grant Thornton.
 target_sentence | Zuvor war er Leiter der Steuerabteilung bei Arthur Andersen in Schottland und arbeitete später sowohl für Deloitte als auch für Grant Thornton.
 -[ RECORD 4 ]---+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 source_sentence | Joining the Andersen family only broadens our ability to develop seamless, quality solutions and provide our clients with best-in-class service.
 target_sentence | Der Beitritt zur Andersen-Familie erweitert unsere Fähigkeit, nahtlose und qualitativ hochwertige Lösungen zu entwickeln und unseren Kunden einen erstklassigen Service zu bieten.

 -[ RECORD 5 ]---+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 source_sentence | Andersen Tax LLP in the UK joins the global organization as the first member firm in the UK and is led by Partners George McCracken, Julian Nelberg, and Paul Lloyds..
 target_sentence | Andersen Tax LLP in Großbritannien wird als erste Mitgliedsfirma in Großbritannien in die globale Organisation aufgenommen und wird von den Partnern George McCracken, Julian Nelberg und Paul Lloyds geführt.
 -[ RECORD 6 ]---+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 source_sentence | George McCracken joins Andersen Tax LLP with more than 40 years of experience advising both ultra-high net worth individuals and larger companies on complex international tax matters..
 target_sentence | George McCracken kommt mit mehr als 40 Jahren Erfahrung zu Andersen Tax LLP, wo er sowohl vermögende Privatpersonen als auch größere Unternehmen in komplexen internationalen Steuerfragen berät.
 -[ RECORD 7 ]---+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 source_sentence | Increasing complexities in tax legislation around the world have only increased the necessity for clients to have the best and most trusted advisors with reach in every global region, said Mark.
 target_sentence | Die zunehmende Komplexität der Steuergesetzgebung auf der ganzen Welt hat die Notwendigkeit für die Kunden, die besten und vertrauenswürdigsten Berater mit einer weltweiten Abdeckung zu haben, nur noch erhöht, so Mark Vorsatz, Vorstandsvorsitzender von Andersen Global und CEO von Andersen Tax LLC.
 -[ RECORD 8 ]---+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 source_sentence | Julian Nelberg and Paul Lloyds join Andersen Tax LLP from PwC.. Julian has more than 22 years of experience and the reputation of being one of the best in his field.
 target_sentence | Julian Nelberg und Paul Lloyds wechseln von PwC zu Andersen Tax LLP.
 -[ RECORD 9 ]---+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 source_sentence | We have long focused on helping our clients find concrete, sustainable solutions to their needs..
 target_sentence | Wir konzentrieren uns seit langem darauf, unseren Kunden zu helfen, konkrete und nachhaltige Lösungen für ihre Bedürfnisse zu finden.
 -[ RECORD 10 ]--+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 source_sentence | Unlike a lot of firms, we are not focused on quick, impersonal, cookie-cutter solutions for clients, said George.
 target_sentence | Im Gegensatz zu vielen anderen Unternehmen konzentrieren wir uns nicht auf schnelle, unpersönliche Standard-Lösungen für Kunden, sagte George.



















----------------


source_article_id | /app/LASER-Thesis/tasks/news_uni_leipzig/input_files/2020-01-16_en_article_11190
target_article_id | /app/LASER-Thesis/tasks/news_uni_leipzig/input_files/2020-01-17_de_article_658
