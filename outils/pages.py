"""Site map of the OLY prototype: every page, where its text comes from, and how it is linked.

Line numbers refer to the content corpus « Corpus_contenus_OLY_2026-09-25.md » (project OLY in Claude).
A part is (heading, first_line, last_line); heading None keeps the corpus' own sub-headings at h2 level.
"""

# Rubriques of the main menu: id -> (landing file, label used in breadcrumbs, pastel colour)
RUBRIQUES = {
    'noh': ('les-noh.html', 'Les NOH', '#E3F0FC'),
    'vie': ('la-vie-handicap-visuel.html', 'La vie en situation de handicap visuel', '#E2F3EE'),
    'actions': ('nos-actions.html', 'Nos Actions', '#FFE6E5'),
    'actus': ('actualites.html', 'Nos Actualités', '#FFEBDD'),
    'partenaires': ('nos-partenaires.html', 'Nos Partenaires', '#E3F0FC'),
    'faq': ('questions-frequentes.html', 'Les Questions Fréquentes', '#E2F3EE'),
    'boutique': ('notre-boutique.html', 'Notre boutique', '#FFE6E5'),
    'asso': ('qui-sommes-nous.html', "L'association", '#E3F0FC'),
    'agir': ('agir-avec-nous.html', 'Agir avec nous', '#FFE6E5'),
    'infos': ('contact.html', 'Infos pratiques', '#E3F0FC'),
}

# Content pages generated from the corpus.
PAGES = [
    # --- Les NOH ---
    dict(file='que-sont-ces-maladies.html', rub='noh', title='Que sont ces maladies ?',
         card="Les neuropathies optiques héréditaires : Leber, Kjer, et le rôle des mitochondries.",
         intro="Les neuropathies optiques héréditaires (NOH) sont des maladies rares du nerf optique, la plupart d'origine mitochondriale.",
         parts=[('Les NOH, neuropathies optiques héréditaires', 1207, 1259),
                ('La neuropathie optique héréditaire de Leber', 1260, 1335),
                ('La maladie de Kjer', 1336, 1350),
                ('Les NOH, maladies mitochondriales', 1140, 1206)]),
    dict(file='prevention.html', rub='noh', title='Prévention',
         card="Porteur sain, déclenchement, transmission et recommandations actuelles.",
         intro="Ce que l'on sait aujourd'hui du porteur sain, du déclenchement de la maladie et de sa transmission.",
         parts=[('Le porteur sain', 1360, 1381), ('Le déclenchement', 1382, 1396),
                ('La transmission des NOH', 1397, 1410), ('Les recommandations actuelles', 1822, 1840)]),
    dict(file='page-a.html', rub='noh', title='Le diagnostic et parcours de soin', template=True,
         card="Consulter un centre expert, confirmer le diagnostic, être suivi."),
    dict(file='les-traitements.html', rub='noh', title='Les traitements',
         card="Idébénone, thérapie génique et essais cliniques.",
         intro="Les traitements disponibles ou à l'étude pour les neuropathies optiques héréditaires.",
         parts=[('Idébénone et thérapie génique', 1442, 1453), ('La thérapie génique', 1507, 1564),
                ('Les essais cliniques', 1590, 1630)]),
    dict(file='la-recherche.html', rub='noh', title='La recherche',
         card="L'histoire de la recherche sur les NOH, ses acteurs et ses pistes.",
         intro="Où en est la recherche sur les neuropathies optiques héréditaires, et qui la mène.",
         parts=[(None, 1420, 1441), (None, 1454, 1487)]),
    # --- La vie en situation de handicap visuel ---
    dict(file='les-demarches.html', rub='vie', title='Les démarches',
         card="MDPH, compensation du handicap, aides financières, scolarité et emploi.",
         intro="Les démarches pour faire valoir vos droits : compensation du handicap, aides, scolarité et vie professionnelle.",
         parts=[('Vous aider à faire valoir vos droits', 1865, 1912), ('La compensation du handicap', 2013, 2040),
                ("L'aide financière", 2218, 2236), ('La scolarité', 2246, 2279), ('Le parcours professionnel', 2280, 2292)]),
    dict(file='adapter-son-environnement.html', rub='vie', title='Adapter son environnement',
         card="Informatique adaptée, matériel, téléphonie et déplacements.",
         intro="Les aides techniques pour gagner en autonomie à la maison, au travail et dans les déplacements.",
         parts=[('Sur ordinateur', 2081, 2150), ('Le matériel adapté', 2151, 2190),
                ('Téléphonie', 2191, 2217), ('Les déplacements', 2383, 2449)]),
    dict(file='les-aidants.html', rub='vie', title='Les aidants',
         card="L'aide humaine et le soutien aux aidants familiaux.",
         intro="Accompagner un proche touché par une NOH : l'aide humaine et les ressources pour les aidants.",
         parts=[("L'aide humaine", 2041, 2071), ('Les aidants familiaux', 2294, 2298)]),
    dict(file='les-loisirs.html', rub='vie', title='Les loisirs',
         card="Lecture, podcast, sport, jeux : des loisirs accessibles.",
         intro="Des idées et des ressources pour des loisirs accessibles aux personnes déficientes visuelles.",
         parts=[(None, 2300, 2382)]),
    # --- Nos Actions ---
    dict(file='la-pair-aidance.html', rub='actions', title='La pair-aidance',
         card="Le comité d'aide aux personnes concernées et le Pôle Jeunesse.",
         intro="Des personnes concernées accompagnent d'autres personnes concernées et leurs proches.",
         parts=[("Notre comité d'aide pour les personnes concernées", 292, 320), ("Le Pôle Jeunesse d'OLY", 2451, 2492)]),
    dict(file='recherche-oly.html', rub='actions', title='Recherche',
         card="Ce que fait OLY pour la recherche : santé, prix Espoir.",
         intro="Ouvrir Les Yeux encourage et soutient la recherche sur les neuropathies optiques héréditaires.",
         parts=[('Dans le domaine de la santé', 499, 509)],
         extra='<h2 id="prix-espoir">Le prix Espoir d\'OLY</h2><p>Chaque année, l\'association récompense de jeunes docteurs en sciences et en médecine dont les travaux font progresser la connaissance des NOH. <a href="article.html">Lire l\'appel à candidatures</a>.</p>'),
    dict(file='plaidoyer.html', rub='actions', title='Plaidoyer',
         card="Accessibilité, sensibilisation à la cécité et projet ERASMUS+ Open Up.",
         intro="Changer les regards et faire avancer l'accessibilité, auprès du public comme des décideurs.",
         parts=[("Dans le domaine de l'accessibilité", 511, 525), ('Sensibiliser à la cécité', 527, 560),
                ('Le regard des Français sur la cécité', 1934, 2012), ('Le projet ERASMUS+ Open Up', 562, 631)]),
    dict(file='la-ruche.html', rub='actions', title='La ruche', placeholder=True,
         card="Page à rédiger par l'association.",
         intro="Cette rubrique est nouvelle : le site actuel ne contient pas encore de texte à son sujet."),
    # --- Boutique ---
    dict(file='notre-boutique.html', rub='boutique', title='Notre boutique', landing_self=True,
         card="Livre, cartes de vœux, chanson : des achats solidaires.",
         intro="Chaque achat soutient l'association. La boutique en ligne est gérée par HelloAsso.",
         parts=[(None, 1009, 1034)],
         extra='<p><a class="btn btn-primary" href="https://www.helloasso.com/associations/ouvrir-les-yeux">Voir la boutique sur HelloAsso</a></p>'),
    # --- L'association (hors menu principal : pied de page et Nos Actions) ---
    dict(file='qui-sommes-nous.html', rub='asso', title='Qui sommes-nous ?', landing_self=True,
         card="L'association, ses missions et ses valeurs.",
         intro="Ouvrir Les Yeux est l'association des personnes touchées par toutes les neuropathies optiques héréditaires.",
         parts=[(None, 111, 155), ('Nos missions', 483, 497), ('Nos valeurs', 157, 181)]),
    dict(file='notre-histoire.html', rub='asso', title='Notre histoire',
         card="De la création de l'association à aujourd'hui.",
         intro="L'histoire d'Ouvrir Les Yeux, racontée par celles et ceux qui l'ont construite.",
         parts=[(None, 322, 471)]),
    dict(file='comite-medico-scientifique.html', rub='asso', title='Notre comité médico-scientifique',
         card="Les médecins et chercheurs qui conseillent l'association.",
         intro="Le comité médico-scientifique conseille l'association sur les questions médicales et de recherche.",
         parts=[(None, 195, 268)]),
    dict(file='nos-antennes.html', rub='asso', title='Nos antennes',
         card="Les délégations régionales de l'association.",
         intro="Les antennes d'Ouvrir Les Yeux, au plus près des personnes concernées.",
         parts=[(None, 270, 290)]),
    # --- Agir avec nous ---
    dict(file='agir-avec-nous.html', rub='agir', title='Agir avec nous', landing_self=True,
         card="Don, adhésion, bénévolat, mécénat, legs.",
         intro="Grâce à votre don, à votre adhésion ou aux autres formes de soutien, vous aidez les personnes atteintes de NOH et leurs proches.",
         parts=[(None, 794, 843)]),
    dict(file='adherer.html', rub='agir', title='Adhérer',
         card="Pourquoi adhérer, montant de la cotisation, comment adhérer.",
         intro="Rejoindre l'association, c'est faire entendre la voix des personnes concernées et soutenir la recherche.",
         parts=[(None, 853, 929)]),
    dict(file='devenir-benevole.html', rub='agir', title='Devenir bénévole',
         card="Donner un peu de son temps, à distance ou près de chez soi.",
         intro="Ouvrir Les Yeux a besoin de vous et de vos compétences.",
         parts=[(None, 995, 1007)]),
    dict(file='mecenat.html', rub='agir', title='Le mécénat',
         card="Entreprises : un levier pour la recherche.",
         intro="Le mécénat d'entreprise, un levier pour la recherche et un espoir pour les malades.",
         parts=[(None, 1071, 1107)]),
    dict(file='legs.html', rub='agir', title='Le legs',
         card="Transmettre à l'association.",
         intro="Le legs permet de soutenir durablement l'action de l'association.",
         parts=[(None, 1109, 1131)]),
    dict(file='taxe-apprentissage.html', rub='agir', title="La taxe d'apprentissage",
         card="Un geste simple pour soutenir la recherche.",
         intro="Les entreprises peuvent affecter une part de leur taxe d'apprentissage à la recherche sur les NOH.",
         parts=[(None, 1036, 1069)]),
    # --- Infos pratiques ---
    dict(file='mentions-legales.html', rub='infos', title='Mentions légales et confidentialité',
         card="Éditeur, hébergeur, données personnelles, cookies.",
         intro="Les informations légales du site et la politique de confidentialité des données.",
         parts=[(None, 2716, 2945)]),
]

# Partner pages: lists taken from the corpus « Nos partenaires » section.
PARTNERS = {
    'partenaires-institutionnels.html': ('Institutionnels', "Collectivités, établissements de santé et organismes publics qui soutiennent l'association.", [(712, 719)], None),
    'partenaires-entreprises.html': ('Entreprises', "Les entreprises et médias partenaires de l'association.", [(721, 730)], 'notfondation'),
    'partenaires-associations.html': ('Associations', "Les associations avec lesquelles Ouvrir Les Yeux agit.", [(700, 710)], None),
    'partenaires-fondations.html': ('Fondations', "Les fondations qui soutiennent l'association.", [(721, 730)], 'fondation'),
    'partenaires-personnalites.html': ('Personnalités', "Notre parrain, et les artistes et sportifs qui soutiennent l'association.", [(732, 739), (741, 750)], None),
}

FAQ = {
    'faq-malade.html': ('Je suis malade', [
        ("Où consulter pour obtenir un diagnostic ?", "Prenez rendez-vous dans le centre de compétence OPHTARA de votre région. OPHTARA est le centre de référence pour les maladies rares en ophtalmologie.", 'page-a.html', 'Le diagnostic et parcours de soin'),
        ("Comment le diagnostic est-il confirmé ?", "Le diagnostic moléculaire se fait grâce à une prise de sang, analysée par l'un des laboratoires spécialisés du réseau national.", 'page-a.html', 'Le diagnostic et parcours de soin'),
        ("Existe-t-il un traitement ?", "Des traitements peuvent permettre une récupération visuelle plus ou moins importante. Il n'existe pas aujourd'hui de traitement qui permette de recouvrer complètement la vue.", 'les-traitements.html', 'Les traitements'),
        ("Quelles aides puis-je obtenir ?", "La MDPH est le point d'entrée pour la compensation du handicap : aide humaine, aides techniques, aides financières.", 'les-demarches.html', 'Les démarches'),
        ("Puis-je échanger avec d'autres personnes concernées ?", "Oui : le comité d'aide de l'association est composé de personnes concernées qui vous écoutent et vous orientent.", 'la-pair-aidance.html', 'La pair-aidance'),
    ]),
    'faq-aidant.html': ('Je suis aidant', [
        ("Comment accompagner un proche touché par une NOH ?", "Le comité d'aide de l'association écoute et oriente aussi les proches des personnes concernées.", 'la-pair-aidance.html', 'La pair-aidance'),
        ("Quelles aides humaines existent ?", "Selon la situation, la MDPH peut financer une aide humaine. Des structures spécialisées accompagnent les familles.", 'les-aidants.html', 'Les aidants'),
        ("Mon enfant est concerné : comment adapter sa scolarité ?", "L'Éducation nationale et des organismes spécialisés accompagnent la scolarité des élèves déficients visuels.", 'les-demarches.html', 'Les démarches'),
        ("Suis-je porteur de la maladie ?", "Dans certaines NOH, des personnes portent la mutation sans être malades. La page Prévention explique le porteur sain et la transmission.", 'prevention.html', 'Prévention'),
    ]),
    'faq-medecin.html': ('Je suis médecin', [
        ("Où orienter un patient ?", "Vers le centre de référence OPHTARA ou un centre de compétence maladies rares en ophtalmologie.", 'page-a.html', 'Le diagnostic et parcours de soin'),
        ("Existe-t-il des protocoles nationaux de diagnostic et de soins ?", "Oui : la Haute Autorité de santé a publié en juillet 2021 un PNDS pour l'atrophie optique dominante OPA1 et un pour les neuropathies optiques héréditaires.", 'page-a.html', 'Le diagnostic et parcours de soin'),
        ("Où se fait le diagnostic moléculaire ?", "Une dizaine de laboratoires français, regroupés en réseau national, réalisent ces analyses.", 'page-a.html', 'Le diagnostic et parcours de soin'),
        ("Qui conseille l'association sur le plan médical ?", "Son comité médico-scientifique, composé de médecins et de chercheurs.", 'comite-medico-scientifique.html', 'Notre comité médico-scientifique'),
        ("Je suis jeune chercheur : l'association soutient-elle la recherche ?", "Oui, notamment par le prix Espoir d'OLY, destiné aux jeunes docteurs travaillant sur les NOH.", 'article.html', "L'appel à candidatures du prix Espoir"),
    ]),
}

# Landing pages of the main rubriques: (rubrique id, intro, list of child files)
LANDINGS = {
    'les-noh.html': ('noh', "Tout savoir sur les neuropathies optiques héréditaires : ce qu'elles sont, comment les prévenir, les diagnostiquer et les traiter.",
                     ['que-sont-ces-maladies.html', 'prevention.html', 'page-a.html', 'les-traitements.html', 'la-recherche.html']),
    'la-vie-handicap-visuel.html': ('vie', "Faire valoir ses droits, adapter son environnement, être aidé et profiter de ses loisirs.",
                                    ['les-demarches.html', 'adapter-son-environnement.html', 'les-aidants.html', 'les-loisirs.html']),
    'nos-actions.html': ('actions', "Rassembler les personnes concernées, agir auprès des décideurs, faire connaître les NOH et encourager la recherche.",
                         ['la-pair-aidance.html', 'recherche-oly.html', 'plaidoyer.html', 'la-ruche.html', 'qui-sommes-nous.html']),
    'nos-partenaires.html': ('partenaires', "Institutions, entreprises, associations, fondations et personnalités : ils soutiennent Ouvrir Les Yeux.",
                             list(PARTNERS)),
    'questions-frequentes.html': ('faq', "Les réponses aux questions les plus fréquentes, selon votre situation.",
                                  list(FAQ)),
}

# Pages whose standalone bold lines are real headings (RGAA 9.1). Elsewhere bold lines stay emphasis.
BOLD_HEADINGS = {'que-sont-ces-maladies.html', 'mentions-legales.html', 'adapter-son-environnement.html',
                 'la-recherche.html', 'adherer.html', 'les-traitements.html'}

# Link texts that do not make sense on their own (RGAA 6.1 good practice): (page, old text, new text, new href or None)
LINK_TEXT_FIXES = [
    ('les-aidants.html', 'Cliquez ici', "Les démarches auprès de la MDPH", 'les-demarches.html'),
    ('les-demarches.html', 'cliquez ici', "Qu'est-ce qu'une MDPH ? (site mdph.fr)", None),
    ('les-demarches.html', 'En savoir plus', "En savoir plus sur le Club Emploi du GIAA (site apidv.org)", None),
]

# Menu labels and other link texts -> destination file.
LINKS = {
    'Accueil': 'accueil.html', 'Faire un don': 'don.html',
    'Nos Actualités': 'actualites.html', 'Nos actualités': 'actualites.html', 'Toutes les actualités': 'actualites.html',
    'Internes': 'actualites.html', 'Externes': 'actualites.html', 'Toutes': 'actualites.html',
    'Page suivante': 'actualites.html', '1': 'actualites.html', '2': 'actualites.html', '3': 'actualites.html',
    'Les NOH': 'les-noh.html', 'Tout savoir sur les NOH': 'les-noh.html', 'Découvrir les NOH': 'les-noh.html',
    'Que sont ces maladies': 'que-sont-ces-maladies.html', 'Prévention': 'prevention.html',
    'Le diagnostic et parcours de soin': 'page-a.html', 'Les traitements': 'les-traitements.html', 'La recherche': 'la-recherche.html',
    'La vie en situation de handicap visuel': 'la-vie-handicap-visuel.html', 'Toute la rubrique': 'la-vie-handicap-visuel.html',
    'Les démarches': 'les-demarches.html', 'Adapter son environnement': 'adapter-son-environnement.html',
    'Les aidants': 'les-aidants.html', 'Les loisirs': 'les-loisirs.html',
    'Nos Actions': 'nos-actions.html', 'Toutes nos actions': 'nos-actions.html', 'Découvrir nos actions': 'nos-actions.html',
    'Voir toutes nos actions': 'nos-actions.html',
    'La pair-aidance': 'la-pair-aidance.html', 'Recherche': 'recherche-oly.html', 'Plaidoyer': 'plaidoyer.html', 'La ruche': 'la-ruche.html',
    'Nos Partenaires': 'nos-partenaires.html', 'Tous nos partenaires': 'nos-partenaires.html',
    'Institutionnels': 'partenaires-institutionnels.html', 'Entreprises': 'partenaires-entreprises.html',
    'Associations': 'partenaires-associations.html', 'Fondations': 'partenaires-fondations.html', 'Personnalités': 'partenaires-personnalites.html',
    'Les Questions Fréquentes': 'questions-frequentes.html', 'Toutes les questions': 'questions-frequentes.html',
    'Je suis malade': 'faq-malade.html', 'Je suis aidant': 'faq-aidant.html', 'Je suis médecin': 'faq-medecin.html',
    'Notre boutique': 'notre-boutique.html',
    'Agir avec nous': 'agir-avec-nous.html', 'Adhérer': 'adherer.html', "Adhérer à l'association": 'adherer.html',
    'Devenir bénévole': 'devenir-benevole.html', 'Mécénat et legs': 'mecenat.html', 'En savoir plus sur le mécénat': 'mecenat.html',
    'Nous contacter': 'contact.html', 'Plan du site': 'plan-du-site.html',
    'Mentions légales': 'mentions-legales.html', 'Politique de confidentialité': 'mentions-legales.html',
    'Accessibilité : partiellement conforme': 'accessibilite.html', "Voir tout l'agenda": 'agenda.html', 'Agenda': 'agenda.html',
    'comité médico-scientifique': 'comite-medico-scientifique.html', 'Notre comité médico-scientifique': 'comite-medico-scientifique.html',
    'Qui sommes-nous ?': 'qui-sommes-nous.html',
}
