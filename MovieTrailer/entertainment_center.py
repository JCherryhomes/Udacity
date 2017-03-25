from media import Movie
import fresh_tomatoes as tomato

movies = [
    Movie(
        "Star Wars",
        "Three decades after the defeat of the Galactic Empire, a new threat arises. The First Order attempts to rule the galaxy and only a ragtag group of heroes can stop them, along with the help of the Resistance.",
        "https://upload.wikimedia.org/wikipedia/en/a/a2/Star_Wars_The_Force_Awakens_Theatrical_Poster.jpg",
        "https://www.youtube.com/watch?v=sGbxmsDFVnE"),

    Movie(
        "Captain America",
        "Storyline",
        "https://upload.wikimedia.org/wikipedia/en/5/53/Captain_America_Civil_War_poster.jpg",
        "https://www.youtube.com/watch?v=uVdV-lxRPFo"),

    Movie(
        "Logan",
        "Storyline",
        "https://upload.wikimedia.org/wikipedia/en/3/37/Logan_2017_poster.jpg",
        "https://www.youtube.com/watch?v=gbug3zTm3Ws"),

    Movie(
        "Wonder Woman",
        "Storyline",
        "https://upload.wikimedia.org/wikipedia/en/e/ed/Wonder_Woman_%282017_film%29.jpg",
        "https://www.youtube.com/watch?v=mNpDVccI5Ew"),

    Movie(
        "Toy Store", 
        "A story of a boy and his toys that come to life", 
        "http://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg", 
        "https://www.youtube.com/watch?v=vwyZH85NQC4"),

    Movie(
        "Avatar",
        "A marine on an alien planet",
        "http://upload.wikimedia.org/wikipedia/id/b/b0/Avatar-Teaser-Poster.jpg",
        "https://www.youtube.com/watch?v=-9ceBgWV8io")
]

tomato.open_movies_page(movies)