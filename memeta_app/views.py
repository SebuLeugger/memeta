from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Course, CardFront, CardBack, Card, Preferences, Session, Rep, SessionLog
from .forms import AddCardFrontForm, AddCardBackForm, SetPreferencesForm, AddFrontForm, ChangePreferencesForm, RepFrontForm, RepBackForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.db.models import Q
from random import randint
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaulttags import register

def home_view(request):
    return render(request, 'home.html', {})

def add_view(request):
    return render(request, 'add.html', {})

class CoursesView(ListView):
    model = Course
    template_name = 'courses.html'

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def course_view(request, pk):
    course = get_object_or_404(Course, pk=pk).name
    course_cards = Card.objects.filter(course=pk)
    query = Q(course=pk)
    pks_of_fronts_with_backs = []
    last_rep_per_card = {}
    course_cards = course_cards.all()
    for card in course_cards:
        pks_of_fronts_with_backs.append(card.front.pk)
    query &= ~Q(id__in=pks_of_fronts_with_backs)
    solitary_cardfronts = CardFront.objects.filter(query)

    if request.user.is_authenticated:
        for card in course_cards:
            last_rep_per_card[card.pk] = [card.last_rep(request.user)]

    return render(request, 'course.html', {'course': course, 'course_cards': course_cards, 'solitary_cardfronts': solitary_cardfronts, 'last_rep_per_card': last_rep_per_card})
   
class AddCardFrontView(CreateView):
    model = CardFront
    form_class = AddCardFrontForm
    template_name = 'add_cardfront.html'
    pk = None

    def form_valid(self, form):
        form.instance.creator = self.request.user
        item = form.save()
        self.pk = item.pk
        return super(AddCardFrontView, self).form_valid(form)

    #def form_valid(self, form):
    #    form.instance.creator = self.request.user
    #    return super().form_valid(form)

    def get_success_url(self):
        return reverse( 'add_cardback', kwargs={'front_pk': self.pk} )


class AddCardBackView(CreateView):
    model = CardBack
    form_class = AddCardBackForm
    template_name = 'add_cardback.html'
    pk = None

    def form_valid(self, form):
        form.instance.creator = self.request.user
        item = form.save()
        self.pk = item.pk
        return super(AddCardBackView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(AddCardBackView, self).get_context_data()
        front = get_object_or_404(CardFront, id=self.kwargs['front_pk'])
        context['front'] = front
        return context

    def get_success_url(self):
         return reverse('add_card', kwargs={'front_pk': self.kwargs['front_pk'], 'back_pk': self.pk})

def add_card_view(request, *args, **kwargs):
    front = get_object_or_404(CardFront, pk=kwargs['front_pk'])
    back = get_object_or_404(CardBack, pk=kwargs['back_pk'])
    card = Card(front=front, back=back, creator=back.creator, course=front.course)
    card.save()
    return HttpResponseRedirect(reverse('card_back', args=([card.pk])))

class CardsView(ListView):
    model = Card
    template_name = 'cards.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        last_rep_per_card = {}
        if self.request.user.is_authenticated:
            for card in self.object_list:
                last_rep_per_card[card.pk] = [card.last_rep(self.request.user)]
                context['last_rep_per_card'] = last_rep_per_card
        return context


class CardFrontView(DetailView):
    model = Card
    template_name = 'card_front.html'

class CardBackView(DetailView):
    model = Card
    template_name = 'card_back.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CardBackView, self).get_context_data()
        card_from_db = get_object_or_404(Card, id=self.kwargs['pk'])
        total_appreciators = card_from_db.total_appreciators()
        context['total_appreciators'] = total_appreciators

        if self.request.user.is_authenticated:
            my_reps = card_from_db.my_reps(self.request.user)
            context['my_reps'] = my_reps

            session_pk_strings = self.request.user.preferences.session.card_pk_list_string.split(',')
            in_deck = 0
            for string in session_pk_strings:
                if str(self.object.pk) == string:
                    in_deck += 1
            context['in_deck'] = in_deck

        return context

def rep_repeat_view(request, pk):
    request.user.preferences.session.append(pk)
    request.user.preferences.session.shuffle()
    return HttpResponseRedirect(reverse('preferences', args=([str(request.user.pk)])) )

def card_into_deck_view(request, pk):
    request.user.preferences.session.append(pk)
    request.user.preferences.session.shuffle()
    return HttpResponseRedirect(reverse('card_back', args=([str(pk)])) )

def remove_card_from_deck_view(request, pk):
    request.user.preferences.session.remove(pk)
    return HttpResponseRedirect(reverse('card_back', args=([str(pk)])) )

def sort_out_card_view(request, pk):
    card = get_object_or_404(Card, id=request.POST.get('card_id'))
    card.sorted_out_by.add(request.user)
    return HttpResponseRedirect(reverse('remove_card_from_deck', args=([str(pk)])) )
    
def sort_in_card_view(request, pk):
    card = get_object_or_404(Card, id=request.POST.get('card_id'))
    card.sorted_out_by.remove(request.user)
    return HttpResponseRedirect(reverse('card_back', args=([str(pk)])) )
    
def appreciate_card_view(request, pk):
    card = get_object_or_404(Card, id=request.POST.get('card_id'))
    card.appreciated_by.add(request.user)
    return HttpResponseRedirect(reverse('card_back', args=([str(pk)])) )
    
def unappreciate_card_view(request, pk):
    card = get_object_or_404(Card, id=request.POST.get('card_id'))
    card.appreciated_by.remove(request.user)
    return HttpResponseRedirect(reverse('card_back', args=([str(pk)])) )


class AddFrontView(CreateView):
    model = CardFront
    form_class = AddFrontForm
    template_name = 'add_front.html'
    pk = None

    def form_valid(self, form):
        form.instance.creator = self.request.user
        item = form.save()
        self.pk = item.pk
        return super(AddFrontView, self).form_valid(form)

    def get_success_url(self):
        return reverse('front', kwargs={'pk': self.pk})

class FrontView(DetailView):
    model = CardFront
    template_name = 'front.html'

class FrontsView(ListView):
    model = CardFront
    template_name = 'fronts.html'


def start_training_view(request): #wieder entkommentieren für wenn ich fertig bin mit debugging
    #try:
    preferences = get_object_or_404(Preferences, pk=request.user)
    return render(request, 'preferences.html', {'preferences': preferences})
    #except:
    #    return redirect('set_preferences')

class SetPreferencesView(CreateView):
    model = Preferences
    form_class = SetPreferencesForm
    template_name = 'set_preferences.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PreferencesView(DetailView):    
    model = Preferences
    template_name = 'preferences.html'

class ChangePreferencesView(UpdateView):
    model = Preferences
    form_class = ChangePreferencesForm
    template_name = 'change_preferences.html'


def create_session_view(request):
    preferred_courses = request.user.preferences.courses.all()
    query = Q(course=preferred_courses[0])
    for course in preferred_courses[1:]:
        query |= Q(course=course)
    pks_of_sorted_out_cards = []
    for card in request.user.sorted_out_cards.all():
        pks_of_sorted_out_cards.append(card.pk)
    query &= ~Q(id__in=pks_of_sorted_out_cards)
    candidate_cards_iterable = Card.objects.filter(query).order_by('?').all()
    card_pk_list = []
    for card in candidate_cards_iterable:
        card_pk_list.append(card.pk)
    card_pk_list_string = ''
    for pk in card_pk_list:
        card_pk_list_string += str(pk) + ','
    card_pk_list_string = card_pk_list_string[:-1]
    session = Session(
        preferences=request.user.preferences, 
        card_pk_list_string=card_pk_list_string,
        created = timezone.now()
        )
    try: 
        session.update()
    except:
        session.save()
    return redirect('start_training')


def create_rep_view(request):
    session = request.user.preferences.session
    card_pk_list = session.card_pk_list_string.split(",")
    try:
        card = Card.objects.get(pk=int(card_pk_list[session.next_list_position]))
        session = Session(
            preferences=request.user.preferences,
            card_pk_list_string=session.card_pk_list_string, 
            next_list_position=session.next_list_position+1,
            created = session.created)
        session.save()
        rep = Rep(card=card, user=request.user)
        rep.save()
        session.reps.add(rep)
        return redirect(str(rep.pk) + '/front')
    except:
        return redirect('end_session')

class RepFrontView(UpdateView):
    model = Rep
    form_class = RepFrontForm
    template_name = 'rep_front.html'

    def get_success_url(self):
        if 'cardback' in self.request.POST:
            return 'back' # so eine syntax gibts auch, wofür die wohl steht?: return '{}#education'.format(reverse('profile', kwargs={'pk': pk}))
        elif 'overview' in self.request.POST:
            return '/session-overview/' + str(self.request.user.pk)
        else: # i.e. if 'nextcard' in request.POST
            return '/rep/create'

class RepBackView(UpdateView):
    model = Rep
    form_class = RepBackForm
    template_name = 'rep_back.html'

    def form_valid(self, form):
        form.instance.back_seen = True
        return super().form_valid(form)

    def get_success_url(self):
        if 'recap' in self.request.POST:
            return 'recap' # so eine syntax gibts auch, wofür die wohl steht?: return '{}#education'.format(reverse('profile', kwargs={'pk': pk}))
        elif 'overview' in self.request.POST:
            return '/session-overview/' + str(self.request.user.pk)
        else: # i.e. if 'nextcard' in request.POST
            return '/rep/create'

class RepRecapView(DetailView):
    model = Rep
    template_name = 'rep_recap.html'

class RepView(DetailView):
    model = Rep
    template_name = 'rep.html'

class SessionOverviewView(DetailView):
    model = Session
    template_name = 'session_overview.html'

def end_session_view(request):
    session = request.user.preferences.session
    card_pk_list = session.card_pk_list_string.split(",")[:session.next_list_position]
    if card_pk_list == []:
        return redirect('home') # das sollte nur passieren, wenn man nach der instant-session-recap in seinem browser auf zurück klickt und dann noch einmal auf session beenden. Eigentlich sollte sowas gar nicht passieren; http sollte stateless sein, ist es bei mir aber überaupt nicht...
    else: 
        card_pk_list_string = ''
        for pk in card_pk_list:
            card_pk_list_string += str(pk) + ','
        card_pk_list_string = card_pk_list_string[:-1]
        session_log = SessionLog(
            user = request.user,
            card_pk_list_string = card_pk_list_string,
            start =  request.user.preferences.session.reps.all()[0].start_time, #=request.user.preferences.session.created, #hier sollte ich wohl ein anderes feld im session-modell machen, damit dieses created nicht überschrieben werden muss; und zwar: ein feld, das die zeit angibt, wann ein training gestartet wurde
            )
        session_log.save()
        session_log.courses.set(request.user.preferences.courses.all())
        session_log.sorted_out_cards.set(request.user.sorted_out_cards.all())
        session_log.reps.set(request.user.preferences.session.reps.all())

        card_pk_list = session.card_pk_list_string.split(",")[session.next_list_position:]
        card_pk_list_string = ''
        for pk in card_pk_list:
            card_pk_list_string += str(pk) + ','
        card_pk_list_string = card_pk_list_string[:-1]
        session.card_pk_list_string = card_pk_list_string
        session.next_list_position = 0
        session.save()
        session.reps.clear()
        return redirect('/session-log/' + str(session_log.pk))

def session_refresh_view(request): #testen, dass das nicht eine fremde person auslösen kann!
    if request.user.is_authenticated:
        pk_list = request.user.preferences.session.pks_of_new_cards_list()
        string = ''
        for pk in pk_list:
            string += ','+str(pk)
        if request.user.preferences.session.card_pk_list_string == '':
            request.user.preferences.session.card_pk_list_string += string[1:]
        else:            
            request.user.preferences.session.card_pk_list_string += string
        request.user.preferences.session.created = timezone.now()
        request.user.preferences.session.save()
    return redirect('start_training')

def remove_seen_cards_view(request):
    if request.user.is_authenticated:
        if request.user.preferences.session.card_pk_list_string != '':
            pk_strings = request.user.preferences.session.card_pk_list_string.split(',')
            last_rep_per_card = request.user.preferences.last_rep_per_card()
            for pk_string in pk_strings:
                if int(pk_string) in last_rep_per_card:
                    if last_rep_per_card[int(pk_string)].back_seen:
                        if last_rep_per_card[int(pk_string)].end_time + timezone.timedelta(days=2) > timezone.now():
                            pk_strings = [string for string in pk_strings if string != pk_string]
            if pk_strings == []:
                request.user.preferences.session.card_pk_list_string = ''
            else:
                request.user.preferences.session.card_pk_list_string = ','.join(pk_strings)
            request.user.preferences.session.save()
    return redirect('start_training')

class SessionLogView(DetailView):    
    model = SessionLog
    template_name = 'sessionlog.html'

class UserProfileView(DetailView):
    model = User
    template_name = 'profile.html'

class HighscoreView(ListView):
    model = User
    template_name = 'highscore.html'