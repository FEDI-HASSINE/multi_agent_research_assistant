import os
from dotenv import load_dotenv
from core.langgraph_orchestrator import MultiAgentOrchestrator

# Charger les variables d'environnement
load_dotenv()

def main():
    # Vérification API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERREUR: La clé OPENAI_API_KEY est manquante dans le fichier .env")
        print("Veuillez ajouter votre clé dans le fichier .env : OPENAI_API_KEY=sk-...")
        return

    print("🤖 Initialisation du Multi-Agent Research Assistant...")
    orchestrator = MultiAgentOrchestrator()

    mission = input("\n📝 Entrez votre mission de recherche : ")
    if not mission:
        mission = "L'impact de l'IA générative sur le développement logiciel en 2025"

    print(f"\n🚀 Démarrage de la mission : {mission}\n")
    
    final_state = orchestrator.run(mission)

    print("\n✅ Mission terminée !")
    print("\n📄 RAPPORT FINAL :\n")
    print("="*50)
    print(final_state["draft_report"])
    print("="*50)

if __name__ == "__main__":
    main()
