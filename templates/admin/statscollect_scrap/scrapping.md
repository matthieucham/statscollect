# Instructions
Suivre la procédure dans l'ordre indiqué pour importer complètement une journée de championnat. En fonction de vos
droits, vous ne pourrez accomplir qu'une partie de la procédure vous mêmes, et compter sur vos collègues pour
accomplir le reste.

## 1) Importer la journée

- Pour importer une nouvelle journée : cliquer sur *+Add* de la rubrique *Imports de journées*. Pour éditer
une journée en cours d'importation, cliquer sur *Change*.

- Renseigner le formulaire puis cliquer sur *Scrap data* pour déclencher l'importation. Après cette étape, les
journées en cours d'importation ont le statut **PENDING**

- Vérifier et corriger les données importées : équipes, scores et dates, puis cliquer sur *Save into model* pour copier
les
matchs dans la base
de données principale. Une entrée par rencontre de la journée est alors créée dans la rubrique *Imports de
feuilles de matchs*. Après cette étape, les journées en cours d'importation ont le statut **COMPLETE**

- Il est possible de modifier les données importées par la suite, puis de transmettre ces modifications à la base
principale. Une journée importée ayant connu une telle modification ultérieure a le statut **AMENDED**

## 2) Importer les feuilles de match

*Préambule* Il n'est pas possible de créer une nouvelle feuille de match from scratch. On ne peut que modifier des
feuilles de
matchs qui ont été créées automatiquement suite à l'étape 1.

- Cliquer sur **Imports de feuilles de match**, puis sur la feuille de match à importer. Les feuilles nouvellement
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

## 3) Importer les statistiques de match
*Préambule* Il n'est pas possible de créer une nouvelle entrée from scratch. On ne peut que modifier des
recueils de statistiques qui ont été crées automatiquement suite à l'étape 2.

- Cliquer sur **Imports de statistiques de match**, puis sur le match à importer. Les matchs nouvellement
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

## 4) Importer les notes
*Préambule* Il n'est pas possible de créer une nouvelle entrée from scratch. On ne peut que modifier des
recueils de notes qui ont été crées automatiquement suite à l'étape 2.

- Cliquer sur **Imports de notes de match**, puis sur l'entrée à importer. Les entrées nouvellement
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

**Voilà, vous savez tout ! :rockon: **