from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField,IntegerField
from wtforms.validators import InputRequired

class UploadFileForm(FlaskForm):
    #,validators=[InputRequired()]
    adjacency=FileField("Adjacency Matrix (csv File)")
    tp=FileField("Transition Probability (csv File)")
    xml=FileField("XML File")
    submit=SubmitField("Upload  File")

class UploadFileForm_edges(FlaskForm):
    source=IntegerField("Enter the edge's source:")
    destination=IntegerField("Enter the edge's destination:")
    submit=SubmitField("Submit")