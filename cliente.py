class Cliente:
    def __init__(self, mysql):
        self.mysql = mysql
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()
        
    def consultar(self):
        sql = "SELECT * FROM cliente WHERE activo=1"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        return resultado
    
    def agregar(self, cliente):
        sql = f"INSERT INTO cliente (id,nombre,correo,contraseña,activo)\
            VALUES ('{cliente[0]}','{cliente[1]}','{cliente[2]}','{cliente[3]}',1)"
        self.cursor.execute(sql)
        self.conexion.commit()
        
    def modificar(self, cliente):
        sql = f"UPDATE cliente SET nombre='{cliente[1]}',\
            correo='{cliente[2]}',contraseña='{cliente[3]}'\
                WHERE id='{cliente[0]}'"
        self.cursor.execute(sql)
        self.conexion.commit()
        
    def borrar(self, id):
        sql = f"UPDATE cliente SET activo=0 WHERE id={id}"
        self.cursor.execute(sql)
        self.conexion.commit() 
        
    def buscar(self, id):
        sql = f"SELECT nombre FROM cliente WHERE id={id}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conexion.commit()
        if len(resultado)>0:
            return True
        else:
            return False