import connectionSQL as cs
from  productos import ProductsCGU, ClientsCGU
import load_configuration
import tkinter.messagebox as messagebox
from logger import logger
from typing import List, Tuple, Any
from datetime import datetime

class send:
    def __init__(self):
        super().__init__()
        self.log = logger()
        self.Accestoken1 = ""
        self.configuration = load_configuration.configuration().cargar_configuracion()
        self.connection = cs.SQLServerConnection(self.configuration.server, self.configuration.database, self.configuration.username, self.configuration.password, self.configuration.port)
        self.tabla = []

    def process(self):
        try:
            productos = ProductsCGU()
            self.connection.connect()
            self.veriffy(self.getProducts(), productos.getProductsCGU(self.configuration.endpoint, self.configuration.userws, self.configuration.passws))
            self.connection.disconnect()
            messagebox.showinfo("Proceso terminado", f"Proceso finalizado correctamente.")
        except Exception as e:
            self.log.write_to_log(f"(run_process) - Se produjo un error: {str(e)}")
            messagebox.showerror("Error", f"Se produjo un error, verifique que el archivo este correcto\n\n {str(e)}")

    def processclient(self):
        try:
            clientes = ClientsCGU()
            self.connection.connect()      
            self.veriffyClient(self.getClients(), clientes.getClientsCGU(self.configuration.documento))
            self.connection.disconnect()
            messagebox.showinfo("Proceso terminado", f"Proceso finalizado correctamente.")
        except Exception as e:
            self.log.write_to_log(f"(run_process) - Se produjo un error: {str(e)}")
            messagebox.showerror("Error", f"Se produjo un error, verifique que el archivo este correcto\n\n {str(e)}")

    def getUltimogrupo(self, grupos):
        prioridad_mas_alta = 0
        prioridad_impresion_mas_alta = 0
        ultimo_idgrupo = 0
        if grupos:
            for grupo in grupos:
                prioridad_actual = int(grupo['prioridad'])
                prioridad_impresion_actual = grupo['prioridadimpresion']
                if prioridad_mas_alta is None or prioridad_actual > prioridad_mas_alta:
                    prioridad_mas_alta = prioridad_actual
                if prioridad_impresion_actual != 'None':
                    prioridad_impresion_actual = int(prioridad_impresion_actual)
                    if prioridad_impresion_mas_alta is None or prioridad_impresion_actual > prioridad_impresion_mas_alta:
                        prioridad_impresion_mas_alta = prioridad_impresion_actual
            ultimo_idgrupo = grupos[-1]['idgrupo']
        return [prioridad_mas_alta, prioridad_impresion_mas_alta, ultimo_idgrupo]
    
    def getStation(self):
        #self.connection.connect()
        pyodbc_connection = self.connection.connection
        DataManipulator = cs.SQLServerQueryExecutor(pyodbc_connection)
        select = f"SELECT idestacion FROM estaciones"
        processed_stations = []
        for station in DataManipulator.execute_query(select):
            processed_stations.append(station[0])
        #self.connection.disconnect()
        return processed_stations
    
    def getUnidad(self):
        #self.connection.connect()
        pyodbc_connection = self.connection.connection
        DataManipulator = cs.SQLServerQueryExecutor(pyodbc_connection)
        select = f"SELECT idunidad FROM udsmedida"
        unidades_medida = []
        for unidad in DataManipulator.execute_query(select):
            unidades_medida.append(unidad[0])
        #self.connection.disconnect()
        return unidades_medida
    
    def getAreaRest(self):
        #self.connection.connect()
        pyodbc_connection = self.connection.connection
        DataManipulator = cs.SQLServerQueryExecutor(pyodbc_connection)
        select = f"SELECT idarearestaurant FROM areasrestaurant"
        areas = []
        for area in DataManipulator.execute_query(select):
            areas.append(area[0])
        #self.connection.disconnect()
        return areas
    
    def getGroup(self):
        try:
            #self.connection.connect()
            pyodbc_connection = self.connection.connection
            DataManipulator = cs.SQLServerQueryExecutor(pyodbc_connection)
            select = f"SELECT idgrupo, descripcion, prioridad, prioridadimpresion FROM grupos"
            processed_group = {}
            for group in DataManipulator.execute_query(select):
                processed_group[group[1]] = {
                    "idgrupo" : group[0],
                    "descripcion" : group[1],
                    "prioridad" : str(group[2]),
                    "prioridadimpresion" : str(group[3])
                }
            processed_group = sorted(processed_group.values(), key=lambda x: x["idgrupo"])
            #self.connection.disconnect()
        except Exception as e:
            self.log.write_to_log(f"Error al obtener los grupos: {e}")
        return processed_group
    
    def getProducts(self):
        try:
            #self.connection.connect()
            pyodbc_connection = self.connection.connection
            DataManipulator = cs.SQLServerQueryExecutor(pyodbc_connection)
            select = f"SELECT p.idproducto, p.descripcion, pd.impuesto1, pd.idunidad, pd.preciosinimpuestos, pd.precio FROM productos p INNER JOIN productosdetalle pd ON p.idproducto = pd.idproducto ORDER BY p.idproducto"
            processed_products = {}
            productos = DataManipulator.execute_query(select)
            for product in productos:
                processed_products[product[0]] = {
                    "idproducto" : product[0],
                    "descripcion" : product[1],
                    "impuesto1" : str(product[2]),
                    "idunidad" : str(product[3]),
                    "preciosinimpuestos" : str(product[4]),
                    "precio" : str(product[5])
                }
            processed_products = sorted(processed_products.values(), key=lambda x: x["idproducto"])
            #self.connection.disconnect()
        except Exception as e:
            self.log.write_to_log(f"Error al obtener los grupos: {e}")
        
        return processed_products
    
    def getClients(self):
        try:
            #self.connection.connect()
            pyodbc_connection = self.connection.connection
            DataManipulator = cs.SQLServerQueryExecutor(pyodbc_connection)
            select = f"SELECT idcliente, nombre, curp FROM clientes"
            processed_clients = []
            for client in DataManipulator.execute_query(select):
                processed_clients.append({
                    "idcliente" : client[0],
                    "nombre" : client[1],
                    "cedula" : client[2],
                })
            #processed_clients = sorted(processed_clients.values(), key=lambda x: x["nombre"])
            #print(processed_clients)
            #self.connection.disconnect()
        except Exception as e:
            self.log.write_to_log(f"Error al obtener los grupos: {e}")
        return processed_clients
    
    def veriffy(self, productos, exceldata):
        try:
            for a, b in exceldata.items():
                for c, d in b['productos'].items():
                    grupos = self.getGroup()

                    #PARA VOLVER A QUE SEAN LOS GRUPOS QUE ELLOS MANDAN HAY QUE CAMBIAR "NUEVOS" POR a

                    if not any(e['idproducto'] == d['idproducto'] for e in productos):    # No existe el producto.
                        idgrupo = None
                        if not any(f['descripcion'] == "NUEVOS" for f in grupos):      # No existe el grupo del producto a crear.
                            idgrupo = self.creategroup(grupos, "NUEVOS")
                        else:                                                   # Existe el grupo del producto a crear.
                            print("Existe el grupo")
                            idgrupo = [item['idgrupo'] for item in grupos if item['descripcion'] == "NUEVOS"][0]
                        print(f"voy a crear {d['idproducto']}")
                        self.createproduct(d['unidad'], d['idproducto'], d['descripcion'][:60], idgrupo, d['precio_iva_inc'], d['iva'], d['precio_sin_iva'], d['plu'])
                    else:                                               # Existe el producto.
                        idgrupo = None
                        if not any(f['descripcion'] == "NUEVOS" for f in grupos):      # No existe el grupo del producto a crear.
                            idgrupo = self.creategroup(grupos, "NUEVOS")
                        else:                                                   # Existe el grupo del producto a crear.
                            idgrupo = [item['idgrupo'] for item in grupos if item['descripcion'] == "NUEVOS"][0]
                        self.modifyproduct(idgrupo, d['unidad'], d['descripcion'][:60], "NUEVOS", d['precio_iva_inc'], d['iva'], d['precio_sin_iva'], d['idproducto'], d['plu'])
        except Exception as e:
            self.log.write_to_log(f"(veriffy) - Se produjo un error: {str(e)}")
            messagebox.showerror("Error", f"veriffy - Se produjo un error: {str(e)}")

    def creategroup(self, grupos, grupo_crear):
        [prioridad_mas_alta, prioridad_impresion_mas_alta, ultimo_idgrupo] = self.getUltimogrupo(grupos)
        ultimo_idgrupo = int(ultimo_idgrupo) + 1
        if ultimo_idgrupo < 10: ultimo_idgrupo = "0"+str(ultimo_idgrupo)
        prioridad_mas_alta = int(prioridad_mas_alta) + 1
        prioridad_impresion_mas_alta = int(prioridad_impresion_mas_alta) + 1
        estaciones = self.getStation()

        #self.connection.connect()
        pyodbc_connection = self.connection.connection
        DataManipulator = cs.SQLServerDataManipulator(pyodbc_connection)
        DataManipulator.insert(f"INSERT INTO grupos (idgrupo,descripcion, prioridad, prioridadimpresion, imagenmenuelectronico,clasificacion,COLOR,colorletra,cambiacolorcuenta,colorcuenta,colorletracuenta,solicitaautorizacion) VALUES  ('{ultimo_idgrupo}', '{grupo_crear}', '{prioridad_mas_alta}', '{prioridad_impresion_mas_alta}', null,1,4235005,0,0,13160660,0,0)")
        DataManipulator.insert(f"insert into WorkspaceControl (IdSoftrestaurant,Type,ForSync,DateCreate,IsDelete) values ('{ultimo_idgrupo}','Grupo','1',getdate(),'0')")
        for e in estaciones:
            DataManipulator.insert(f"INSERT INTO gruposdeproductosvisibles (idestacion,idgrupo,VISIBLE,visiblesiempre,lunesinicio,lunesfin,lunesdiafin,martesinicio,martesfin,martesdiafin,miercolesinicio,miercolesfin,miercolesdiafin,juevesinicio,juevesfin,juevesdiafin,viernesinicio,viernesfin,viernesdiafin,sabadoinicio,sabadofin,sabadodiafin,domingoinicio,domingofin,domingodiafin,aplicalunes,aplicamartes,aplicamiercoles,aplicajueves,aplicaviernes,aplicasabado,aplicadomingo) VALUES  ('{e}', '{ultimo_idgrupo}',1,1,'12:00:00 AM','11:59:59 PM',1,'12:00:00 AM','11:59:59 PM',1,'12:00:00 AM','11:59:59 PM',1,'12:00:00 AM','11:59:59 PM',1,'12:00:00 AM','11:59:59 PM',1,'12:00:00 AM','11:59:59 PM',1,'12:00:00 AM','11:59:59 PM',1,0,0,0,0,0,0,0)")
        #self.connection.disconnect()
        return ultimo_idgrupo

    def createproduct(self, unidad, idproducto, descripcion, idgrupo, ivainc, iva, siniva, plu):
        unidad_medida = self.getUnidad()
        unidades_media_excel = []
        #self.connection.connect()
        pyodbc_connection = self.connection.connection
        DataManipulator = cs.SQLServerDataManipulator(pyodbc_connection)
        if unidad not in unidades_media_excel:
            unidades_media_excel.append(unidad)
            if unidad not in unidad_medida:
                DataManipulator.insert(f"INSERT INTO udsmedida (idunidad,idunidadmedida_SAT) VALUES ('{unidad}', '{unidad[:3]}')")
        DataManipulator.insert(f"INSERT INTO productos (idproducto,descripcion,idgrupo,nombrecorto,plu,imagen,imagenmenuelectronico,nofacturable,comentario,usarcomedor,usardomicilio,usarrapido,usarcedis,idinsumospresentaciones,usarmenuelectronico,imagenme_modified) VALUES ('{idproducto}','{descripcion}','{idgrupo}','','{plu}','',null,0.000000,'',1,1,1,0,null,0,0)")
        DataManipulator.insert(f"INSERT INTO productosdetalle (idproducto,idempresa,precio,impuesto1,impuesto2,impuesto3,preciosinimpuestos,bloqueado,precioabierto,lunesinicio,lunesfin,aplicalunes,martesinicio,martesfin,aplicamartes,miercolesinicio,miercolesfin,aplicamiercoles,juevesinicio,juevesfin,aplicajueves,viernesinicio,viernesfin,aplicaviernes,sabadoinicio,sabadofin,aplicasabado,domingoinicio,domingofin,aplicadomingo,preciolunes,preciomartes,preciomiercoles,preciojueves,precioviernes,preciosabado,preciodomingo,lunesdiasalida,martesdiasalida,miercolesdiasalida,juevesdiasalida,viernesdiasalida,sabadodiasalida,domingodiasalida,secuenciacompuesto,finalizarsecuenciacompuesto,heredarmonitormodificadores,comisionvendedor,excentoimpuestos,enviarproduccionsimodificador,cargoadicional,afectacomensales,comensalesafectados,rentabilidadcedis,usarmultiplicadorprodcomp,idarea,descargar,permitirprodcompenmodif,politicapuntos,favorito,idunidad,ocultarmitades,usa_imagen_monitor,rutaimagen,comisionprecio) VALUES ('{idproducto}','0000000001',{ivainc},{iva},0.000000,0.000000,{siniva},0.000000,2.000000,'12:00:00 AM','11:59:59 PM',0.000000,'12:00:00 AM','11:59:59 PM',0.000000,'12:00:00 AM','11:59:59 PM',0.000000,'12:00:00 AM','11:59:59 PM',0.000000,'12:00:00 AM','11:59:59 PM',0.000000,'12:00:00 AM','11:59:59 PM',0.000000,'12:00:00 AM','11:59:59 PM',0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,1.000000,1.000000,1.000000,1.000000,1.000000,1.000000,1.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0,0,0,0.000000,0.000000,'',1,0,1,0.000000,'{unidad}',0.000000,0,'',0.000000)")
        DataManipulator.insert(f"insert into WorkspaceControl (IdSoftrestaurant,Type,ForSync,DateCreate,IsDelete) values ('{idproducto}','Productos','1',getdate(),'0')")
        for a in self.getAreaRest():
            DataManipulator.insert(f"INSERT INTO productosmonedero (IDPRODUCTO,IDAREARESTAURANT,IDEMPRESA,ACTIVO,LUNESAPLICA,LUNESINICIO,LUNESFIN,LUNESDIASALIDA,MARTESAPLICA,MARTESINICIO,MARTESFIN,MARTESDIASALIDA,MIERCOLESAPLICA,MIERCOLESINICIO,MIERCOLESFIN,MIERCOLESDIASALIDA,JUEVESAPLICA,JUEVESINICIO,JUEVESFIN,JUEVESDIASALIDA,VIERNESAPLICA,VIERNESINICIO,VIERNESFIN,VIERNESDIASALIDA,SABADOAPLICA,SABADOINICIO,SABADOFIN,SABADODIASALIDA,DOMINGOAPLICA,DOMINGOINICIO,DOMINGOFIN,DOMINGODIASALIDA,PORCENTAJE,MULTIPLO,PUNTOSMULTIPLO) VALUES ('{idproducto}','{a}','0000000001',0,0,'12:00:00 AM','11:59:59 PM',1.000000,0,'12:00:00 AM','11:59:59 PM',1.000000,0,'12:00:00 AM','11:59:59 PM',1.000000,0,'12:00:00 AM','11:59:59 PM',1.000000,0,'12:00:00 AM','11:59:59 PM',1.000000,0,'12:00:00 AM','11:59:59 PM',1.000000,0,'12:00:00 AM','11:59:59 PM',1.000000,0.000000,0.000000,0.000000)")
        #self.connection.disconnect()

    def modifyproduct(self, idgrupo, unidad, descripcion, grupo, ivainc, iva, siniva, idproducto, plu):
        #self.connection.connect()
        pyodbc_connection = self.connection.connection
        DataManipulator = cs.SQLServerQueryExecutor(pyodbc_connection)
        for p in DataManipulator.execute_query(f"SELECT g.descripcion, p.idproducto, p.descripcion, CAST(pd.impuesto1 AS INT), pd.idunidad, CAST(ROUND(pd.preciosinimpuestos, 2, 1) AS FLOAT), CAST(ROUND(pd.precio, 2, 1) AS FLOAT), p.plu FROM productos p INNER JOIN grupos g ON p.idgrupo = g.idgrupo INNER JOIN productosdetalle pd ON p.idproducto = pd.idproducto WHERE p.idproducto = '{idproducto}'"):
            if  descripcion != p[2] or iva != str(p[3]) or unidad != p[4] or siniva != p[5] or float(ivainc) != p[6] or plu != p[7]:
                '''grupo != p[0] or''' #Esto se agrega al if en caso de querer utilizar los grupos que ellos mandan
                DataManipulator1 = cs.SQLServerDataManipulator(pyodbc_connection)
                DataManipulator1.update(f"UPDATE productos SET descripcion = '{descripcion}', plu = '{plu}' WHERE idproducto = '{idproducto}'")
                DataManipulator1.update(f"UPDATE productosdetalle SET precio = {str(float(ivainc))}, impuesto1 = {iva}, preciosinimpuestos = {siniva}, idunidad = '{unidad}' WHERE idproducto = '{idproducto}'")
        #self.connection.disconnect()

    def veriffyClient(self, clientes, exceldata):
        try:
            #print(len(exceldata))
            for p in exceldata:
                #print(f"Voy a buscar {p['cedula']} - {p['nombre']}")
                clienteFind = next((cliente for cliente in clientes if cliente["cedula"] == p["cedula"]), None)
                #print(f"Lo encontré {clienteFind}") if clienteFind else print(f"No lo encontré {clienteFind}")
                if not clienteFind is None:
                    #print(f"Existe este cliente {clienteFind['idcliente']} que es: {p} - HAY QUE IR A VER SI SE MODIFICO ALGUN DATO")
                    if clienteFind['nombre'] != p['nombre']:
                        #print(f"Edito cliente: {clienteFind['idcliente']} - {clienteFind['nombre']} - {p['nombre']}")
                        self.editClient(p)
                else:
                    self.createClient(p)
        except Exception as e:
            self.log.write_to_log(f"(veriffyClient) - Se produjo un error: {str(e)}")
            #messagebox.showerror("Error", f"veriffyClient - Se produjo un error: {str(e)}")

    def createClient(self, cliente):
        try:
            descuento = ""
            if self.configuration.descuento:
                descuento = self.configuration.descuento

            pyodbc_connection = self.connection.connection
            DataManipulator = cs.SQLServerDataManipulator(pyodbc_connection)  
            DataManipulator.insert(f"INSERT INTO clientes (idcliente,nombre,direccion,poblacion,email,rfc,cumpleaños,limitedecredito,descuento,codigopostal,notas,foliofiscal,idtipodescuento,pais,estado,curp,limitecreditodiario,tipofacturacion,procesadoweb,nocobrarimpuestos,tipocredito,giro,idtipocliente,idtipomenu,contacto,tarjetamonedero, telefono1,telefono2,telefono3,telefono4,telefono5,dias_vigencia_credito,retenerimpuesto,tipocuenta,tipoclientencf ,descuentoprimeraventacomedoremp,contemplarpropina,status) VALUES ('{cliente['cedula']}','{cliente['nombre']}','','','','','',0.000000,0.000000,'','','','{descuento}','URUGUAY','','{cliente['cedula']}',0.000000,1.000000,0,0,1.000000,'','','', '{cliente['nombre']}','' , '', '','', '','',0.000000,0,1.000000,0.000000,0.000000,0,1)")
            
            return True
        except Exception as e:
            self.log.write_to_log(f"(createClient) - Se produjo un error: {str(e)}")
            messagebox.showerror("Error", f"createClient - Se produjo un error: {str(e)}")

    def editClient(self, cliente):
        try:
            pyodbc_connection = self.connection.connection
            DataManipulator = cs.SQLServerDataManipulator(pyodbc_connection)
            DataManipulator.update(f"UPDATE clientes SET nombre = '{cliente['nombre']}' WHERE idcliente = '{cliente['cedula']}'")
            return True
        except Exception as e:
            self.log.write_to_log(f"(editClient) - Se produjo un error: {str(e)}")
            messagebox.showerror("Error", f"editClient - Se produjo un error: {str(e)}")

class utils:
    def charactervalidator(self, str, ch, rplc):
        if ch in str:
            str = str.replace(ch, rplc)
        return str