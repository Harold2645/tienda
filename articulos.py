from datetime import datetime
import os


class Articulos:
    def __init__(self, empresa_app,mysql):
        self.empresa_app = empresa_app
        self.mysql = mysql
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()

    def consultar(self):
        sql = "SELECT * FROM articulo WHERE activo=1"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        return resultado

    def agregar(self, articulo):
        print(articulo[4])
        sql = f"INSERT INTO articulo (ida,nombrea,precio,saldo,foto,activo) \
        VALUES ('{articulo[0]}','{articulo[1]}',{articulo[2]},{articulo[3]},\
            '{articulo[4]}',1)"
        self.cursor.execute(sql)
        self.conexion.commit()
    
    def modificar(self, articulo):
        sql = f"UPDATE articulo SET nombrea='{articulo[1]}',\
            precio={articulo[2]},saldo={articulo[3]} WHERE ida='{articulo[0]}'"
        self.cursor.execute(sql)
        self.conexion.commit()
        if articulo[4].filename != '':
            sql=f"SELECT foto FROM articulo WHERE ida='{articulo[0]}'"
            self.cursor.execute(sql)
            resultado=self.cursor.fetchall()
            self.conexion.commit()
            os.remove(os.path.join(self.empresa_app.config['CARPETAUP'],resultado[0][0]))
            ahora = datetime.now()
            tiempo = ahora.strftime("%Y%m%d%H%M%S")
            nom,ext = os.path.splitext(articulo[4].filename)
            nombreFoto = "A"+tiempo+ext
            articulo[4].save("uploads/"+nombreFoto)
            sql=f"UPDATE articulo SET foto='{nombreFoto}'"
            self.cursor.execute(sql)
            self.conexion.commit()

        
    def borrar(self, ida):
        sql = f"UPDATE articulo SET activo=0 WHERE ida={ida}"
        self.cursor.execute(sql)
        self.conexion.commit()
    
    def buscar(self,ida):
        sql = f"SELECT * FROM articulo WHERE ida={ida}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        return resultado