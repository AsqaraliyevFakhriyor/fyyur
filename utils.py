import babel

import dateutil.parser



def format__venue_shows(shows):
    shows_list = []
    for show in shows:
        shows_list.append({
                'artist_id': show.artist_id,
                'artist_name': show.Artist.name,
                'artrist_image_link': str(show.Artist.image_link),
                'start_time': str(show.start_time)
                })
    return shows_list

def format_artist_shows(shows):
    shows_list = []
    for show in shows:
        shows_list.append({
            'venue_id': show.venue_id,
            'venue_name': show.Venue.name,
            'venue_image_link':show.Venue.image_link,
            'start_time': str(show.start_time)
            })
    return shows_list

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')



  # def shows_data(past_or_up):
  #   if past_or_up == 'up':
  #     for show in all_upcomming_shows:
  #       venue = Venue.query.get(show.venue_id)
  #       upcomming_shows.append({
  #         'venue_id': show.venue_id,
  #         'venue_name': venue.name,
  #         'venue_image_link':venue.image_link,
  #         'start_time': str(show.start_time)
  #         })
  #     return upcomming_shows
  #   else:
  #     for show in all_past_shows:
  #       venue = Venue.query.get(show.venue_id)
  #       past_shows.append({
  #         'venue_id': show.venue_id,
  #         'venue_name': venue.name,
  #         'venue_image_link':venue.image_link,
  #         'start_time': str(show.start_time)
  #         })
  #     return past_shows

  # data = {
  # 'id': artist.id,
  # 'name':artist.name,
  # 'genres':artist.genres.split(','),
  # 'city': artist.city,
  # 'state': artist.state,
  # 'phone': artist.state,
  # 'website': artist.website_link,
  # "facebook_link": artist.facebook_link,
  # "seeking_talent": artist.looking_talent,
  # "seeking_description": artist.seeking_description,
  # "image_link": artist.image_link,
  # "past_shows": shows_data('past'),
  # "upcoming_shows": shows_data('up'),
  # "past_shows_count": all_past_shows.count(),
  # "upcoming_shows_count": all_upcomming_shows.count(),
  # }