from typing import List

def search_web(query: str) -> List[str]:
    """
    Simule une recherche web. 
    À remplacer plus tard par Tavily, Serper ou un RAG.
    """
    print(f"    [Tool] Recherche en cours pour : {query}")
    # Simulation de résultats
    return [
        f"Source A: L'IA dans la santé permet de diagnostiquer les maladies plus tôt (Étude 2024).",
        f"Source B: Les agents autonomes réduisent la charge administrative des médecins.",
        f"Source C: Défis éthiques : confidentialité des données patients et biais algorithmiques.",
        f"Source D: Le marché de l'IA en santé devrait atteindre 188 milliards d'ici 2030."
    ]
