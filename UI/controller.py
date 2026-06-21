import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStores(self):
        stores = self._model.getAllStores()
        for s in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(key=str(s.store_id), text=s.store_name))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        if self._view._ddStore.value is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona uno store!"))
            self._view.update_page()
            return
        if self._view._txtIntK.value == "":
            self._view.txt_result.controls.append(ft.Text("Inserisci un valore per K!"))
            self._view.update_page()
            return
        store_id = self._view._ddStore.value
        k = int(self._view._txtIntK.value)
        self._model.creaGrafo(store_id, k)
        n_nodi, n_archi = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato. Il grafo contiene {n_nodi} nodi e {n_archi} archi")
        )
        edges = self._model.getEdgeGrandi()
        count = 0
        self._view.txt_result.controls.append(ft.Text(f"Archi di peso maggiore:"))
        for e in edges:
            if count < 5:
                self._view.txt_result.controls.append(
                    ft.Text(f"{e[0]} --> {e[1]}: {e[2]["weight"]}")
                )
                count += 1
        self._view._btnCerca.disabled = False
        self._view._ddNode.disabled = False
        nodes = self._model.getAllNodes(store_id)
        for n in nodes:
            self._view._ddNode.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def handleCerca(self, e):
        node_str = self._view._ddNode.value
        if node_str is None:
            self._view.txt_result.controls.append(ft.Text("Attenzione: seleziona un nodo dalla tendina!"))
            self._view.update_page()
            return

        # 2. Recupero l'oggetto nodo corrispondente alla stringa selezionata
        nodo_partenza = None
        for n in self._model._graph.nodes:
            if str(n) == node_str:
                nodo_partenza = n
                break

        if nodo_partenza is None:
            self._view.txt_result.controls.append(ft.Text("Errore: nodo non trovato nel grafo!"))
            self._view.update_page()
            return

        # 3. Chiamo il metodo del modello
        percorso, peso = self._model.get_percorso_piu_lungo(nodo_partenza)

        # 4. Pulisco e stampo i risultati nella view
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ricerca Percorso Massimo completata!", color="green", weight="bold")
        )
        self._view.txt_result.controls.append(ft.Text(f"Peso totale del percorso: {peso}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi visitati: {len(percorso)}"))
        self._view.txt_result.controls.append(ft.Text("Nodi del percorso:"))

        for n in percorso:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))

        # 5. Abilito il bottone per la seconda ricorsione
        self._view._btnRicorsione.disabled = False
        self._view.update_page()

    def handleRicorsione(self, e):
        node_str = self._view._ddNode.value
        if node_str is None:
            self._view.txt_result.controls.append(ft.Text("Attenzione: seleziona un nodo dalla tendina!"))
            self._view.update_page()
            return

        # 2. Recupero oggetto nodo (stessa logica di prima)
        nodo_partenza = None
        for n in self._model._graph.nodes:
            if str(n) == node_str:
                nodo_partenza = n
                break

        if nodo_partenza is None:
            self._view.txt_result.controls.append(ft.Text("Errore: nodo non trovato nel grafo!"))
            self._view.update_page()
            return

        # 3. Chiamo il metodo del modello per la ricorsione con pesi decrescenti
        percorso, peso = self._model.get_percorso_decrescente(nodo_partenza)

        # 4. Stampo i risultati nella view
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ricerca Percorso Decrescente completata!", color="red", weight="bold")
        )
        self._view.txt_result.controls.append(ft.Text(f"Peso totale: {peso}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {len(percorso)}"))

        self._view.txt_result.controls.append(ft.Text("Cammino: "))
        for n in percorso:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))

        self._view.update_page()