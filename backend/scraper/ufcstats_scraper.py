import logging
import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils import timezone

logger = logging.getLogger(__name__)

BASE_URL = "http://ufcstats.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def _get_soup(url):
    """Fetch a page and return a BeautifulSoup object."""
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def _clean(text):
    """Strip whitespace from scraped text."""
    return text.strip() if text else ""


def _parse_pct(text):
    """Parse '48%' -> 48.0, returns None if not parseable."""
    m = re.search(r"(\d+)%", text)
    return float(m.group(1)) if m else None


def _parse_float(text):
    """Parse '7.20' -> 7.2, returns None if not parseable."""
    try:
        return float(text.strip())
    except (ValueError, AttributeError):
        return None


# --- Events ---

def scrape_events(page="completed", limit=5):
    """
    Scrape events from ufcstats.com.
    page: 'completed' or 'upcoming'
    limit: max number of events to return
    """
    url = f"{BASE_URL}/statistics/events/{page}"
    soup = _get_soup(url)

    events = []
    rows = soup.select("tr.b-statistics__table-row_type_first, tr.b-statistics__table-row")

    for row in rows:
        link = row.select_one("a.b-link")
        if not link:
            continue

        name = _clean(link.text)
        href = link.get("href", "")
        event_id = href.split("/")[-1] if href else ""

        date_el = row.select_one("span.b-statistics__date")
        date_str = _clean(date_el.text) if date_el else ""

        location_td = row.select("td.b-statistics__table-col")
        location = ""
        if len(location_td) >= 2:
            location = _clean(location_td[1].text)

        event_date = None
        if date_str:
            try:
                event_date = datetime.strptime(date_str, "%B %d, %Y")
                event_date = event_date.replace(hour=23, minute=0)
                event_date = timezone.make_aware(
                    event_date, timezone=timezone.utc
                )
            except ValueError:
                logger.warning(f"Could not parse date: {date_str}")

        events.append({
            "ufcstats_id": event_id,
            "name": name,
            "date": event_date,
            "location": location,
            "url": href,
            "status": "upcoming" if page == "upcoming" else "completed",
        })

        if len(events) >= limit:
            break

    return events


def scrape_event_fights(event_url):
    """
    Scrape all fights from an event detail page.
    Returns list of fight dicts with fighter names, links, weight class, method, etc.
    """
    soup = _get_soup(event_url)

    # Event name and info
    title_el = soup.select_one("h2.b-content__title span.b-content__title-highlight")
    event_name = _clean(title_el.text) if title_el else ""

    date_str = ""
    location = ""
    info_items = soup.select("li.b-list__box-list-item")
    for item in info_items:
        label = item.select_one("i.b-list__box-item-title")
        if not label:
            continue
        label_text = _clean(label.text).rstrip(":")
        value = _clean(item.text.replace(label.text, ""))
        if "Date" in label_text:
            date_str = value
        elif "Location" in label_text:
            location = value

    # Fights table
    fights = []
    fight_rows = soup.select("tr.b-fight-details__table-row.js-fight-details-click")

    for idx, row in enumerate(fight_rows):
        cols = row.select("td.b-fight-details__table-col")
        if len(cols) < 10:
            continue

        # Fighter links
        fighter_links = cols[1].select("a.b-link")
        if len(fighter_links) < 2:
            continue

        fighter_a_name = _clean(fighter_links[0].text)
        fighter_a_url = fighter_links[0].get("href", "")
        fighter_a_id = fighter_a_url.split("/")[-1]

        fighter_b_name = _clean(fighter_links[1].text)
        fighter_b_url = fighter_links[1].get("href", "")
        fighter_b_id = fighter_b_url.split("/")[-1]

        # W/L indicator
        wl_col = cols[0]
        wl_flags = wl_col.select("i.b-flag__text")
        winner_flag = _clean(wl_flags[0].text).lower() if wl_flags else ""

        # Weight class
        weight_el = cols[6].select_one("p.b-fight-details__table-text")
        weight_class = _clean(weight_el.text).split("\n")[0].strip() if weight_el else ""

        # Method
        method_el = cols[7].select_one("p.b-fight-details__table-text")
        method = _clean(method_el.text).split("\n")[0].strip() if method_el else ""

        # Round
        round_el = cols[8].select_one("p.b-fight-details__table-text")
        fight_round = _clean(round_el.text) if round_el else ""

        # Time
        time_el = cols[9].select_one("p.b-fight-details__table-text")
        fight_time = _clean(time_el.text) if time_el else ""

        # Determine card section based on position
        if idx == 0:
            card_section = "main"
        elif idx <= 4:
            card_section = "main"
        elif idx <= 8:
            card_section = "prelim"
        else:
            card_section = "early"

        fights.append({
            "fighter_a": {
                "name": fighter_a_name,
                "ufcstats_id": fighter_a_id,
                "url": fighter_a_url,
            },
            "fighter_b": {
                "name": fighter_b_name,
                "ufcstats_id": fighter_b_id,
                "url": fighter_b_url,
            },
            "weight_class": weight_class,
            "method": method,
            "round": fight_round,
            "time": fight_time,
            "winner": "a" if winner_flag == "win" else ("b" if winner_flag == "loss" else ""),
            "card_section": card_section,
            "order": idx,
        })

    return {
        "name": event_name,
        "date": date_str,
        "location": location,
        "fights": fights,
    }


# --- Fighter Stats ---

def scrape_fighter(fighter_url):
    """
    Scrape a fighter's full stats from their ufcstats.com profile.
    Returns a dict with all stats we need for our Fighter model.
    """
    soup = _get_soup(fighter_url)

    # Name
    name_el = soup.select_one("span.b-content__title-highlight")
    name = _clean(name_el.text) if name_el else ""

    # Nickname
    nick_el = soup.select_one("p.b-content__Nickname")
    nickname = _clean(nick_el.text).strip('"') if nick_el else ""

    # Record from title
    record_el = soup.select_one("span.b-content__title-record")
    record_text = _clean(record_el.text) if record_el else ""
    wins, losses, draws = 0, 0, 0
    record_match = re.search(r"Record:\s*(\d+)-(\d+)-(\d+)", record_text)
    if record_match:
        wins = int(record_match.group(1))
        losses = int(record_match.group(2))
        draws = int(record_match.group(3))

    # Career stats (SLpM, Str Acc, TD Avg, etc.)
    stats = {}
    stat_items = soup.select("li.b-list__box-list-item")
    for item in stat_items:
        title_el = item.select_one("i.b-list__box-item-title")
        if not title_el:
            continue
        label = _clean(title_el.text).rstrip(":").strip()
        value = _clean(item.text.replace(title_el.text, ""))
        stats[label] = value

    sig_strikes_per_min = _parse_float(stats.get("SLpM", ""))
    strike_accuracy = _parse_pct(stats.get("Str. Acc.", ""))
    takedown_avg = _parse_float(stats.get("TD Avg.", ""))
    takedown_accuracy = _parse_pct(stats.get("TD Acc.", ""))
    takedown_defense = _parse_pct(stats.get("TD Def.", ""))
    sub_attempts = _parse_float(stats.get("Sub. Avg.", ""))

    # Weight class from the info box
    weight_class = stats.get("Weight", "").replace("lbs.", "").strip()

    # Parse fight history to count win/loss methods
    wins_ko, wins_sub, wins_dec = 0, 0, 0
    losses_ko, losses_sub, losses_dec = 0, 0, 0

    fight_rows = soup.select("tr.b-fight-details__table-row.js-fight-details-click")
    for row in fight_rows:
        # W/L flag
        flag = row.select_one("i.b-flag__text")
        if not flag:
            continue
        result = _clean(flag.text).lower()

        # Method column (8th col, index 7)
        cols = row.select("td.b-fight-details__table-col")
        if len(cols) < 10:
            continue

        method_el = cols[7].select_one("p.b-fight-details__table-text")
        method = _clean(method_el.text).upper() if method_el else ""

        if result == "win":
            if "KO" in method or "TKO" in method:
                wins_ko += 1
            elif "SUB" in method:
                wins_sub += 1
            elif "DEC" in method:
                wins_dec += 1
        elif result == "loss":
            if "KO" in method or "TKO" in method:
                losses_ko += 1
            elif "SUB" in method:
                losses_sub += 1
            elif "DEC" in method:
                losses_dec += 1

    return {
        "name": name,
        "nickname": nickname,
        "weight_class": weight_class,
        "record_wins": wins,
        "record_losses": losses,
        "record_draws": draws,
        "wins_ko_tko": wins_ko,
        "wins_submission": wins_sub,
        "wins_decision": wins_dec,
        "losses_ko_tko": losses_ko,
        "losses_submission": losses_sub,
        "losses_decision": losses_dec,
        "sig_strikes_per_min": sig_strikes_per_min,
        "strike_accuracy": strike_accuracy,
        "takedown_avg": takedown_avg,
        "takedown_accuracy": takedown_accuracy,
        "takedown_defense": takedown_defense,
        "sub_attempts_per_min": sub_attempts,
    }
