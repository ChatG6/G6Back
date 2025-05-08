from django.urls import  path,include
from . import views
urlpatterns = [

    path('literature/',views.LiteratureView.as_view(),name='literature'),
    path('documentation/',views.Documentation.as_view(),name='documentation'),
    path('plagiarism/',views.Plagiarism_detector.as_view(),name='plagiarism_detector'),
    path('article/',views.Article.as_view(),name='article_generator'),
    path('outline/',views.Outline.as_view(),name='outline_generator'),
    path('complete/',views.Complete.as_view(),name='complete_generator')
]