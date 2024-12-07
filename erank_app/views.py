# erank_app/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Import AllowAny
from .models import ShopListing
from .serializers import ShopListingSerializer
from .tasks import fetch_erank_data


class ShopListingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing shop listings.
    """
    queryset = ShopListing.objects.all()
    serializer_class = ShopListingSerializer

    # Remove authentication by setting permission_classes to AllowAny
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='fetch-erank-data')
    def fetch_erank_data_view(self, request):
        shop_name = request.data.get('shop_name')
        if not shop_name:
            return Response({'error': 'shop_name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        fetch_erank_data.delay(shop_name)
        return Response({'status': 'Task initiated successfully.'}, status=status.HTTP_200_OK)
