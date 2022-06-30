from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(), nullable=False)
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_talent = db.Column(db.Boolean(), default=False, nullable=False)
    seeking_description = db.Column(db.Text)
    shows = db.relationship('Show', backref='Venue',lazy ='joined')

    def __init__(self, name, genres, address, city, state, phone, website_link, facebook_link, image_link,
                 looking_talent, seeking_description):
        self.name = name
        self.genres = genres
        self.city = city
        self.state = state
        self.address = address
        self.phone = phone
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.website_link = website_link
        self.seeking_description = seeking_description
        self.looking_talent = looking_talent

    def __repr__(self):
      return f"<Vanue id:{self.id} name: {self.name}>"

    def get_genres(self):
      genres = str(self.genres).split(sep=",") 
      return genres


class Artist(db.Model):

    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(), nullable=False)
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_talent = db.Column(db.Boolean(),default=False, nullable=False)
    seeking_description = db.Column(db.Text)
    shows = db.relationship('Show', backref='Artist',lazy='joined')

    def __repr__(self):
      return f"<Artist id: {self.id} name: {self.id}>"

    def get_genres(self):
      genres = str(self.genres).split(sep=",") 
      return genres
      

class Show(db.Model):
  __tablename__='show'

  id = db.Column(db.Integer, primary_key = True)
  venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id))
  artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id))
  start_time = db.Column(db.String())

  def __repr__(self):
    return f"<Show id: {self.id} vanue: {self.venue_id} artist: {self.artist_id} start_time: {self.start_time}>"
 