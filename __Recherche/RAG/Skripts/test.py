import winsound
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

client = chromadb.PersistentClient(
    path=r"__Recherche\RAG\Skripts\chromadb",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)
# Print list of all current names
for collection in client.list_collections():
    print(collection.name)

winsound.PlaySound("*", winsound.SND_ALIAS)