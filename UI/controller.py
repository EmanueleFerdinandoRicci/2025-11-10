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
            self._view._ddStore.options.append(ft.dropdown.Option(s))
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
        self._view.update_page()

    def handleCerca(self, e):
        pass

    def handleRicorsione(self, e):
        pass