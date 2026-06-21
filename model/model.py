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

    def get_percorso_piu_lungo(self, nodo_partenza):
        """
        Metodo pubblico da chiamare dal Controller.
        """
        self._bestPath = []
        self._bestWeight = -1  # Partiamo da un valore bassissimo

        # Facciamo partire la ricorsione
        self._ricorsione([nodo_partenza], 0)

        return self._bestPath, self._bestWeight

    def _ricorsione(self, parziale, peso_corrente):
        """
        Metodo privato ricorsivo che esegue la DFS con Backtracking.
        """
        # 1. Controlliamo se la soluzione corrente è migliore della best salvata
        if peso_corrente > self._bestWeight:
            self._bestPath = list(parziale)  # IMPORTANTE: facciamo una copia!
            self._bestWeight = peso_corrente

        # 2. Esploriamo i vicini in profondità
        ultimo_nodo = parziale[-1]

        for vicino in self._graph.neighbors(ultimo_nodo):
            # Condizione per evitare i cicli
            if vicino not in parziale:
                # Estraiamo il peso dell'arco
                peso_arco = self._graph[ultimo_nodo][vicino]['weight']

                # Aggiungiamo il vicino al percorso parziale
                parziale.append(vicino)

                # Chiamata ricorsiva avanzando lungo questo ramo
                self._ricorsione(parziale, peso_corrente + peso_arco)

                # BACKTRACKING: torniamo indietro rimuovendo l'ultimo nodo aggiunto
                parziale.pop()

    def get_percorso_decrescente(self, nodo_partenza):
        """
        Metodo pubblico che avvia la ricerca del percorso di peso massimo
        con la regola degli archi strettamente decrescenti.
        """
        self._bestPath = []
        self._bestWeight = -1

        # Facciamo partire la ricorsione.
        # Passiamo float('inf') come "peso dell'ultimo arco" per assicurarci
        # che il primissimo arco scelto sia sicuramente minore di infinito.
        self._ricorsione_decrescente([nodo_partenza], 0, float('inf'))

        return self._bestPath, self._bestWeight

    def _ricorsione_decrescente(self, parziale, peso_totale, peso_ultimo_arco):
        """
        Metodo privato ricorsivo con Backtracking e vincolo di decrescenza.
        """
        # 1. Aggiorniamo la soluzione migliore se troviamo un peso totale maggiore
        if peso_totale > self._bestWeight:
            self._bestPath = list(parziale)
            self._bestWeight = peso_totale

        # 2. Esploriamo i vicini in profondità
        ultimo_nodo = parziale[-1]

        for vicino in self._graph.neighbors(ultimo_nodo):
            # Regola 1: Un vertice può entrare una volta sola nel percorso
            if vicino not in parziale:
                # Estraiamo il peso dell'arco che stiamo valutando
                peso_arco = self._graph[ultimo_nodo][vicino]['weight']

                # Regola 2: Il peso dell'arco deve essere STRETTAMENTE DECRESCENTE
                if peso_arco < peso_ultimo_arco:
                    # Aggiungiamo il vicino al percorso parziale
                    parziale.append(vicino)

                    # Chiamata ricorsiva:
                    # - aggiorniamo il peso totale (+ peso_arco)
                    # - passiamo il peso di questo arco come nuovo "peso_ultimo_arco"
                    self._ricorsione_decrescente(parziale, peso_totale + peso_arco, peso_arco)

                    # BACKTRACKING: rimuoviamo il nodo per esplorare altre strade
                    parziale.pop()