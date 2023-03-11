from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.core.validators import validate_comma_separated_integer_list
from random import shuffle
from django.utils import timezone


#class Subject(models.Model): #z.B. Psychologie vs. Medizin
#    name = models.CharField(max_length=255)

class Course(models.Model): #z.B. Sozialpsychologie I vs. Entwicklungspsychologie II
    #subject = models.ForeignKey(Subjet, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('home')

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted_user')[0]


class CardFront(models.Model):
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        )
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)

    def is_lonely(self):
        if self.front_for.count() == 0:
            return True
        else:
            return False

    def was_completed_in_colab(self):
        if self.front_for.count() >= 1:
            for card in self.front_for.all():
                if self.creator != card.creator:
                    return True
        else:
            return False 

    def first_colab_card(self):
        if self.front_for.count() >= 1:
            for card in self.front_for.all():
                if self.creator != card.creator:
                    return card
            return None
        else:
            return None            

    def __str__(self):
        return '\"' + self.body[3:19] + '...\" von ' + str(self.creator)


class CardBack(models.Model):
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        )
    #course = models.ForeignKey(Course, on_delete=models.RESTRICT)

    def __str__(self):
        return '\"' + self.body[3:19] + '...\" von ' + str(self.creator)

class Card(models.Model):
    front = models.ForeignKey(CardFront, related_name='front_for', blank=True, null=True, on_delete=models.RESTRICT)
    back = models.ForeignKey(CardBack, related_name='back_for', blank=True, null=True, on_delete=models.RESTRICT) 
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        )
    created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    sorted_out_by = models.ManyToManyField(User, related_name='sorted_out_cards', blank=True)
    appreciated_by = models.ManyToManyField(User, related_name='appreciated_cards', blank=True)

    def my_reps(self, user):
        my_reps = []
        for rep in user.rep_set.filter(card=self):
            my_reps.append(rep)
        return my_reps

    def last_rep(self, user):
        try:
            return user.rep_set.filter(card=self).latest('end_time')
        except:
            return None          

    def total_appreciators(self):
        return self.appreciated_by.count()

    def __str__(self):
        return '\"' + self.front.body[3:19] + '...\" von ' + str(self.creator)
        
    def get_absolute_url(self):
        return reverse('card_front', args=([str(self.id)]) )
      

class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    courses = models.ManyToManyField(Course, related_name='studied_by')

    def not_known_last_time(self): 
        not_known = {}
        preferred = set()
        last_reps = self.last_rep_per_card()
        for course in self.courses.all():
            for card in course.card_set.all():
                if card not in self.user.sorted_out_cards.all():
                    preferred.add(card.pk)
        for card_pk in preferred:
            if card_pk in last_reps:
                if not (last_reps[card_pk].i_know and last_reps[card_pk].i_knew):
                    not_known[card_pk] = last_reps[card_pk]
        try:        
            for card_pk in self.session.card_pk_list():
                not_known.pop(card_pk, None)
        except Session.DoesNotExist:
            pass
        return not_known

    def last_rep_per_card(self): 
        last_rep_per_card = {}
        my_reps = self.user.rep_set.all()
        for rep in my_reps:
            if rep.card.pk in last_rep_per_card:
                if last_rep_per_card[rep.card.pk].end_time < rep.end_time:
                    last_rep_per_card[rep.card.pk] = rep
            else: last_rep_per_card[rep.card.pk] = rep
        return last_rep_per_card

    def list_course_strings(self):
        output = []
        for course in self.courses.all():
            output.append(course.name)
        return output

    def __str__(self):
        return str(self.user)
        
    def get_absolute_url(self):
        return reverse('start_training')

class Rep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.PROTECT)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True, null=True)
    i_know = models.BooleanField(default=False)
    i_knew = models.BooleanField(default=False)
    back_seen = models.BooleanField(default=False)
    honors_bet = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + ' - ' +str(self.start_time.date()) + ' - "' +  self.card.front.body[3:19] + '..."'
        

class IllKnow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.PROTECT)
    said_when = models.DateTimeField(auto_now_add=True)
    when = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'card'], name='unique prognosis')
        ]

    def __str__(self):
        return str(self.user) + ': "Ich weiss es noch am ' +str(self.when.date()) + ', d.h. ' +  str((self.when - self.said_when).days) + ' Tage später"'

class HonoredIllKnow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.PROTECT)
    said_when = models.DateTimeField()
    when = models.DateTimeField()
    honored = models.DateTimeField(auto_now_add=True)
    i_know = models.BooleanField()
    i_knew = models.BooleanField()
    rep = models.ForeignKey(Rep, on_delete=models.PROTECT) #this field should be obsolete, or the i_know, i_knew, user and card fields are jointly obsolete, but I don't trust my code, so I'll add a few redundancies. (Reps can be changed after the fact if users use their browsers' back buttons - this shouldn't be possible, but it is, the way I hacked this thing together)

    def __str__(self):
        return str(self.user) + ': ' + str(self.i_knew) + ': "Ich weiss es noch ' +  str((self.when - self.said_when).days) + ' Tage später" - Geehrt am ' + str(self.honored.date()) + ', ' + str((self.honored - self.when).days) + ' Tage nach Fälligkeit der Wette'

class Session(models.Model):
    preferences = models.OneToOneField(Preferences, on_delete=models.CASCADE, primary_key=True)
    card_pk_list_string = models.TextField(validators=[validate_comma_separated_integer_list])
    next_list_position = models.SmallIntegerField(default=0)
    created =  models.DateTimeField(auto_now_add=True)
    reps = models.ManyToManyField(Rep, blank=True)

    def shuffle(self):
        if self.card_pk_list_string == '':
            pass
        else:
            pk_strings = self.card_pk_list_string.split(',')
            shuffle(pk_strings)
            self.card_pk_list_string = ','.join(pk_strings)
            self.save()

    def append(self, card_pk):
        if self.card_pk_list_string == '':
            self.card_pk_list_string += str(card_pk)
        else:            
            self.card_pk_list_string += ',' + str(card_pk)
        self.save()

    def remove(self, card_pk):
        if self.card_pk_list_string == '':
            pass
        else:            
            pk_strings = self.card_pk_list_string.split(',')
            new_card_pk_list_string = ''
            for pk_string in pk_strings:
                if str(card_pk) == pk_string:
                    pass
                else:
                    new_card_pk_list_string += ',' + pk_string
            self.card_pk_list_string = new_card_pk_list_string[1:]
            self.save()

    def card_pk_list(self):
        if self.card_pk_list_string == '':
            return []
        else:
            pk_string_list = self.card_pk_list_string.split(",")
            pk_int_list = []
            for string in pk_string_list:
                pk_int_list.append(int(string))
            return pk_int_list

    def deck_size(self):
        if self.card_pk_list_string == '':
            return 0
        else: 
            return self.card_pk_list_string.count(',') +1 - self.next_list_position

    def has_x_cards_illknow(self):
        count = 0
        for illknow in self.preferences.user.illknow_set.filter(when__lte=timezone.now()):
                count += 1
        return count

    def has_x_new_cards(self):
        count = 0
        for course in self.preferences.courses.all():
            for card in course.card_set.all():
                if card.created > self.created:
                    count += 1
        return count

    def pks_of_new_cards_list(self):
        pk_list = []
        for course in self.preferences.courses.all():
            for card in course.card_set.all():
                if card.created > self.created:
                    pk_list.append(card.pk)
        return pk_list

    def has_unseen_backs(self):
        for rep in self.reps.all():
            if not rep.back_seen:
                return True
        return False

    def unseen_backs_count(self):
        count = 0
        for rep in self.reps.all():
            if not rep.back_seen:
                count += 1
        return count

    def has_seen_backs(self):
        for rep in self.reps.all():
            if rep.back_seen:
                return True
        return False

    def seen_backs_count(self):
        count = 0
        for rep in self.reps.all():
            if rep.back_seen:
                count += 1
        return count

    def __str__(self):
        return 'Laufende Session von User No ' + str(self.pk) + ' - ' + str(self.preferences.user)

class SessionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    sorted_out_cards = models.ManyToManyField(Card)
    card_pk_list_string = models.TextField(validators=[validate_comma_separated_integer_list])
    reps = models.ManyToManyField(Rep)
    start = models.DateTimeField()
    end = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Session-Log No ' + str(self.pk) + ' - ' + str(self.user) + ' - ' + str(self.end)
