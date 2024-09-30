from typing import Any
from dataaccess.db import dbsqlite
from datetime import date, datetime

class BaseClass:
    def __init__(self, *args: Any, **kwds: Any):
        self.apiEvento = False
        self.retorno = 0
        self._message = ''
        self.data = {}

    def to_dict(self):
        return {
            'apiEvento': self.apiEvento,
            'retorno': self.retorno,
            '_message': self._message,
            'data': self.data
        }

class Evento(BaseClass):
    def __init__(self, id: str, evento: int, entrega: str, tipo: int, data: date, hora: str):
        super().__init__()
        self.apiEvento = True
        self.retorno = 0
        self._message = 'Ok'
        self.data = {
            'id': id,
            'evento': evento,
            'entrega': entrega,
            'tipo': tipo,
            'data': data,
            'hora': hora
        }

    def to_dict(self):
        return {
            'apiEvento': self.apiEvento,
            'retorno': self.retorno,
            '_message': self._message,
            'data': {
                'id': self.data['id'],
                'evento': self.data['evento'],
                'entrega': self.data['entrega'],
                'tipo': self.data['tipo'],
                'data': self.data['data'],
                'hora': self.data['hora']
            }
        }

def getEventos() -> dict:
    SQL = dbsqlite()
    SQL.cur.execute("SELECT id, evento, entrega, tipo, data, hora FROM Eventos")
    records = SQL.cur.fetchall()
    eventos = []

    for r in records:
        evento = Evento(r[0], r[1], r[2], r[3], r[4], r[5])
        eventos.append(evento.to_dict())

    SQL.cur.close()

    if not eventos:
        result = Evento('', 0, '', 0, date.today(), datetime.now().strftime('%H:%M'))
        result.apiEvento = True
        result.retorno = 1
        result._message = 'Nenhum registro encontrado'
        return result.to_dict()
    else:
        return eventos

def getEvento(id: str) -> dict:
    SQL = dbsqlite()
    SQL.cur.execute(f"SELECT id, evento, entrega, tipo, data, hora FROM Eventos WHERE entrega = '{id}'")
    records = SQL.cur.fetchall()
    eventos = []

    for r in records:
        evento = Evento(r[0], r[1], r[2], r[3], r[4], r[5])
        eventos.append(evento.to_dict())

    SQL.cur.close()

    if not eventos:
        result = Evento('', 0, '', 0, date.today(), datetime.now().strftime('%H:%M'))
        result.apiEvento = False
        result.retorno = 1
        result._message = 'Nenhum registro encontrado'
        return result.to_dict()
    else:
        return eventos
    
def getEventoevento(id: int) -> dict:
    SQL = dbsqlite()
    SQL.cur.execute(f"SELECT id, evento, entrega, tipo, data, hora FROM Eventos WHERE evento = '{id}'")
    records = SQL.cur.fetchall()
    eventos = []

    for r in records:
        evento = Evento(r[0], r[1], r[2], r[3], r[4], r[5])
        eventos.append(evento.to_dict())

    SQL.cur.close()

    if not eventos:
        result = Evento('', 0, '', 0, date.today(), datetime.now().strftime('%H:%M'))
        result.apiEvento = False
        result.retorno = 1
        result._message = 'Nenhum registro encontrado'
        return result.to_dict()
    else:
        return eventos
    
def getEventoEntrega(id: str) -> dict:
    SQL = dbsqlite()
    SQL.cur.execute(f"""                        
                    SELECT 
                            ev.id, 
                            ev.evento, 
                            ev.entrega, 
                            ev.tipo, 
                            ev.data, 
                            ev.hora,
                            et.Entrega 
                        FROM 
                            Eventos as ev
                        LEFT JOIN Entregas as et ON ev.id = et.Id
                        WHERE ev.entrega = ?""", (id,))
    
    records = SQL.cur.fetchall()
    eventos = []

    for r in records:
        evento = Evento(r[0], r[1], r[2], r[3], r[4], r[5])
        eventos.append(evento.to_dict())

    SQL.cur.close()

    if not eventos:
        result = Evento('', 0, '', 0, date.today(), datetime.now().strftime('%H:%M'))
        result.apiEvento = False
        result.retorno = 1
        result._message = 'Nenhum registro encontrado'
        return result.to_dict()
    else:
        return eventos

def postEvento(evento: Evento) -> dict:
    SQL = dbsqlite()

    SQL.cur.execute("SELECT * FROM Eventos WHERE entrega = ? AND tipo = ?", (evento.data['entrega'], evento.data['tipo']))
    result_tipo = SQL.cur.fetchone()

    result = Evento('', 0, '', 0, date.today(), datetime.now().strftime('%H:%M'))

    if result_tipo:
        result.apiEvento = True
        result.retorno = 2
        result._message = u'Tipo já cadastrado'
    else:
        SQL.cur.execute("SELECT COUNT(*) FROM Eventos")
        count = SQL.cur.fetchone()[0]

        current_year = str(datetime.today().year)
        current_day = str(datetime.today().day)

        if count == 0:
            new_code = 1
        else:
            SQL.cur.execute("SELECT MAX(id) FROM Eventos")
            last_id = SQL.cur.fetchone()[0]

            last_id_parts = last_id.split('-') if '-' in last_id else []
        
            if len(last_id_parts) == 3:
                last_code = int(last_id_parts[2])
            else:
                last_code = 0
            
            new_code = last_code + 1

        new_id = f"EV{current_year}{current_day}{new_code}"

        while True:
            SQL.cur.execute("SELECT COUNT(*) FROM Eventos WHERE id = ?", (new_id,))
            if SQL.cur.fetchone()[0] == 0:
                break
            new_code += 1
            new_id = f"EV{current_year}{current_day}{new_code}"

        SQL.cur.execute("INSERT INTO Eventos (id, evento, entrega, tipo, data, hora) VALUES (?, ?, ?, ?, ?, ?)",
                        (new_id, evento.data['evento'], evento.data['entrega'],
                         evento.data['tipo'], evento.data['data'], evento.data['hora']))
        SQL.con.commit()
        SQL.close_db_connection()

        result = evento
       
    return result.to_dict()

def updateEvento(id: str, evento: Evento) -> dict:
    SQL = dbsqlite()
    SQL.cur.execute("UPDATE Eventos SET tipo = ?, data = ?, hora = ? WHERE entrega = ?",
                    (evento.data['tipo'], evento.data['data'], evento.data['hora'], id))
    SQL.con.commit()
    SQL.close_db_connection()

    return evento.to_dict()

def updateEventoEntrega(id: str, evento: Evento) -> dict:
    SQL = dbsqlite()
    SQL.cur.execute("UPDATE Eventos SET tipo = ?, data = ?, hora = ? WHERE id = ?",
                    (evento.data['tipo'], evento.data['data'], evento.data['hora'], id))
    SQL.con.commit()
    SQL.close_db_connection()

    return evento.to_dict()

