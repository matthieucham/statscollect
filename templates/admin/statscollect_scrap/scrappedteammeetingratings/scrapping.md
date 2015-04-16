## 4) Importer les notes
*Préambule* Il n'est pas possible de créer une nouvelle entrée from scratch. On ne peut que modifier des
recueils de notes qui ont été crées automatiquement suite à l'étape 2.

- Cliquer sur l'entrée à importer. Les entrées nouvellement
créées ont le statut **CREATED**

- Renseigner le formulaire puis cliquer sur *Scrap data* pour déclencher l'importation. Après cette étape, les
recueils de notes en cours d'importation ont le statut **PENDING**

- Vérifier et corriger les notes importées : à chaque fois, la valeur importée (lue sur la page distante) et à comparer
avec
 la valeur à enregistrer dans le champ de saisie à sa droite.

- cliquer sur *Save into model* pour copier les notes dans la base de données principale. Après cette étape les
 recueils de notes de matchs importés ont le statut **COMPLETE**

- **Cas particulier du FakeScrapper** : ce robot ne déclenche pas d'importation à distance. Il est donc inutile de
renseigner la scrapped_url pour l'utiliser : dans ce cas, il faut ajouter un à un les joueurs qui doivent recevoir
une note de la source indiquée, et saisir leur note à la main. Cas d'utilisation : Notes du journal L'Equipe lorsque
la note Orange n'est pas disponible. Un recueil de notes traités par le FakeScrapper passe directement de l'état
**CREATED** à l'état **COMPLETE**.

- Il est possible de modifier les données importées par la suite, puis de transmettre ces modifications à la base
principale. Un recueil de notes de matchs importé ayant connu une telle modification ultérieure a le statut **AMENDED**