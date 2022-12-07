from flask import Flask,render_template,url_for,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from forms import *
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
from util import *
import networkx as nx


app = Flask(__name__)
Bootstrap(app)

ALLOWED_EXTENSIONS = {'csv', 'xsls'}
app.config['SECRET_KEY']='supersecretkey'
app.config['UPLOAD_FOLDER']='static/files'
edges=[]
DG = nx.DiGraph()



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_xml_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower()=='xml'


@app.route('/',methods=['POST','GET'])
def index():
    form = UploadFileForm()
    if request.method=='GET':        
        return render_template("index.html",form=form)
    if request.method=='POST':
        if form.validate_on_submit() :
            file = form.adjacency.data
            if file.filename=='':
                file = form.tp.data
                if file.filename=='':
                    file = form.xml.data
                    if file.filename=='':
                        flash('No selected file')
                        return redirect(request.url)                    
                    return show_page_rank(file,mode='XML_file')
                return show_page_rank(file,mode='Transition_probability')

            return show_page_rank(file,mode='Adjacency')


@app.route('/edges',methods=['POST','GET'])
def add_edges():
    form = UploadFileForm_edges()
    if request.method=='GET':        
        return render_template("add_edges.html",form=form)               
    if request.method=='POST':                
        if form.validate_on_submit() :
                source = form.source.data
                destination=form.destination.data 
                DG.add_edge(source,destination)
        else:
            return "There was an issue"        
        return  render_template("list_edges.html",edges=DG.edges)
    


@app.route('/prg',methods=['POST'])
def show_rank_graph():    
    if request.method=='POST':
        page_rank_object=PageRank(n=len(DG))
        page_rank_matrix=page_rank_object.PageRank_Graph(DG)

    return render_template("show_pr.html",rank_matrix=page_rank_matrix)
                   
@app.route('/delete/<int:source>/<int:destination>',methods=['GET'])
def delete(source,destination):
    if request.method=='GET':
        DG.remove_edge(source,destination)
        return render_template("list_edges.html",edges=DG.edges)




#the methods below are helper methods
def show_page_rank(file,mode='Adjacency'):
    if mode=='Adjacency' or  mode=='Transition_probability':
        if not allowed_file(file.filename):
                    flash('file format invalide please choose a csv file')
                    return redirect(request.url)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))

        page_rank_object=PageRank()
        csv_file=os.path.join("static/files",file.filename)
        page_rank_matrix=page_rank_object.PageRank_csv(csv_file,mode=mode)
    if mode=='XML_file':
        if not allowed_xml_file(file.filename):
                    flash('file format invalide please choose an xml file')
                    return redirect(request.url)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        page_rank_object=PageRank()
        csv_file=os.path.join("static/files",file.filename)
        page_rank_matrix=page_rank_object.Page_Rank_xmlFile(csv_file)
    return render_template("show_pr.html",rank_matrix=page_rank_matrix)



if __name__=="__main__":
    app.run(debug=True) 