# Multi-Agent Research Assistant

### C'est quoi ?
Un assistant de recherche intelligent composé de plusieurs agents IA autonomes qui collaborent pour produire des rapports de haute qualité. Ce n'est pas juste un chatbot, c'est une **équipe virtuelle** dédiée à la recherche.

### Le problème
Faire des recherches approfondies prend du temps. Les LLMs classiques (ChatGPT, Claude) sont géniaux, mais :
- Ils hallucinent parfois des faits.
- Ils manquent de recul critique sur leur propre production.
- Ils ont du mal à gérer des tâches longues et complexes en une seule fois.
- Un seul "cerveau" ne suffit pas pour exceller partout (recherche, rédaction, critique).

### ✅La solution
Une architecture **multi-agents** où chaque IA a un rôle spécialisé, orchestrée par **LangGraph** et connectée via le protocole standard **MCP** (Model Context Protocol).

L'équipe est composée de :
1.  **Manager** : Le chef de projet qui comprend la mission et distribue les tâches.
2.  **Researcher** : L'expert qui fouille le web et les bases de données pour trouver des faits vérifiés.
3.  **Writer** : La plume qui synthétise les informations et rédige un rapport structuré (Markdown/PDF).
4.  **Critic** : Le contrôleur qualité qui relit le travail, détecte les biais et demande des corrections si nécessaire.

### Comment l'utiliser ?

#### 1. Installation
Clonez le projet et installez les dépendances :
```bash
pip install -r requirements.txt
```

#### 2. Configuration
Créez un fichier `.env` à la racine du projet et ajoutez votre clé API OpenAI :
```bash
OPENAI_API_KEY=sk-votre-cle-api-ici
```

#### 3. Lancement
Lancez l'interface utilisateur pour démarrer une mission :
```bash
streamlit run ui/streamlit_app.py
```

### Structure du projet
- `agents/` : Les cerveaux (Manager, Researcher, Writer, Critic).
- `core/` : L'orchestrateur LangGraph et la gestion d'état.
- `mcp/` : Le protocole de communication standardisé entre agents et outils.
- `tools/` : Les capacités concrètes (Recherche, RAG, Export).
- `ui/` : L'interface utilisateur Streamlit.
- `logs/` : L'observabilité (traces et logs d'exécution).
