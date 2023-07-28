# Application Projet 12 - Epic Event CRM

Bienvenue dans l'application **Projet 12 - Epic Event CRM**, un logiciel de gestion de la relation client (Customer Relationship Management - CRM) conçu pour améliorer le travail d'EPIC EVENT, une entreprise spécialisée dans l'organisation d'événements (fêtes, réunions professionnelles, manifestations hors les murs) pour ses clients. Cette application propose une interface CLI (Command Line Interface - en ligne de commande).

## Présentation du Projet

L'objectif de cette application est de faciliter la gestion des données liées aux collaborateurs, clients, contrats et événements pour EPIC EVENT. Elle est sécurisée, nécessitant une connexion avec un email et un mot de passe. Un token est généré à l'authentification de l'utilisateur, expirant après 10 minutes, pour vérifier l'authenticité de l'accès aux requêtes spécifiques. Des permissions sont également mises en place pour limiter certaines requêtes en fonction des rôles des utilisateurs (administrateur, vendeur ou support). Pour plus d'informations sur les permissions, veuillez vous référer à la documentation disponible dans le repository.

Les modèles principaux de l'application sont les suivants :
- Collaborator (Collaborateur)
- Customer (Client)
- Contract (Contrat)
- Event (Événement)

Pour chacun de ces modèles, l'application propose les fonctionnalités suivantes :
- Création (create)
- Mise à jour (update)
- Suppression (delete)
- Lecture en liste (list)
- Lecture en détail (detail) par identifiant (id) pour tous les modèles, et également par email pour les Collaborateurs et Clients.

## Installation

Pour pouvoir utiliser l'application, suivez ces étapes d'installation :

1. **PostgreSQL** :
   - Installez PostgreSQL sur votre système d'exploitation en téléchargeant le programme à partir du site officiel : [Télécharger PostgreSQL](https://www.postgresql.org/download/).
   - Suivez les instructions d'installation appropriées pour votre système d'exploitation.

2. **Graphviz** :
   - Graphviz est requis pour la génération et l'actualisation du diagramme ERD (UML) des modèles utilisés dans l'application.
   - Téléchargez Graphviz à partir du site officiel : [Télécharger Graphviz](https://graphviz.org/download/).
   - Suivez les instructions d'installation adaptées à votre système d'exploitation.

3. **Environnement virtuel** :
   - Mettez en place un environnement virtuel pour isoler les dépendances de l'application. Pour ce faire, vous pouvez utiliser `venv` :
     ```
     python -m venv venv
     ```

4. **Dépendances** :
   - Activez votre environnement virtuel :
     - Sous Windows (Powershell) :
       ```
       venv\Scripts\activate
       ```
     - Sous macOS/Linux :
       ```
       source venv/bin/activate
       ```
   - Installez les dépendances nécessaires en exécutant la commande suivante :
     ```
     pip install -r requirements.txt
     ```

5. **Initialisation de l'application et configuration de la base de données** :
   - Lors de la première utilisation, exécutez la commande suivante dans PowerShell (Windows) ou Terminal (macOS/Linux) :
     - Sous Windows (Powershell) :
       ```
       python main.py
       ```
     - Sous macOS/Linux :
       ```
       python3 main.py
       ```
   - Cette commande vous guidera pour créer ou vous connecter à une base de données existante dans PostgreSQL en remplissant un formulaire.

6. **Création du premier administrateur** :
   - Une fois que la base de données est configurée et fonctionnelle, vous serez invité à créer le premier administrateur si aucun n'existe dans la base de données.

## Utilisation

Félicitations ! Vous avez suivi toutes les étapes d'installation et de configuration de l'application. Vous êtes désormais prêt à utiliser l'application Projet 12 - Epic Event CRM.

Pour accéder au menu principal de l'application, utilisez la commande suivante :
- Sous Windows (Powershell) :
  ```
  python main.py
  ```
- Sous macOS/Linux :
  ```
  python3 main.py
  ```

Pour accéder au menu de connexion avec un formulaire :
- Sous Windows (Powershell) :
  ```
  python main.py form login
  ```
- Sous macOS/Linux :
  ```
  python3 main.py form login
  ```

Si vous avez besoin d'aide concernant une commande, vous pouvez utiliser l'option "--help". Par exemple, pour obtenir de l'aide sur la création d'un collaborateur :
- Sous Windows (Powershell) :
  ```
  python main.py collaborator create --help
  ```
- Sous macOS/Linux :
  ```
  python3 main.py collaborator create --help
  ```

## Documentation

Une documentation complète est disponible dans le repository, elle présente les différents endpoints et fonctionnalités accessibles via l'interface CLI. Vous pouvez la consulter pour en savoir plus sur les commandes disponibles et leur utilisation.

## Contact

Merci de l'intérêt que vous portez à notre application Projet 12 - Epic Event CRM ! Si vous avez des remarques, des questions ou besoin d'assistance, n'hésitez pas à nous contacter par e-mail à l'adresse : developpeur@examplemail.fr.

Nous vous souhaitons une excellente utilisation de notre application !

Développeur du code : Nicolas Deleu