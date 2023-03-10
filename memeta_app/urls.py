from django.urls import path
#from . import views
from .views import AddCardFrontView, add_card_view, AddCardBackView, CardsView, CardFrontView, CardBackView, sort_out_card_view, sort_in_card_view, appreciate_card_view, unappreciate_card_view, card_into_deck_view, remove_card_from_deck_view
from .views import CoursesView, course_view, start_training_view, SetPreferencesView, PreferencesView, ChangePreferencesView, create_session_view, create_rep_view, RepFrontView, RepBackView,  SessionOverviewView, end_session_view, RepRecapView, rep_repeat_view, remove_seen_cards_view
from .views import AddIllKnowView, prognosis_session_view
from .views import home_view, HighscoreView, UserProfileView, SessionLogView, RepView, session_refresh_view
from .views import add_view, AddFrontView, FrontView, FrontsView

urlpatterns = [
    path('', home_view, name='home'),
    path('add', add_view, name='add'),

    path('add-card/', AddCardFrontView.as_view(), name='add_cardfront'),
    path('add-card/<int:front_pk>', AddCardBackView.as_view(), name='add_cardback'),
    path('add-card/<int:front_pk>/<int:back_pk>', add_card_view, name='add_card'),
    path('cards', CardsView.as_view(), name='cards'),
    path('card/front/<int:pk>', CardFrontView.as_view(), name='card_front'),
    path('card/back/<int:pk>', CardBackView.as_view(), name='card_back'),
    
    path('sort_out_card/<int:pk>', sort_out_card_view, name='sort_out_card'),
    path('sort_in_card/<int:pk>', sort_in_card_view, name='sort_in_card'),
    path('appreciate_card/<int:pk>', appreciate_card_view, name='appreciate_card'),
    path('unappreciate_card/<int:pk>', unappreciate_card_view, name='unappreciate_card'),
    path('card-into-deck/<int:pk>', card_into_deck_view, name='card_into_deck'),
    path('remove-card-from-deck/<int:pk>', remove_card_from_deck_view, name='remove_card_from_deck'),

    path('add-front', AddFrontView.as_view(), name='add_front'),
    path('front/<int:pk>', FrontView.as_view(), name='front'),
    path('fronts', FrontsView.as_view(), name='fronts'),
    
    path('courses/', CoursesView.as_view(), name='courses'), 
    path('course/<int:pk>', course_view, name='course'),
    
    path('training/start', start_training_view, name='start_training'),    
    path('preferences/set', SetPreferencesView.as_view(success_url='/session/create'), name='set_preferences'), 
    path('preferences/<int:pk>', PreferencesView.as_view(), name='preferences'),
    path('preferences/change/<int:pk>', ChangePreferencesView.as_view(success_url='/session/create'), name='change_preferences'),

    path('session/create', create_session_view, name='create_session'),
    path('session/end', end_session_view, name='end_session'),
    path('session-overview/<int:pk>', SessionOverviewView.as_view(), name='session_overview'),
    path('session-log/<int:pk>', SessionLogView.as_view(), name='session_log'),
    path('session/refresh', session_refresh_view, name='session_refresh'),
    path('rep-repeat/<int:pk>', rep_repeat_view, name='rep_repeat'),
    path('remove-seen-cards/', remove_seen_cards_view, name='remove_seen_cards'),

    path('rep/create', create_rep_view, name='create_rep'),
    path('rep/<int:pk>/front', RepFrontView.as_view(success_url='back'), name='rep_front'),
    path('rep/<int:pk>/back', RepBackView.as_view(success_url='recap'), name='rep_back'),
    path('rep/<int:pk>/recap', RepRecapView.as_view(), name='recap'),
    path('rep/<int:pk>/', RepView.as_view(), name='rep'),
    
    path('card/<int:card_pk>/prognosis', AddIllKnowView.as_view(), name='prognosis'),
    path('prognosis-session', prognosis_session_view, name='prognosis_session'),

    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('highscore/', HighscoreView.as_view(), name='highscore'),

]
