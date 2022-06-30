#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from re import A
import sys

import logging
from logging import Formatter, FileHandler

from datetime import datetime
from xml.dom import NotFoundErr

from models import db, Venue, Artist, Show  

from utils import format__venue_shows, format_datetime, format_artist_shows

from forms import VenueForm, ArtistForm, ShowForm, validate_phone

from flask import (
  Flask, 
  render_template, 
  request, 
  flash, 
  redirect, 
  url_for,
  abort
  )
from flask_moment import Moment
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

app.jinja_env.filters['datetime'] = format_datetime

 

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# Venues.
#----------------------------------------------------------------------------#

@app.route('/venues')
def venues():
  venues = Venue.query.all()
  data = []
  for venue in venues:
    venues_loc = Venue.query.filter_by(state=venue.state).filter_by(city=venue.city).all()
    venues_data = []
    for venue_loc in venues_loc:
      venues_data.append({
        'id': venue_loc.id,
        'name': venue_loc.name,
        })
    data.append({
      'city': venue_loc.city,
      'state': venue_loc.state,
      'venues': venues_data
      })
  return render_template('pages/venues.html', areas=data);


#----------------------------------------------------------------------------#
# Search Venues.
#----------------------------------------------------------------------------#

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form['search_term']
  venues = Venue.query.filter(Venue.name.ilike('%'+ search_term + '%'))
  data = []
  for venue in venues:
    cur_date = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
    all_upcomming_shows = Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time > cur_date).all()
    data.append({
      'id': venue.id,
      'name': venue.name,
      'num_upcoming_shows': len(all_upcomming_shows)  
      })
  response={
    "count": venues.count(),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

#----------------------------------------------------------------------------#
# Venues Detail.
#----------------------------------------------------------------------------#

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if venue is None:
      abort(404)

    cur_date = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
   
    all_upcomming_shows = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id, Show.start_time>cur_date)
    all_past_shows = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id, Show.start_time<cur_date)

    try:
      data: dict = venue.__dict__
      data["genres"] = venue.get_genres()
      data["seeking_talent"] = venue.looking_talent
      data["past_shows"] = format__venue_shows(all_past_shows)
      data["upcoming_shows"] = format__venue_shows(all_upcomming_shows)
      data["past_shows_count"] = all_past_shows.count()
      data["upcoming_shows_count"] = all_upcomming_shows.count()

      return render_template('pages/show_venue.html', venue=data)
    except:
      abort(500)
    

#----------------------------------------------------------------------------#
# Create Venues.
#----------------------------------------------------------------------------#

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    form = VenueForm(request.form)
    name = form.name.data
    city = form.city.data
    state = form.state.data
    website_link = form.website_link.data
    address =form.address.data
    phone = form.phone.data
    genres = ','.join(form.genres.data)
    facebook_link = form.facebook_link.data
    seeking_description = form.seeking_description.data
    image_link = form.image_link.data
    looking_talent = form.seeking_talent.data

    venue = Venue(
      name=name, 
      genres=genres, 
      address=address, 
      city=city,
      state=state, 
      phone=phone, 
      website_link=website_link, 
      facebook_link=facebook_link,
      looking_talent=looking_talent, 
      seeking_description=seeking_description,
      image_link=image_link)

    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except Exception as e:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# Venue Delete
#----------------------------------------------------------------------------#

@app.route('/venues/<venue_id>/delete', methods=['DELETE', 'POST', 'GET'])
def delete_venue(venue_id):
  try:
    venues = Venue.query.get(venue_id)
    try:
      show = Show.query.get(venue_id)
      db.session.delete(show)
    except Exception as e:
      print(e)
    db.session.delete(venues)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

#----------------------------------------------------------------------------#
# Venue Edit
#----------------------------------------------------------------------------#

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  try: 
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.genres.data = venue.genres
    form.address.data = venue.address
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.website_link.data = venue.website_link
    form.seeking_talent.data = venue.looking_talent
    form.seeking_description.data = venue.seeking_description
  except:
    flash('Oops... Something went wrong try again!')
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get(venue_id)
  try:
    form = VenueForm(request.form)

    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.website_link = form.website_link.data
    venue.address =form.address.data
    venue.phone = form.phone.data
    venue.genres = ','.join(form.genres.data)
    venue.facebook_link = form.facebook_link.data
    venue.seeking_description = form.seeking_description.data
    venue.image_link = form.image_link.data
    venue.looking_talent = form.seeking_talent.data

    db.session.commit()
    flash(request.form['name'] +' chanched successfully!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    abort(500)
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#----------------------------------------------------------------------------#
# Artists.
#----------------------------------------------------------------------------#

@app.route('/artists')
def artists():
  artists = Artist.query.all()
  data = []
  for artist in artists:
    data.append({
      'id': artist.id,
      'name': artist.name
      })
  return render_template('pages/artists.html', artists=data)

#----------------------------------------------------------------------------#
# Artist Search.
#----------------------------------------------------------------------------#

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form['search_term']
  artists = Artist.query.filter(Artist.name.ilike('%'+ search_term + '%'))
  data = []
  for artist in artists:
    data.append({
      'id': artist.id,
      'name': artist.name,
      })
  response={
    "count": artists.count(),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

#----------------------------------------------------------------------------#
# Artist Detail.
#----------------------------------------------------------------------------#

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)

  cur_date = datetime.now().strftime('%Y-%m-%d %H:%S:%M')

  all_upcomming_shows = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id, Show.start_time>cur_date)
  all_past_shows = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id, Show.start_time<cur_date)
  

  try:
    data: dict = artist.__dict__
    data["genres"] = artist.get_genres()
    data["seeking_talent"] = artist.looking_talent
    data["past_shows"] = format_artist_shows(all_past_shows)
    data["upcoming_shows"] = format_artist_shows(all_upcomming_shows)
    data["past_shows_count"] = all_past_shows.count()
    data["upcoming_shows_count"] = all_upcomming_shows.count()

    return render_template('pages/show_artist.html', artist=data)
  except:
    abort(500)

#----------------------------------------------------------------------------#
# Artist Delete.
#----------------------------------------------------------------------------#

@app.route('/artists/<int:artist_id>/delete', methods=['DELETE','POST', 'GET'])
def delete_artist(artist_id):
  try:
    artists = Artist.query.get(artist_id)
    try:
      show = Show.query.get(artist_id)
      db.session.delete(show)
    except Exception as e:
      print(e)
    db.session.delete(artists)  
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

#----------------------------------------------------------------------------#
# Artists Update.
#----------------------------------------------------------------------------#

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  if artist is None:
    abort(404)
  try:
    data = artist.__dict__
    data["genres"] = artist.get_genres()
    data["seeking_venue"] = artist.looking_talent
    form = ArtistForm(**data)
    return render_template('forms/edit_artist.html', form=form, artist=artist)
  except:
    abort(500)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.get(artist_id)
  try:
    form = ArtistForm(request.form)

    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.website_link = form.website_link.data
    artist.phone = form.phone.data
    artist.genres = ','.join(form.genres.data)
    artist.facebook_link = form.facebook_link.data
    artist.seeking_description = form.seeking_description.data
    artist.image_link = form.image_link.data
    artist.looking_talent = form.seeking_venue.data

    db.session.commit()
    flash(request.form['name'] +' chanched successfully!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    abort(500)
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

#----------------------------------------------------------------------------#
# Artists Create.
#----------------------------------------------------------------------------#

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    form = ArtistForm(request.form)
    name = form.name.data
    city = form.city.data
    state = form.state.data
    website_link = form.website_link.data
    phone = form.phone.data
    genres = ','.join(form.genres.data)
    facebook_link = form.facebook_link.data
    seeking_description = form.seeking_description.data
    image_link = form.image_link.data
    looking_talent = form.seeking_venue.data

    artist = Artist(
      name=name, 
      genres=genres, 
      city=city,
      state=state, 
      phone=phone, 
      website_link=website_link, 
      facebook_link=facebook_link,
      looking_talent=looking_talent, 
      seeking_description=seeking_description,
      image_link=image_link)

    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    abort(405)
  finally:
    db.session.close()

  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# Shows.
#----------------------------------------------------------------------------#

@app.route('/shows')
def shows():
  shows=Show.query.all()
  data=[]
  for show in shows:
    show_data = {
            "venue_id": show.venue_id,
            "venue_name": Venue.query.get(show.venue_id).name,
            "artist_id": show.artist_id,
            "artist_image_link":Artist.query.get(show.artist_id).image_link,
            "start_time": str(show.start_time)
        }
    data.append(show_data)
  return render_template('pages/shows.html', shows=data)

#----------------------------------------------------------------------------#
# Shows Create.
#----------------------------------------------------------------------------#

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  show = Show()
  try:
    show.artist_id = request.form['artist_id']
    show.venue_id = request.form['venue_id']
    show.start_time = request.form['start_time']
    db.session.add(show)
    db.session.commit()
    flash('Show posted successfully')
  except:
      db.session.rollback()
      print(sys.exc_info)
      abort(500)
  finally:
      db.session.close()
  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# Show Delete.
#----------------------------------------------------------------------------#

@app.route('/shows/<show_id>/delete', methods=['DELETE', 'GET', 'POST'])
def delete_show(show_id):
  shows = Show.query.filter_by(venue_id=show_id).all()
  for show in shows:
    db.session.delete(show)
  db.session.commit()
  db.session.close()

  return redirect(url_for('index'))


# ------------------------------------------------------------------------------------------------------
# Errors Handlers
#-------------------------------------------------------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
