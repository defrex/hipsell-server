from django.views.generic import TemplateView

from listings.models import Listing

class ListingView(TemplateView):
    template_name = 'listings/listing.html'

    def get_context_data(self, **kwargs):
        return {
            'listing': Listing.objects.get(pk=self.kwargs['id'])
        }
