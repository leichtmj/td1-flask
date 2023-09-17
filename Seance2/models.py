
from flask import Flask, render_template, render_template_string,request
from flask_sqlalchemy import SQLAlchemy

import os
from sqlalchemy import func

import seaborn as sns                      
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure     
import io
import base64
import numpy as np


file_path = os.path.abspath(os.getcwd())+"/database/chinook.db"


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

print(app.config['SQLALCHEMY_DATABASE_URI'])

# app.app_context().push()

#Model for table Artist
class Artist(db.Model):
    __tablename__ = 'Artists'
    ArtistId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120))
    albums = db.relationship('Album', backref='artists', lazy='dynamic')

    def __init__(self, Name):
        self.Name = Name
        
    def __repr__(self) :
        rep = 'Artist(Id : ' + str(self.ArtistId) + ', Name : ' + str(self.Name) + ')'
        return rep

#Model for table 'Album'
class Album(db.Model):
    __tablename__ = 'Albums'
    AlbumId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(160))
    ArtistId = db.Column(db.Integer, db.ForeignKey('Artists.ArtistId'))
    # Relation avec la table 'Track'
    tracks = db.relationship('Track', backref='albums', lazy='dynamic')
    def __init__(self, Title, ArtistId):
        self.Title = Title
        self.ArtistId = ArtistId
        
# Model for table 'Track'
class Track(db.Model):
    __tablename__ = 'Tracks'
    TrackId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200))
    AlbumId = db.Column(db.Integer, db.ForeignKey('Albums.AlbumId'))
    GenreId = db.Column(db.Integer, db.ForeignKey('Genres.GenreId'))
    
    invoice_items = db.relationship('InvoiceItem', backref='tracks', lazy='dynamic')
    
    def __init__(self, Name, AlbumId, GenreId):
        self.Name = Name
        self.AlbumId = AlbumId
        self.GenreId = GenreId
        
# Model for table 'Invoice_items'
class InvoiceItem(db.Model):
    __tablename__ = 'Invoice_items'
    InvoiceItemId = db.Column(db.Integer, primary_key=True) 
    TrackId = db.Column(db.Integer, db.ForeignKey('Tracks.TrackId'))
    Quantity = db.Column(db.Integer)

    def __init__(self, InvoiceItemId, TrackId, Quantity):
        self.InvoiceItemId = InvoiceItemId
        self.TrackId = TrackId
        self.Quantity = Quantity
        
class Invoice(db.Model):
    __tablename__='Invoices'
    InvoiceId = db.Column(db.Integer, primary_key=True)
    CustomerId=db.Column(db.Integer, db.ForeignKey('Customers.CustomerId'))
    Total = db.Column(db.Numeric)
    
    def __init__(self, InvoiceId, CustomerId, Total):
        self.InvoiceId = InvoiceId
        self.CustomerId = CustomerId
        self.Total = Total
    
class Customer(db.Model):
    __tablename__='Customers'
    CustomerId = db.Column(db.Integer, primary_key=True)
    FirstName=db.Column(db.String(40))
    LastName=db.Column(db.String(20))

    invoice = db.relationship('Invoice', backref='customers', lazy='dynamic')
    
    def __init__(self, CustomerId,FirstName, LastName):
        self.CustomerId = CustomerId
        self.FirstName=FirstName
        self.LastName=LastName
        
class Genre(db.Model):
    __tablename__='Genres'
    GenreId = db.Column(db.Integer, primary_key=True)
    Name=db.Column(db.String(120))
    
    tracks = db.relationship('Track', backref='genres', lazy='dynamic')
    
    def __init__(self, CustomerId,FirstName, LastName):
        self.CustomerId = CustomerId
        self.FirstName=FirstName
        self.LastName=LastName


with app.app_context():
    db.create_all()
    
@app.route('/', methods=['GET'])
def index():
    return render_template('database.html')
        
@app.route('/artists', methods=['POST'])
def list_artists():

    artists = Artist.query.all()

    print(Artist.query)
    print(type(artists))
    return render_template('database.html', getAllArtists=artists)

@app.route('/albumsbyartists', methods=['POST'])
def albumsbyartists():

    res = db.session.query(Artist.Name, func.count(Album.ArtistId)).join(Album, Album.ArtistId==Artist.ArtistId).group_by(Artist.ArtistId).all()
    print(res[0])
    return render_template('database.html', getAlbumsByArtists=res)


@app.route('/top10tracks', methods=['POST'])
def top10tracks():

    res = db.session.query(Track.Name, func.sum(InvoiceItem.Quantity).label('nb_achats')).join(InvoiceItem, InvoiceItem.TrackId==Track.TrackId).group_by(Track.TrackId).order_by(func.sum(InvoiceItem.Quantity).desc()).limit(10)
    print(res[0][0])
    return render_template('database.html', getTop10=res)

if __name__ == '__main__':
    app.run (debug=True)
    
@app.route('/top10achats', methods=['POST'])
def top10achats():
    
    res = db.session.query(Customer.FirstName,Customer.LastName, func.round(func.sum(Invoice.Total),2).label('total_depense')).join(Invoice, Invoice.CustomerId==Customer.CustomerId).group_by(Customer.CustomerId).order_by(func.sum(Invoice.Total).desc()).limit(10)

    return render_template('database.html', getTop10Achats=res)
    
@app.route('/histogenrepistes', methods=['POST'])
def histogenrepistes():
    

    

    # Convert plot to image
    img_b64 = plot_to_img()

    # Render HTML with base64 image
    html = f'<img src="data:image/png;base64,{img_b64}" class="blog-image">'
    return render_template_string(html)


def create_plot():
    # Create data
    res = db.session.query(Genre.Name).order_by(Genre.Name).all()
    genres = []
    for t in res:
        genres.extend(t)
    print(genres)
    
    nb_tracks = []
    res = db.session.query(func.count(Track.GenreId)).join(Genre, Genre.GenreId==Track.GenreId).group_by(Genre.Name).order_by(Genre.Name).all()
    for t in res:
        nb_tracks.extend(t)
    print(nb_tracks)
        
    fig = plt.figure(figsize=(13,7))
    
    ax = fig.add_subplot(111)

    ax.bar(genres, nb_tracks)
    
    ax.set_xlabel('Genres de musique')
    ax.set_ylabel('Nombre de chansons')
    
    plt.title('Nombre de chansons par genre de musique')
    
    plt.xticks(rotation=45,fontsize=10)  # Rotation des étiquettes pour un meilleur affichage
    plt.tight_layout()  # Ajustez la disposition
    
    
def plot_to_img():
    # Create plot
    create_plot()

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convert BytesIO object to base64 string
    img_b64 = base64.b64encode(img.getvalue()).decode()

    return img_b64