# Projet Médiathèque (Django)

Ce projet est une application Django de gestion d’une médiathèque réalisé dans le cadre de ma formation de développeur web et web mobile.  
Il permet de gérer :
- Les **membres (emprunteurs)**,
- Les **médias** (Livres, DVD, CD, Jeux de plateau),
- Les **emprunts et retours**,
- Avec une séparation **espace public** et **espace staff** (bibliothécaires).

---

## Installation & Exécution

 
Suivez ces étapes :

### 1. Installer Python

Télécharger Python 3.13.7 depuis le site officiel :
 [https://www.python.org/downloads/release/python-3137/](https://www.python.org/downloads/release/python-3137/)

#### Pendant l’installation :

- Cocher "Add Python to PATH".

- Laisser les options par défaut.

##### Vérifier l’installation :

Copier le code

```bash
python --version
```

Cela doit afficher :

**Python 3.13.7**

### 2. Cloner le projet

Copier le code

```bash
git clone https://github.com/MaitreGobz/Projet-mediateque-Django
cd Projet-mediateque-Django
```
### 3. Créer un environnement virtuel

Copier le code

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 4.Installer les dépendances

Copier le code

```bash
pip install -r requirements.txt
```
### 5.Préparer la base de données

Copier le code

```bash
python manage.py migrate
```

### 6. Charger les données de test

Copier le code

```bash
python manage.py loaddata core/fixtures/demo.json
```

### 7. Créer un compte administrateur (staff)

Copier le code

```bash
python manage.py createsuperuser
```
- Choisissez un identifiant et un mot de passe.
- Ce compte servira à vous connecter à /admin/ ou à l’espace staff.

### 8. Lancer le serveur

Copier le code

```bash
python manage.py runserver
```

Accès à l'application via : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 9. Lancer les tests

Copier le code un test après l'autre

```bash
python manage.py test core.tests.test_core
python manage.py test member.tests.test_member
python manage.py test staff.tests.test_staff
```