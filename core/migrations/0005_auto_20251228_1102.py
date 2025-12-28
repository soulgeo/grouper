from django.db import migrations


def seed_interests(apps, schema_editor):
    InterestCategory = apps.get_model('core', 'InterestCategory')
    Interest = apps.get_model('core', 'Interest')

    initial_data = {
        "Sports & Outdoors": [
            "Soccer",
            "Basketball",
            "Tennis",
            "Running",
            "Hiking",
            "Cycling",
            "Swimming",
            "Yoga",
            "Gym/Fitness",
            "Surfing",
        ],
        "Tech & Coding": [
            "Python",
            "Web Development",
            "AI & Machine Learning",
            "Data Science",
            "Gaming",
            "Robotics",
            "Cybersecurity",
            "Blockchain",
            "Open Source",
            "Hardware/DIY",
        ],
        "Arts & Creatives": [
            "Painting",
            "Photography",
            "Digital Art",
            "Writing",
            "Sketching",
            "Pottery",
            "Calligraphy",
            "Graphic Design",
            "Filmmaking",
            "Fashion Design",
        ],
        "Music & Audio": [
            "Playing Guitar",
            "Playing Piano",
            "Singing",
            "Music Production",
            "DJing",
            "Podcasts",
            "Vinyl Collecting",
            "Concerts/Festivals",
            "Classical Music",
            "Jazz",
        ],
        "Food & Drink": [
            "Cooking",
            "Baking",
            "Coffee Brewing",
            "Mixology/Bartending",
            "Wine Tasting",
            "Foodie/Dining Out",
            "Vegan Cooking",
            "BBQ & Grilling",
        ],
        "Travel & Adventure": [
            "Backpacking",
            "Solo Travel",
            "Camping",
            "Road Trips",
            "Language Learning",
            "Cultural Exchange",
            "Van Life",
            "City Breaks",
        ],
        "Gaming": [
            "PC Gaming",
            "Console Gaming",
            "Tabletop RPGs (D&D)",
            "Board Games",
            "Esports",
            "Retro Gaming",
            "Mobile Gaming",
            "Game Development",
        ],
        "Reading & Learning": [
            "Fiction",
            "Non-Fiction",
            "Sci-Fi/Fantasy",
            "History",
            "Philosophy",
            "Self-Improvement",
            "Science",
            "Biographies",
            "Book Clubs",
        ],
        "Entertainment": [
            "Movies",
            "TV Series",
            "Anime",
            "Documentaries",
            "Theatre/Musicals",
            "Stand-up Comedy",
            "Magic/Illusion",
        ],
        "DIY & Crafts": [
            "Knitting/Crochet",
            "Woodworking",
            "Gardening",
            "Sewing",
            "Interior Design",
            "Origami",
            "Model Building",
            "Upcycling",
        ],
    }

    for cat_name, interests_list in initial_data.items():
        category_obj, _ = InterestCategory.objects.get_or_create(name=cat_name)

        interest_objects = [
            Interest(name=interest_name, category=category_obj)
            for interest_name in interests_list
        ]

        Interest.objects.bulk_create(interest_objects, ignore_conflicts=True)


def remove_interests(apps, schema_editor):
    InterestCategory = apps.get_model('core', 'InterestCategory')
    Interest = apps.get_model('core', 'Interest')
    Interest.objects.all().delete()
    InterestCategory.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        (
            'core',
            '0004_interestcategory_interest',
        ),
    ]

    operations = [
        migrations.RunPython(seed_interests, remove_interests),
    ]
