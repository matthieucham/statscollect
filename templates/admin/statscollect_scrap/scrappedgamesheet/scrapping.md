## 2) Importer les feuilles de match

*Préambule* Il n'est pas possible de créer une nouvelle feuille de match from scratch. On ne peut que modifier des
feuilles de
matchs qui ont été créées automatiquement suite à l'étape 1.

- Cliquer sur la feuille de match à importer. Les feuilles nouvellement
créées ont le statut **CREATED**

- Renseigner le formulaire puis cliquer sur *Scrap data* pour déclencher l'importation. Après cette étape, les
feuilles en cours d'importation ont le statut **PENDING**

- Vérifier et corriger les données importées : joueurs et équipes. Les robots scrappers ne recherchent les joueurs que
dans
l'effectif de chaque équipe. Quand les effectifs des clubs de la base principale ne sont pas à jour, ou si le robot
n'arrive pas reconnaître le nom d'un joueur, il laisse vide le champ *Actual player* correspondant. Dans ce cas c'est
 à vous de retrouver le joueur qui correspond dans la base de données principale. C'est facile : il vous suffit de
 taper quelques lettres du prénom, nom ou surnom du joueur pour que vous soit présentée une liste de propositions de
 plus en plus restreinte.

- cliquer sur *Save into model* pour copier les effectifs dans la base de données principale. Cela provoque
l'insertion d'une entrée dans la rubrique *Imports de statistiques de match* et d'une entrée par source de notation
attendue dans la rubrique *Imports de notes*. Après cette étape les
 feuilles de matchs importées ont le statut **COMPLETE**

- Si jamais le joueur n'existe pas dans la base de données principale, supprimez l'entrée (Case à cocher *Delete* en
haut à droite de la section), finissez la vérification des autres joueurs de la feuille, puis enregistrez (*Save
into model*). Créez le joueur dans la base principale, ou si vous n'en avez pas les droits informez la personne en
charge des créations de joueurs, puis revenez sur la feuille de match, et rajoutez le joueur tout en bas de la
feuille (*Add another joueur*). La feuille de match ainsi modifiée prend alors le statut **AMENDED**