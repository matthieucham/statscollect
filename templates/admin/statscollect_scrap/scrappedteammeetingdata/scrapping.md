## 3) Importer les statistiques de match
*Préambule* Il n'est pas possible de créer une nouvelle entrée from scratch. On ne peut que modifier des
recueils de statistiques qui ont été crées automatiquement suite à l'étape 2.

- Cliquer sur le match à importer. Les matchs nouvellement
crées ont le statut **CREATED**

- Renseigner le formulaire puis cliquer sur *Scrap data* pour déclencher l'importation. Après cette étape, les
receuils de statistiques en cours d'importation ont le statut **PENDING**

- Vérifier et corriger les données importées : à chaque fois, la valeur importée (lue sur la page) et à comparer avec
 la valeur à enregistrer dans le champ de saisie à sa droite. Certaines données comme les pénaltys obtenus ne peuvent
  pas être importées automatiquement : il faut penser à modifier la valeur dans le champ de saisie *Actual
  penalties assists* s'il y a lieu.

- cliquer sur *Save into model* pour copier les statistiques dans la base de données principale. Après cette étape les
 recueils de statistiques de matchs importés ont le statut **COMPLETE**

- Il est possible de modifier les données importées par la suite, puis de transmettre ces modifications à la base
principale. Un recueil de statistiques importé ayant connu une telle modification ultérieure a le statut **AMENDED**