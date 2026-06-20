import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMapO = {}
        self._graph = nx.DiGraph()
        self._orders = []

    def getAllStores(self):
        return DAO.getAllStores()

    def getAllNodes(self,store):
        self._orders = DAO.getAllNodes(store)
        return self._orders

    def creaGrafo(self, store, k):
        self._graph.clear()
        self._orders = DAO.getAllNodes(store)
        for o in self._orders:
            self._idMapO[o.order_id] = o
        self._graph.add_nodes_from(self._orders)

        # 1. Recuperi la lista di oggetti Quantita dal DAO
        lista_quantita = DAO.getAllQuantity(self._idMapO)
        # 2. Trasformi la lista in un dizionario {order_id: totale_quantita} per una ricerca fulminea (O(1))
        mappa_quantita = {}
        for q in lista_quantita:
            mappa_quantita[q.order.order_id] = q.totale_quantita

        allEdges = DAO.getAllEdges(store, k, self._idMapO)
        for e in allEdges:
            q1 = mappa_quantita.get(e.o1.order_id, 0)
            q2 = mappa_quantita.get(e.o2.order_id, 0)
            e.sommaOggetti = q1 + q2
            if e.diff != 0:
                peso = e.sommaOggetti / e.diff
                self._graph.add_edge(e.o1, e.o2, weight=peso)
            else:
                pass

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getEdgeGrandi(self):
        edgeGrandi = list(self._graph.edges(data=True))
        edgeGrandi.sort(key=lambda e: e[2]["weight"], reverse=True)
        return edgeGrandi

    def getPath(self,v0):
        path = nx.dag_longest_path(self._graph,v0)
        return path