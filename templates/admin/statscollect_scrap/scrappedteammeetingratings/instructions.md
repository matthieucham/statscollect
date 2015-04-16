## Cas particulier du FakeScrapper

Ce robot ne déclenche pas d'importation à distance. Il est donc inutile de
renseigner la scrapped_url pour l'utiliser : dans ce cas, il faut ajouter un à un les joueurs qui doivent recevoir
une note de la source indiquée, et saisir leur note à la main. Cas d'utilisation : Notes du journal L'Equipe lorsque
la note Orange n'est pas disponible. Un recueil de notes traités par le FakeScrapper passe directement de l'état
**CREATED** à l'état **COMPLETE**.
