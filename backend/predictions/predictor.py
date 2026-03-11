import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def build_fighter_profile(fighter):
    """Build a structured data profile for a fighter."""
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
    """Construct the prompt for generating fight predictions."""
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


def generate_stats_prediction(fight):
    """Generate a prediction using local stats analysis — no API needed."""
    a = fight.fighter_a
    b = fight.fighter_b

    score_a = 0.0
    score_b = 0.0

    # Win rate
    a_win_rate = a.record_wins / max(a.total_fights, 1)
    b_win_rate = b.record_wins / max(b.total_fights, 1)
    score_a += a_win_rate * 30
    score_b += b_win_rate * 30

    # Striking
    a_striking = (a.sig_strikes_per_min or 0) * (a.strike_accuracy or 0) / 100
    b_striking = (b.sig_strikes_per_min or 0) * (b.strike_accuracy or 0) / 100
    score_a += min(a_striking * 5, 15)
    score_b += min(b_striking * 5, 15)

    # Grappling
    a_grappling = (a.takedown_avg or 0) * (a.takedown_accuracy or 0) / 100
    b_grappling = (b.takedown_avg or 0) * (b.takedown_accuracy or 0) / 100
    score_a += min(a_grappling * 5, 10)
    score_b += min(b_grappling * 5, 10)

    # Defense
    score_a += (a.takedown_defense or 0) / 10
    score_b += (b.takedown_defense or 0) / 10

    # Vulnerability cross-reference: A's strengths vs B's weaknesses
    vuln_notes = []
    vuln_severity = 0  # track overall severity for betting insight

    # KO vulnerability
    ko_vuln_b = a.wins_ko_tko * b.losses_ko_tko
    ko_vuln_a = b.wins_ko_tko * a.losses_ko_tko
    if ko_vuln_b >= 2 and (a.wins_ko_tko >= 2 or b.losses_ko_tko >= 2):
        score_a += ko_vuln_b * 0.5
        severity = "HIGH" if ko_vuln_b >= 6 else "MODERATE"
        vuln_severity += ko_vuln_b
        vuln_notes.append(
            f"[{severity}] {b.name} has been KO/TKO'd {b.losses_ko_tko} times and {a.name} has {a.wins_ko_tko} KO/TKO wins — striking danger."
        )
    if ko_vuln_a >= 2 and (b.wins_ko_tko >= 2 or a.losses_ko_tko >= 2):
        score_b += ko_vuln_a * 0.5
        severity = "HIGH" if ko_vuln_a >= 6 else "MODERATE"
        vuln_severity += ko_vuln_a
        vuln_notes.append(
            f"[{severity}] {a.name} has been KO/TKO'd {a.losses_ko_tko} times and {b.name} has {b.wins_ko_tko} KO/TKO wins — striking danger."
        )

    # Submission vulnerability
    sub_vuln_b = a.wins_submission * b.losses_submission
    sub_vuln_a = b.wins_submission * a.losses_submission
    if sub_vuln_b >= 2 and (a.wins_submission >= 2 or b.losses_submission >= 2):
        score_a += sub_vuln_b * 0.8
        severity = "HIGH" if sub_vuln_b >= 4 else "MODERATE"
        vuln_severity += sub_vuln_b
        vuln_notes.append(
            f"[{severity}] {b.name} has {b.losses_submission} submission losses and {a.name} has {a.wins_submission} submission wins — grappling danger."
        )
    if sub_vuln_a >= 2 and (b.wins_submission >= 2 or a.losses_submission >= 2):
        score_b += sub_vuln_a * 0.8
        severity = "HIGH" if sub_vuln_a >= 4 else "MODERATE"
        vuln_severity += sub_vuln_a
        vuln_notes.append(
            f"[{severity}] {a.name} has {a.losses_submission} submission losses and {b.name} has {b.wins_submission} submission wins — grappling danger."
        )

    # Decision vulnerability — fighters who can't finish vs fighters who go the distance
    a_finish_rate = (a.wins_ko_tko + a.wins_submission) / max(a.record_wins, 1)
    b_finish_rate = (b.wins_ko_tko + b.wins_submission) / max(b.record_wins, 1)
    a_finished_rate = (a.losses_ko_tko + a.losses_submission) / max(a.record_losses, 1) if a.record_losses else 0
    b_finished_rate = (b.losses_ko_tko + b.losses_submission) / max(b.record_losses, 1) if b.record_losses else 0

    if a_finish_rate > 0.7 and b_finished_rate > 0.6 and b.record_losses >= 2:
        vuln_severity += 2
        vuln_notes.append(
            f"[MODERATE] {b.name} has been finished in {round(b_finished_rate * 100)}% of losses and {a.name} finishes {round(a_finish_rate * 100)}% of wins — high stoppage risk."
        )
    if b_finish_rate > 0.7 and a_finished_rate > 0.6 and a.record_losses >= 2:
        vuln_severity += 2
        vuln_notes.append(
            f"[MODERATE] {a.name} has been finished in {round(a_finished_rate * 100)}% of losses and {b.name} finishes {round(b_finish_rate * 100)}% of wins — high stoppage risk."
        )

    # Chin vulnerability — fighters with high KO loss rate
    if a.record_losses >= 3 and a.losses_ko_tko / max(a.record_losses, 1) >= 0.5:
        vuln_severity += 1
        vuln_notes.append(
            f"[MODERATE] {a.name} has been stopped by strikes in {a.losses_ko_tko} of {a.record_losses} losses — chin concerns."
        )
    if b.record_losses >= 3 and b.losses_ko_tko / max(b.record_losses, 1) >= 0.5:
        vuln_severity += 1
        vuln_notes.append(
            f"[MODERATE] {b.name} has been stopped by strikes in {b.losses_ko_tko} of {b.record_losses} losses — chin concerns."
        )

    # Calculate confidence and winner
    total = score_a + score_b
    if total == 0:
        total = 1

    conf_a = round((score_a / total) * 100)
    conf_b = round((score_b / total) * 100)

    if score_a >= score_b:
        winner = a
        confidence = max(min(conf_a, 95), 50)
    else:
        winner = b
        confidence = max(min(conf_b, 95), 50)

    # Method probabilities based on winner's style
    w = winner
    total_w_wins = w.record_wins or 1
    ko_pct = round((w.wins_ko_tko / total_w_wins) * 100)
    sub_pct = round((w.wins_submission / total_w_wins) * 100)
    dec_pct = 100 - ko_pct - sub_pct

    # Split decision probability
    dec_unan = round(dec_pct * 0.65)
    dec_split = round(dec_pct * 0.25)
    dec_maj = dec_pct - dec_unan - dec_split

    vulnerability_note = " ".join(vuln_notes) if vuln_notes else ""

    key_factors = []
    loser = b if winner == a else a

    if (winner.sig_strikes_per_min or 0) > 5:
        key_factors.append(f"{winner.name} has a high striking output ({winner.sig_strikes_per_min}/min)")
    if (winner.takedown_avg or 0) > 2:
        key_factors.append(f"{winner.name} averages {winner.takedown_avg} takedowns per 15 min")
    if (winner.takedown_defense or 0) > 85:
        key_factors.append(f"{winner.name} has elite takedown defense ({winner.takedown_defense}%)")
    if winner.record_wins > 20:
        key_factors.append(f"{winner.name} has deep experience with {winner.record_wins} wins")
    if (loser.takedown_defense or 0) < 55 and (winner.takedown_avg or 0) > 1.5:
        key_factors.append(f"{loser.name} has weak takedown defense ({loser.takedown_defense}%) against an active wrestler")
    if (winner.strike_accuracy or 0) > 55:
        key_factors.append(f"{winner.name} lands strikes at {winner.strike_accuracy}% accuracy")
    if not key_factors:
        key_factors.append(f"{winner.name} has a statistical edge based on overall record and fighting style")

    # Generate betting insight based on vulnerabilities and method probabilities
    betting_insight = ""
    if vuln_severity >= 4:
        dominant_method = max(
            [("KO/TKO", ko_pct), ("submission", sub_pct), ("decision", dec_pct)],
            key=lambda x: x[1]
        )
        betting_insight = (
            f"Significant stylistic mismatches detected. "
            f"{winner.name}'s most likely path to victory is by {dominant_method[0]} ({dominant_method[1]}%). "
            f"The vulnerability profile suggests this fight may not go the distance."
        )
    elif vuln_severity >= 2:
        betting_insight = (
            f"{winner.name} holds a notable edge in this matchup. "
            f"Method-specific vulnerabilities could create value on finish props."
        )
    elif confidence >= 70:
        betting_insight = (
            f"{winner.name} is a strong statistical favorite at {confidence}% confidence. "
            f"The data favors a {('KO/TKO' if ko_pct > sub_pct and ko_pct > dec_pct else 'submission' if sub_pct > dec_pct else 'decision')} outcome."
        )

    return {
        "winner": winner.name,
        "confidence": confidence,
        "method_probabilities": {
            "ko_tko": ko_pct,
            "submission": sub_pct,
            "decision_unanimous": dec_unan,
            "decision_split": dec_split,
            "decision_majority": dec_maj,
        },
        "predicted_round": None,
        "predicted_time": "",
        "key_factors": key_factors,
        "vulnerability_note": vulnerability_note,
        "betting_insight": betting_insight,
    }


def save_prediction(fight, prediction_data):
    """Save prediction data (from any source) to the database."""
    from .models import Prediction

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


def generate_prediction(fight, language="en"):
    """Generate a prediction — uses local stats analysis (free, no API needed)."""
    prediction_data = generate_stats_prediction(fight)
    return save_prediction(fight, prediction_data)


def import_prediction(fight, json_text):
    """Import a prediction from raw JSON text."""
    raw = json_text.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:-1])

    prediction_data = json.loads(raw)
    return save_prediction(fight, prediction_data)
