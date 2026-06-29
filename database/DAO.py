from database.DB_connect import DBConnect
from model.Arco import Arco
from model.order import Order
from model.quantita import Quantita

from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(store):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select o.*
                    from orders o, stores s 
                    where o.store_id = s.store_id and s.store_id = %s"""

        cursor.execute(query, (store,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(store, k, idMapO):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select o1.order_id as id1, o2.order_id as id2, o1.order_date as od1, o2.order_date as od2, abs(DATEDIFF(o1.order_date,o2.order_date)) as diff
                    from (select o.*
                    from orders o, stores s 
                    where o.store_id = s.store_id and s.store_id = %s) o1,
                    (select o.*
                    from orders o, stores s 
                    where o.store_id = s.store_id and s.store_id = %s) o2
                    where o1.order_id != o2.order_id and abs(DATEDIFF(o1.order_date,o2.order_date)) <= %s and o1.order_date < o2.order_date """

        cursor.execute(query, (store,store,k,))

        for row in cursor:
            results.append(Arco(
                idMapO[row["id1"]],
                idMapO[row["id2"]],
                row["diff"],
                0
            ))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllQuantity(idMapO):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT o.order_id as id, SUM(oi.quantity) AS totale_quantita
                    FROM orders o, order_items oi 
                    WHERE o.order_id = oi.order_id
                    GROUP BY o.order_id
                    ORDER BY o.order_id"""

        cursor.execute(query, )

        for row in cursor:
            if row["id"] in idMapO:
                results.append(Quantita(idMapO[row["id"]], row["totale_quantita"]))

        cursor.close()
        conn.close()
        return results