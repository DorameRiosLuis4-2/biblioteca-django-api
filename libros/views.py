from rest_framework.decorators import api_view, throttle_classes
from .throttles import BurstRateThrottle

@api_view(['GET'])
@throttle_classes([BurstRateThrottle])
def api_intensiva(request):
    # Esta ruta tiene throttling especial
    return Response({'data': 'información'})