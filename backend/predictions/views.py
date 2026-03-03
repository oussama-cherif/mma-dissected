from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from events.models import Fight
from .models import Prediction
from .serializers import PredictionSerializer
from .predictor import generate_prediction


class PredictionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Prediction.objects.select_related("predicted_winner", "fight")
    serializer_class = PredictionSerializer


class FightPredictionView(viewsets.ViewSet):
    """Handles prediction retrieval and generation for a specific fight."""

    def retrieve(self, request, fight_pk=None):
        """GET /api/fights/:id/prediction/ — get existing prediction."""
        try:
            prediction = Prediction.objects.select_related("predicted_winner").get(
                fight_id=fight_pk
            )
        except Prediction.DoesNotExist:
            return Response(
                {"detail": "No prediction available for this fight."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PredictionSerializer(prediction)
        return Response(serializer.data)

    def create(self, request, fight_pk=None):
        """POST /api/fights/:id/predict/ — generate or regenerate prediction."""
        try:
            fight = Fight.objects.select_related("fighter_a", "fighter_b").get(pk=fight_pk)
        except Fight.DoesNotExist:
            return Response(
                {"detail": "Fight not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        language = request.query_params.get("lang", "en")

        try:
            prediction = generate_prediction(fight, language=language)
        except Exception as e:
            return Response(
                {"detail": f"Prediction generation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer = PredictionSerializer(prediction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
