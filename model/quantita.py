from dataclasses import dataclass

from model.order import Order


@dataclass
class Quantita:
    order: Order
    totale_quantita: int