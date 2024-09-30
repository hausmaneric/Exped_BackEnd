from typing import Any
from dataaccess.db import dbsqlite
from datetime import date

class BaseClass:
    def __init__(self, *args: Any, **kwds: Any):
        self.apiEntrega = False
        self.retorno = 0
        self._message = ''
        self.data = {}

    def to_dict(self):
        return {
            'apiEntrega': self.apiEntrega,
            'retorno': self.retorno,
            '_message': self._message,
            'data': self.data
        }

class Entrega(BaseClass):
    def __init__(self, id: str, cnpj: str, venda: int, entrega: int, status: int, previsao: date):
        super().__init__()
        self.apiEntrega = True
        self.retorno = 0
        self._message = 'Ok'
        self.data = {
            'id': id,
            'cnpj': cnpj,
            'venda': venda,
            'entrega': entrega,
            'status': status,
            'previsao': previsao,
        }

    def to_dict(self):
        return {
            'apiEntrega': self.apiEntrega,
            'retorno': self.retorno,
            '_message': self._message,
            'data': {
                'id': self.data['id'],
                'cnpj': self.data['cnpj'],
                'venda': self.data['venda'],
                'entrega': self.data['entrega'],
                'status': self.data['status'],
                'previsao': self.data['previsao'],
            }
        }

def getEntregas() -> dict:
    SQL = dbsqlite()
    SQL.cur.execute("SELECT id, cnpj, venda, entrega, status, previsao FROM Entregas")
    records = SQL.cur.fetchall()
    _list = []

    for r in records:
        _entrega = Entrega(r[0], r[1], r[2], r[3], r[4], r[5])
        _list.append(_entrega.to_dict())

    SQL.cur.close()

    if not _list:
        result = Entrega('', '', 0, 0, 0, date.today())
        result.apiEntrega = True
        result.retorno = 1
        result._message = 'Nenhum registro encontrado'
        return result.to_dict()
    else:
        return _list

def getEntrega(id: str) -> dict:
    SQL = dbsqlite()
    SQL.cur.execute(f"SELECT id, cnpj, venda, entrega, status, previsao FROM entregas WHERE id = '{id}'")
    records = SQL.cur.fetchall()
    _list = []

    for r in records:
        _entrega = Entrega(r[0], r[1], r[2], r[3], r[4], r[5])
        _list.append(_entrega.to_dict())

    SQL.cur.close()

    if not _list:
        result = Entrega('', '', 0, 0, 0, date.today())
        result.apiEntrega = False
        result.retorno = 1
        result._message = 'Nenhum registro encontrado'
        return result.to_dict()
    else:
        return _list

def getEntregaToken(token: str):
    SQL = dbsqlite()
    SQL.cur.execute(f"SELECT id, cnpj, venda, entrega, status, previsao FROM entregas WHERE SUBSTR(cnpj, 1, 8) || CAST(venda AS TEXT) LIKE '{token}'")
    records = SQL.cur.fetchall()
    _list = []

    for r in records:
        _entrega = Entrega(r[0], r[1], r[2], r[3], r[4], r[5])
        _list.append(_entrega.to_dict())

    SQL.cur.close()

    if not _list:
        result = Entrega('', '', 0, 0, 0, date.today())
        result.apiEntrega = False
        result.retorno = 1
        result._message = 'Nenhum registro encontrado'
        return result.to_dict()
    else:
        return _list

def postEntrega(entrega: Entrega) -> dict:
    SQL = dbsqlite()

    SQL.cur.execute("SELECT * FROM entregas WHERE id = ?", (entrega.data['id'],))
    result_id = SQL.cur.fetchone()

    SQL.cur.execute("SELECT * FROM entregas WHERE cnpj = ? AND entrega = ?", (entrega.data['cnpj'], entrega.data['entrega']))
    result_entrega = SQL.cur.fetchone()

    result = Entrega('', '', 0, 0, 0, date.today())

    if result_id:
        result.apiEntrega = True
        result.retorno = 1
        result._message = u'id já cadastrado'
    elif result_entrega:
        result.apiEntrega = True
        result.retorno = 2
        result._message = u'Entrega já cadastrada'
    else:
        SQL.cur.execute("INSERT INTO Entregas (Id, Cnpj, Venda, Entrega, Status, Previsao) VALUES (?, ?, ?, ?, ?, ?)", (entrega.data['id'], entrega.data['cnpj'], entrega.data['venda'], entrega.data['entrega'], entrega.data['status'], entrega.data['previsao']))
        SQL.con.commit()
        SQL.close_db_connection()

        result = Entrega(entrega.data['id'], entrega.data['cnpj'], entrega.data['venda'], entrega.data['entrega'], entrega.data['status'], entrega.data['previsao'])

    return result.to_dict()

def updateEntrega(id: str, entrega: Entrega):
    SQL = dbsqlite()
    
    SQL.cur.execute("SELECT * FROM entregas WHERE id = ?", (id,))
    result_id = SQL.cur.fetchone()
    
    result = Entrega('', '', 0, 0, 0, date.today())
    
    if result_id is None:
        result.apiEntrega = True
        result.retorno = 1
        result._message = u'Id não localizado'
    else:    
        SQL.cur.execute("UPDATE Entregas SET previsao = ? WHERE id = ?", (entrega.data['previsao'], id))
        SQL.con.commit()
        SQL.close_db_connection()

        result = Entrega(entrega.data['id'], entrega.data['cnpj'], entrega.data['venda'], entrega.data['entrega'], entrega.data['status'], entrega.data['previsao'])
    
    return result.to_dict()
