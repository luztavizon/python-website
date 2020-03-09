from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#inicializamos flask y pasamos el nombre a una 
#variable (objeto) que llamaremos app para poder crear rutas
app=Flask(__name__)
#configuramos el sqlalchemy para la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vintage.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)

class Frames(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    Material=db.Column(db.Text,nullable=False)
    Author=db.Column(db.String(20),nullable=True,default='Desconocido')
    Date_posted=db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
#la funcion nos permitira obtener los atributos que tenemos en nuestra clase Frames
    def __repr__(self):
        return 'Vintage Frames ' + str(self.id)

#creamos un diccionario para tomar los valores 
#para la pagina que llamamos post

all_frames = [{'title':'Marco Vintage 1','Author':'Arturo 1','Material':'El material del marco es blabla'},{'title':'Marco Vintage 2','Author':'Celsa 1','Material':'El material del marco es blabla'},{'title':'Marco Vintage 3','Material':'El material del marco es blabla'}]
#para crear las rutas, crearemos un decorador
@app.route('/')
def home():
    return render_template('home.html')

#creamos otro decorador para entrar a la pagina about
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/frames', methods=['GET','POST'])
def frames():
    if  request.method =='POST':
        post_title=request.form['title']
        post_material=request.form['material']
        new_post =Frames(title=post_title,Material=post_material)
        #db=get_db()
        db.session.add(new_post)
        db.session.commit()
        return redirect('/frames')
    else:
        all_frames=Frames.query.order_by(Frames.Date_posted).all()
        return render_template('frames.html', posts=all_frames)

@app.route('/frames/delete/<int:id>')
def delete(id):
    post=Frames.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/frames')
#@app.route('/<string:name>')
#def hello(name):
#    return "hello "+name

#@app.route('/<int:id>')
#def hello(id):
#    return "hello "+str(id)

#@app.route('/<string:name>/posts/<int:id>')
#def hello(name,id):
#    return "hello "+name +" your id is: "+str(id)

#@app.route('/onlyget', methods=['GET'])
#def get_req():
#    return 'you can only get this webpage'

#esta validacion indica que este sea el modulo que este corriendo siempre
if __name__=='__main__':
    app.run(debug=True)