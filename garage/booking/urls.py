from django.urls import path
from booking.views import BookSlot


urlpatterns = [
    path("", BookSlot.as_view(), name="book_slot"),
]