# Instagram & Facebook Ashler & Manson — procédure du lot mensuel

Ce dépôt héberge les visuels publiés chaque semaine sur Instagram (@ashlermanson) et sur la page Facebook d'Ashler & Manson. Il sert aussi de « serveur d'images » : Metricool récupère chaque visuel par son lien public `raw.githubusercontent.com`.

Commanditaire : Aymerick PENICAUT, CEO. Il a délégué l'animation entièrement. Il ne valide pas avant publication : il reçoit un récapitulatif et intervient seulement s'il veut modifier ou retirer un post.

## Le format

- **1 post par semaine, le jeudi à 12 h 30, heure de Paris**, sur Instagram et Facebook (même visuel, même légende).
- Une seule information par post. Ton : chic, sobre, jamais racoleur, jamais barbant. Pas d'emojis, pas de point d'exclamation, pas de « Saviez-vous que… ».
- **Quatre rubriques en rotation**, dans cet ordre et en reprenant là où le mois précédent s'est arrêté (voir `historique.md`) :
  1. `chiffre` — **Le chiffre** : un chiffre marquant du marché du crédit immobilier, de l'immobilier ou de l'assurance emprunteur, **vérifié à sa source primaire** (Observatoire Crédit Logement/CSA, Banque de France, INSEE, notaires, ACPR, CCSF…). Le grand chiffre doit tenir sur une ligne (« 1 sur 2 », « 252 mois », « 4,2 ans »).
  2. `mot` — **Le mot juste** : un terme du crédit ou de l'assurance emprunteur, défini en une phrase élégante (quotité, délégation d'assurance, différé, IRA, taux d'usure, HCSF, caution, hypothèque, etc.).
  3. `idee` — **L'idée reçue** : une croyance courante, barrée, suivie de « Faux. » (ou « Pas toujours. ») et de la réalité en une ou deux phrases.
  4. `pierre` — **Bordeaux, côté pierre** : patrimoine, architecture ou histoire de Bordeaux (un quartier, une façade, un pont, un matériau). Facultatif : un dessin au trait en SVG (marine `#16233B`, laiton `#A8875A`, viewBox `0 0 880 430`, pas de remplissage).
- Un mois avec 5 jeudis : le 5e post est une rubrique de plus dans la rotation.
- Ne jamais réutiliser un sujet déjà présent dans `historique.md`.

## Garde-fous réglementaires (non négociables)

- **Aucun chiffre sans source primaire vérifiée** pendant la session (ouvrir le document, lire le chiffre). La source figure sur le visuel (pour « Le chiffre ») et dans la légende.
- **Aucun taux d'intérêt affiché**, ni promesse de taux, d'économie chiffrée ou d'obtention de crédit : un taux exigerait un exemple représentatif. Parler de tendances (« les taux remontent ») est possible, avec source.
- Pas de comparaison avec un concurrent, pas de témoignage client inventé, pas de nom de banque.
- Droit à jour : vérifier l'état du droit avant toute idée reçue juridique (Légifrance, ACPR, service-public.fr). Attention à la réforme CCD2 applicable au 20/11/2026.
- **Mention en fin de chaque légende de crédit ou d'assurance** (copier exactement) :
  `Ashler & Manson, courtier en opérations de banque et en assurance. ORIAS n° 08041452 (orias.fr). Aucun versement, de quelque nature que ce soit, ne peut être exigé d'un particulier avant l'obtention d'un ou plusieurs prêts d'argent.`
  Pour « Bordeaux, côté pierre » (pas de contenu crédit) : `Ashler & Manson, courtier en opérations de banque et en assurance. ORIAS n° 08041452 (orias.fr).`
- Graphie : « Ashler & Manson » (avec esperluette : la SARL de courtage).

## La légende

3 à 6 lignes : une accroche qui reformule l'info, un paragraphe qui donne le contexte ou la conséquence concrète, la source le cas échéant, la mention réglementaire, puis 4 hashtags (`#creditimmobilier`, `#bordeaux`, `#courtier`, `#assuranceemprunteur`, `#immobilier`… selon le sujet). Français soigné, sans anglicismes.

## Procédure pas à pas

1. **Préparer l'outillage** : `cd outils && npm i @fontsource/cormorant-garamond @fontsource/manrope` (Chromium et Playwright sont préinstallés).
2. **Lire `historique.md`** : rubrique suivante dans la rotation, sujets déjà traités.
3. **Lister les jeudis** du mois cible et attribuer une rubrique à chacun.
4. **Rechercher et vérifier** chaque information (WebSearch puis WebFetch du document source). Noter l'URL source.
5. **Écrire `AAAA-MM/posts.json`** sur le modèle de `2026-10/posts.json` : `slug` (`01_le-chiffre`, `02_le-mot-juste`…), `rubrique`, `date` (`AAAA-MM-JJT12:30:00`), `visuel` (champs du gabarit, voir `outils/build.py`), `legende`, `alt` (texte alternatif), `source_url`.
6. **Générer** : `python3 outils/build.py AAAA-MM`, puis **regarder `AAAA-MM/_planche.png`** (outil Read). Corriger : pas de débordement, pas de mot seul en dernière ligne (utiliser `&nbsp;`), grand chiffre lisible. Régénérer si besoin.
7. **Pousser** sur `main` (le `.jpg` est celui que Metricool récupère). Vérifier que chaque `https://raw.githubusercontent.com/ASHLER-MANSON/ashler-manson-social/main/AAAA-MM/<slug>.jpg` répond 200.
8. **Programmer dans Metricool** (connecteur Metricool, marque `blogId` **7285357**, fuseau `Europe/Paris`) avec `createScheduledPost`, un appel par post :
   - `providers` : `[{"network":"instagram"},{"network":"facebook"}]`
   - `media` : le lien raw du `.jpg` ; `mediaAltText` : le champ `alt`
   - `instagramData` : `{"type":"POST","collaborators":[],"showReelOnFeed":true,"isAiGenerated":false}` ; `facebookData` : `{"type":"POST"}`
   - `autoPublish: true`, `draft: false`, `publicationDate` : `{"dateTime":"AAAA-MM-JJT12:30:00","timezone":"Europe/Paris"}`
   - Avant de programmer, vérifier avec `getScheduledPosts` qu'aucun post n'existe déjà sur ces dates (pas de doublon si la tâche est relancée).
   - Formule gratuite Metricool : 20 publications par mois maximum.
9. **Noter les identifiants Metricool** retournés dans `posts.json` (`metricool_id`), **mettre à jour `historique.md`**, committer et pousser.
10. **Récapitulatif** pour Aymerick (message final de la session) : un tableau date / rubrique / sujet / source, la planche des visuels, et une ligne « Pour modifier ou retirer un post, répondez-moi avant sa date ». Court, sans détailler la méthode.

En cas d'échec bloquant (connecteur Metricool déconnecté, GitHub refusé, source introuvable), ne rien publier d'approximatif : programmer ce qui est sûr et signaler clairement ce qui manque.

## Hors périmètre pour l'instant

LinkedIn (payant dans Metricool, écarté le 07/10/2026), TikTok, stories, carrousels.
