import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def build_fighter_profile(fighter):
    """Build a structured data profile for a fighter to send to the prediction engine."""
    total_wins = fighter.record_wins or 1
    total_losses = fighter.record_losses or 1

    return {
        "name": fighter.name,
        "record": fighter.record,
        "wins_by_method": {
            "ko_tko": fighter.wins_ko_tko,
            "ko_tko_pct": round((fighter.wins_ko_tko / total_wins) * 100, 1) if total_wins else 0,
            "submission": fighter.wins_submission,
            "submission_pct": round((fighter.wins_submission / total_wins) * 100, 1) if total_wins else 0,
            "decision": fighter.wins_decision,
            "decision_pct": round((fighter.wins_decision / total_wins) * 100, 1) if total_wins else 0,
        },
        "losses_by_method": {
            "ko_tko": fighter.losses_ko_tko,
            "ko_tko_pct": round((fighter.losses_ko_tko / total_losses) * 100, 1) if total_losses else 0,
            "submission": fighter.losses_submission,
            "submission_pct": round((fighter.losses_submission / total_losses) * 100, 1) if total_losses else 0,
            "decision": fighter.losses_decision,
            "decision_pct": round((fighter.losses_decision / total_losses) * 100, 1) if total_losses else 0,
        },
        "stats": {
            "avg_fight_time_min": fighter.avg_fight_time,
            "sig_strikes_per_min": fighter.sig_strikes_per_min,
            "strike_accuracy_pct": fighter.strike_accuracy,
            "takedown_avg": fighter.takedown_avg,
            "takedown_accuracy_pct": fighter.takedown_accuracy,
            "takedown_defense_pct": fighter.takedown_defense,
            "sub_attempts_per_min": fighter.sub_attempts_per_min,
        },
    }


def build_prediction_prompt(fighter_a_profile, fighter_b_profile, language="en"):
    """Construct the prompt for the prediction engine."""
    lang_instruction = ""
    if language == "fr":
        lang_instruction = "Respond with key_factors, vulnerability_note, and betting_insight in French."
    elif language == "ar":
        lang_instruction = "Respond with key_factors, vulnerability_note, and betting_insight in Arabic."

    return f"""You are an expert MMA analyst. Analyze this upcoming UFC fight and predict the outcome.

FIGHTER A:
{json.dumps(fighter_a_profile, indent=2)}

FIGHTER B:
{json.dumps(fighter_b_profile, indent=2)}

CRITICAL INSTRUCTION:
Cross-reference how each fighter wins with how the other fighter has LOST.
If Fighter A has submission wins AND Fighter B has submission losses, this is a KEY vulnerability — flag it explicitly in vulnerability_note and adjust prob_submission accordingly, even if Fighter B has a better overall record.
Do the same analysis for KO/TKO and decision tendencies.

{lang_instruction}

Return ONLY valid JSON in this exact format:
{{
  "winner": "Fighter A name or Fighter B name",
  "confidence": 67,
  "method_probabilities": {{
    "ko_tko": 28,
    "submission": 41,
    "decision_unanimous": 22,
    "decision_split": 7,
    "decision_majority": 2
  }},
  "predicted_round": 2,
  "predicted_time": "3:15",
  "key_factors": ["factor 1", "factor 2", "factor 3"],
  "vulnerability_note": "Description of key vulnerabilities detected...",
  "betting_insight": "Analysis of betting value..."
}}"""


def generate_prediction(fight, language="en"):
    """Generate a prediction for a fight using the Anthropic API."""
    import anthropic

    fighter_a_profile = build_fighter_profile(fight.fighter_a)
    fighter_b_profile = build_fighter_profile(fight.fighter_b)

    prompt = build_prediction_prompt(fighter_a_profile, fighter_b_profile, language)

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.content[0].text.strip()

    # Extract JSON from response (handle markdown code blocks)
    if raw_text.startswith("```"):
        lines = raw_text.split("\n")
        raw_text = "\n".join(lines[1:-1])

    prediction_data = json.loads(raw_text)

    from .models import Prediction
    from fighters.models import Fighter

    winner_name = prediction_data["winner"]
    if winner_name == fight.fighter_a.name:
        predicted_winner = fight.fighter_a
    elif winner_name == fight.fighter_b.name:
        predicted_winner = fight.fighter_b
    else:
        logger.warning(f"Winner name '{winner_name}' doesn't match either fighter, defaulting to fighter_a")
        predicted_winner = fight.fighter_a

    method_probs = prediction_data.get("method_probabilities", {})

    prediction, created = Prediction.objects.update_or_create(
        fight=fight,
        defaults={
            "predicted_winner": predicted_winner,
            "confidence": prediction_data.get("confidence", 50),
            "prob_ko_tko": method_probs.get("ko_tko", 0),
            "prob_submission": method_probs.get("submission", 0),
            "prob_dec_unanimous": method_probs.get("decision_unanimous", 0),
            "prob_dec_split": method_probs.get("decision_split", 0),
            "prob_dec_majority": method_probs.get("decision_majority", 0),
            "predicted_round": prediction_data.get("predicted_round"),
            "predicted_time": prediction_data.get("predicted_time", ""),
            "key_factors": prediction_data.get("key_factors", []),
            "vulnerability_note": prediction_data.get("vulnerability_note", ""),
            "betting_insight": prediction_data.get("betting_insight", ""),
        },
    )

    return prediction
