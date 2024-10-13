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

    @action(detail=False, methods=['post'], url_path='fetch-erank_app-data')
    def fetch_erank_data_view(self, request):
        """
        API endpoint to fetch eRank data for a given shop.
        Expects 'shop_name' and optional 'offset' in the request data.
        """
        shop_name = request.data.get('shop_name')
        offset = request.data.get('offset', 0)

        if not shop_name:
            return Response(
                {'error': 'shop_name is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Call your task to fetch and save eRank data
            fetch_erank_data(shop_name, offset)
            return Response(
                {'status': 'Data fetched and saved successfully.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
