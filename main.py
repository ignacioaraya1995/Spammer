import csv
import smtplib
import email.message
from string import Template

class Cliente:
    def __init__(self, comuna, email):
        self.comuna = comuna
        self.email = email
        self.ofertas = []
    
    def __str__(self):
        print("Email: {} \t Comuna: {}".format(self.email, self.comuna))
        print(self.ofertas)
        return "\n"

    def __repr__(self):
        print("Email: {} \t Comuna: {}".format(self.email, self.comuna))
        print(self.ofertas)
        return "\n"

    def chequearOfertas(self):
        if len(self.ofertas) > 0:
            self.existeOferta = True
        else:
            self.existeOferta = False

class Producto:
    def __init__(self, Name,Type,Tags,Published, RealPrice, OriginalPrice,ImageSrc):
        self.name = Name
        self.type = Type
        self.tags = Tags
        self.published = Published
        self.price = RealPrice
        self.originalPrice = OriginalPrice
        self.img = ImageSrc
    
    def __str__(self):
        output = self.name + "\t" + self.type + "\t $" + str(self.price) 
        return output

    def __repr__(self):
        output = self.name + "\t" + self.type + "\t $" + str(self.price) + "\n"
        return output

def crearClientes():
    clientes = []
    with open('clients.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        i = 0
        for row in spamreader:
            if i == 0:
                i +=1
            else:
                clientes.append(Cliente(row[0],row[1]))
    return clientes

def crearProductos():
    productos = []
    with open('products.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in spamreader:
            if i == 0:
                i +=1
            else:
                productos.append( Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    return productos

def verificarProductos(productos):
    output = []
    for p in productos:
        if p.published == "TRUE":
            output.append(p)
    return output

def generarOfertasComuna(clientes, productos):
    for c in clientes:
        for p in productos:
            if c.comuna.lower() in p.tags.lower():
                c.ofertas.append(p)
        c.chequearOfertas()

def startEmailing(clientes):
    server = smtplib.SMTP('smtp.gmail.com:587')
    msg = email.message.Message()
    msg['From'] = 'ccardcl@gmail.com'
    password = "k00969291"

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)

    for c in clientes:

        if len(c.ofertas) >= 2:
            img1 = c.ofertas[0].img
            img2 = c.ofertas[1].img
            title1 = c.ofertas[0].name
            title2 = c.ofertas[1].name
            comuna = c.comuna
            msg['Subject'] = 'Nuevas Pymes en {}!'.format(comuna)
            description1 = "Esta oferta es para ti!, {} es una {} que tiene una giftCard de ${} a solo ${} Aprovecha!".format(title1, c.ofertas[0].type, c.ofertas[0].originalPrice, c.ofertas[0].price)

            description2 = "Esta oferta es para ti!, {} es una {} que tiene una giftCard de ${} a solo ${} Aprovecha!".format(title2, c.ofertas[1].type, c.ofertas[1].originalPrice, c.ofertas[1].price)

            email_content = """
                        <html>
                        
                        <head>
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                            
                        <title>Ccard - Nuevas Pymes!</title>
                        <style type="text/css">
                            a {color: #d80a1e;}
                        body, #header h1, #header h2, p {margin: 0; padding: 0;}
                        #main {border: 1px solid #ffffff;}
                        img {display: block;}
                        #top-message p, #bottom p {color: #3f4042; font-size: 12px; font-family: Arial, Helvetica, sans-serif; }
                        #header h1 {color: #ffffff !important; font-family: "Lucida Grande", sans-serif; font-size: 24px; margin-bottom: 0!important; padding-bottom: 0; }
                        #header p {color: #ffffff !important; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; font-size: 12px;  }
                        h5 {margin: 0 0 0.8em 0;}
                            h5 {font-size: 18px; color: #444444 !important; font-family: Arial, Helvetica, sans-serif; }
                        p {font-size: 12px; color: #444444 !important; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; line-height: 1.5;}
                        </style>
                        </head>
                        
                        <body>
                    
                        <table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4"><tr><td>

                        
                        <table id="main" width="600" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff">
                            <tr>
                            <td>
                                <table id="header" cellpadding="10" cellspacing="0" align="center" bgcolor="8fb3e9">
                                <tr>
                                    <td width="570" align="center"  bgcolor="#d80a3e"><h1><a href = "www.ccard.cl">Nuevas Pymes en Ccard! Visitanos</a></h1></td>
                                </tr>
                                <tr>
                                    <td width="570" align="right" bgcolor="#d80a3e"><p>Marzo 2020</p></td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        
                            <tr>
                            <td>
                                <table id="content-3" cellpadding="0" cellspacing="0" align="center">
                                <tr>
                                    <td width="250" valign="top" bgcolor="d0d0d0" style="padding:5px;">
                                    <img src="$img1" width="250" height="150"  />
                                    </td>
                                    <td width="15"></td>
                                    <td width="250" valign="top" bgcolor="d0d0d0" style="padding:5px;">
                                        <img src="$img2" width ="250" height="150" />
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr>
                            <td>
                                <table id="content-4" cellpadding="0" cellspacing="0" align="center">
                                <tr>
                                    <td width="200" valign="top">
                                    <h5>$title1</h5>
                                    <p>$description1</p>
                                    </td>
                                    <td width="15"></td>
                                    <td width="200" valign="top">
                                    <h5>$title2</h5>
                                    <p>$description2</p>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            
                        
                        </table>
                        <table id="bottom" cellpadding="20" cellspacing="0" width="600" align="center">

                            <tr>
                            <td align="center">
                                <p>Enviado por el Equipo de Ccard!</p>
                                <p><a href="#">Unsubscribe</a> | <a href="#">Compartir en Facebook</a> | <a href="#">View in Browser</a></p>
                            </td>
                            </tr>

                        </table><!-- top message -->
                        </td></tr></table><!-- wrapper -->
                        
                        </body>
                        </html>           
            """
            email_content = Template(email_content).safe_substitute(comuna=comuna, img1=img1, img2=img2, title1= title1, description1=description1,title2=title2,      description2=description2)
            msg['To'] = 'idaraya@uc.cl'
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_content)
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
 
            print("Correo enviado!")







if  __name__ == "__main__":
    clientes = crearClientes()
    productos = crearProductos()
    productos = verificarProductos(productos)
    generarOfertasComuna(clientes, productos)
    i = 0
    startEmailing(clientes)
        