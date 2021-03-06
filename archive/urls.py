from django.urls import path

from . import views

#index page url configurations
urlpatterns = [
    path('', views.index, name='index'),
    path('scholarships/', views.ScholarshipListView.as_view(), name='scholarships'),
    #path('scholarships/', views.AwardedScholarshipsAllListView.as_view(), name='all-applied'),
    path('scholarship/<int:pk>', views.ScholarshipDetailView.as_view(), name='scholarship-detail'),
    path('donors/', views.DonorListView.as_view(), name='donors'),
    path('donor/<int:pk>',
         views.DonorDetailView.as_view(), name='donor-detail'),
    path('applicants/', views.ApplicantsListView.as_view(), name= 'student-applied')
]


urlpatterns += [
    path('myscholarships/', views.AwardedScholarshipsByUserListView.as_view(), name='my-applied'),
    path(r'apply/', views.AwardedScholarshipsAllListView.as_view(), name='all-applied'),
    path('success', views.Success.as_view(), name='success' ),

]


#intesting
urlpatterns += [
    path('scholarship/<uuid:pk>/apply/', views.apply_scholarship_archival, name='apply-scholarship-archival'),
]


# in testing
urlpatterns += [
    path('donor/create/', views.DonorCreate.as_view(), name='donor_create'),
    path('donor/<int:pk>/update/', views.DonorUpdate.as_view(), name='donor_update'),
    path('donor/<int:pk>/delete/', views.DonorDelete.as_view(), name='donor_delete'),
]

# Add URLConf to create, update, and delete scholarships
urlpatterns += [
    path('scholarship/create/', views.ScholarshipCreate.as_view(), name='scholarship_create'),
    path('scholarship/<int:pk>/update/', views.ScholarshipUpdate.as_view(), name='scholarship_update'),
    path('scholarship/<int:pk>/delete/', views.ScholarshipDelete.as_view(), name='scholarship_delete'),
]
