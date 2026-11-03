# Maquettes du nouveau site — Ouvrir Les Yeux

Prototype navigable de la refonte du site de l'association Ouvrir Les Yeux (OLY).
Document de travail, non contractuel. Site publié avec GitHub Pages : la page d'entrée est `index.html` (sommaire des maquettes).

## Contenu

- **Gabarits de référence** (`accueil.html`, `actualites.html`, `article.html`, `page-a.html`, `page-b.html`, `don.html`, `systeme-de-design.html`) : exportés du canevas Claude « Maquettes OLY ».
- **Toutes les autres pages** : générées à partir de l'arborescence de septembre 2026 et du texte du site actuel (corpus du 25/09/2026). Elles reprennent les gabarits validés.
- `a-venir.html` : page d'attente pour les liens hors périmètre (langues, recherche…).

## Mettre à jour

1. Demander la modification à Claude dans le projet OLY.
2. Claude modifie le canevas et/ou `outils/pages.py` (plan du site, sources des textes), puis lance :
   `python3 outils/build.py <chemin du corpus Corpus_contenus_OLY_2026-09-25.md>`
3. Claude vérifie l'accessibilité (axe-core, 1440 px et 390 px) et pousse sur ce dépôt.
4. GitHub Pages republie le site automatiquement en une à deux minutes.

## Fichiers des outils

| Fichier | Rôle |
|---------|------|
| `outils/canvas/*.dc.html` | Copie des planches du canevas (gabarits de référence) |
| `outils/pages.py` | Plan du site : pages, rubriques, sources des textes, liens |
| `outils/build.py` | Générateur du site |
| `outils/static/` | Sommaire, page d'attente, ce README |

## Accessibilité

Conçu pour le RGAA / WCAG 2.1 AA. Chaque version est contrôlée avec axe-core en 1440 px et 390 px avant publication.
