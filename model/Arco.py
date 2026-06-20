from dataclasses import dataclass

from model.order import Order


@dataclass
class Arco:
    o1: Order
    o2: Order
    diff: int
    sommaOggetti: int