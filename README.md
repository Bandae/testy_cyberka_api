# A movie rating website with django RF and vue (in progress)

Will feature a database of movies, which users can review and rate. Reviews can be commented and up/downvoted. The site's intended use is for closed groups to rate and compare movies they have watched.

### [Frontend repository link](https://github.com/Bandae/cyberka_front)

## Next steps:

- ✅<s>finish loggin/authentication functionality (registration, logging out)</s>
- ✅<s>complete CRUD for reviews, comments, votes</s>
- ✅<s>clean up axios requests</s>
- make sure to properly display error messages
- forgot password
- ✅<s>add profile pages</s>
- ✅<s>allow creating and updating movies</s>
- ✅<s>enforce permissions, movies - staff, reviews etc. - authorized users</s>
- ✅<s>change review serializer, get users vote for every comment to allow styling vote buttons</s>
- ✅<s>styling</s>
- allow uploading movie thumbnails / posters

### Possible features for later development:

- web scraping to make addding movies to the database easier.
- user profiles with statistics (the average rating, total up/downvote balance of all reviews, all watched movies etc.)
- _more to be added_

## Initial design:

### Main page:

![Main_page](https://user-images.githubusercontent.com/76438366/230723632-a8cd2159-ff33-4596-9aed-82446ba1903e.svg)

### Movie detail page:

![Movie_page](https://user-images.githubusercontent.com/76438366/230723653-5eae627d-fac8-409b-87e6-be10e6a1d333.svg)

## Setup

### DRF

```sh
python -m venv .venv
.\.venv\scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate --run-syncdb
python manage.py runserver
```

### vue

```sh
npm install
npm run dev
```
