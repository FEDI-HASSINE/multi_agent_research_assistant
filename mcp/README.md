# 🔌 Dossier MCP (Model Context Protocol)

### 💡 C'est quoi ?
C'est le standard de communication. C'est comme une prise universelle (USB) pour connecter nos agents à leurs outils.

### ❌ Le problème
Si chaque agent appelle ses outils (recherche, écriture) d'une façon différente, le code devient un plat de spaghettis impossible à maintenir. Si on veut changer un outil, on casse tout.

### ✅ La solution
Un protocole standard !
- **Server** : Les outils attendent les ordres de façon standardisée.
- **Client** : Les agents envoient les ordres de la même façon.
Cela permet de débrancher et rebrancher des outils ou des agents sans rien casser.
