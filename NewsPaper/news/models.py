from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Autor(models.Model):
    autorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAutor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        comRat = self.autorUser.comment_set.aggregate(comRating=Sum('rating'))
        cRat = 0
        cRat += comRat.get('comRating')

        self.ratingAutor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return str(self.autorUser)

sport = 'sport'
politics = 'politics'
education = 'education'
art = 'art'

TOPICS = [
    (sport, 'Спорт'),
    (politics, 'политика'),
    (education, 'образование'),
    (art, 'искусство')
]

class Category(models.Model):
    name = models.CharField(max_length=225, choices=TOPICS, unique=True, verbose_name='Категории')
    def __str__(self):
        return self.name

article = 'AR'
news = 'NW'
ARTICLEORNEWS = [
    (article, 'статья'),
    (news, 'сатья')
]
class Post(models.Model):
    PostAutor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    Choise = models.CharField(max_length=2, choices=ARTICLEORNEWS, default=article)
    timeCreation = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=255, verbose_name='Заголовок')
    _postcategory = models.ManyToManyField(Category, through='PostCategory')
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    def __str__(self):
        return str(self.header)

class PostCategory(models.Model):
    _Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    _Category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    com_text = models.TextField()
    timeCreation = models.DateTimeField(auto_now_add = True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.com_text