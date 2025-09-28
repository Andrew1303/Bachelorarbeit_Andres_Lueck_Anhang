Versuch 2 beinhaltet RAG (Retrieval Augmented Generation). Für eine Anwendung dieses Versuchs wird vorausgesetzt, dass für eine Anzahl n von Dokumenten als Wissensbasis Embeddings berechnet wurden.
Mit dem Model, mit welchem die Embeddings berechnet wurden, müssen in diesem Skript für alle Prompts, die verwendet werden sollen, ebenfalls die Embeddings berechnet werden.
Der Grund hierfür ist, dass der Rechner, welcher für das LLM und die Embeddings berechnet werden, der selbe ist. Dieser Rechner hat eine RTX 3070 mit 8GB Grafikspeicher, weshalb nicht beide Modelle,
das für das Berechnen der Embeddings und das zweite zur Verarbeitung des Prompts mit dem ermittelten Kontext, gleichzeitig laufen können. 

Die Benennung des Ergebnisses wird folgendermaßen strukturiert:
V** - Versionsbenennung
2025******** - Zeitstempel
al - Amount Languages
ap - Amount Prompts
it - Iterations
temp - temperature for LLM
*** - name of try

Die Ergebnisse sind in der Evaluation nutzbar.