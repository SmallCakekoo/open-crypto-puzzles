#!/usr/bin/env python3
"""
intruder_repeat_check.py -- test the "shares a director or lead actor with another
panel" hypothesis for the 10 intruders, against the full 34-panel corpus.

Purpose:
    The rules say the intruder criterion is "on IMDb, on each movie's page." Every
    IMDb title page lists a director and a top-billed cast. This script checks
    whether "this film's director OR top-billed actor also directs/stars in another
    film among these same 34 panels" picks out exactly the 10 films to drop, the
    way MPAA rating, Oscar wins, and novel adaptation (analysis/tested.md) did not.

Input:
    The DIRECTOR and LEAD_ACTOR tables below, one entry per panel, filled in from
    each film's own IMDb/Wikipedia page (sources noted where a specific claim was
    checked in this session; well-known credits for iconic films were not
    separately searched).

Output:
    Which panels share a director or lead actor with another panel in this set
    (the intruder candidates under this hypothesis), the resulting count, and
    whether it equals 10.

Usage:
    python analysis/intruder_repeat_check.py

This performs no search of its own and touches no escrow; it is arithmetic over a
small, manually compiled table.
"""

# panel: (title, director, lead_actor)
FILMS = {
    1: ("Die Hard", "John McTiernan", "Bruce Willis"),
    2: ("Paths of Glory", "Stanley Kubrick", "Kirk Douglas"),
    3: ("Alien", "Ridley Scott", "Sigourney Weaver"),
    4: ("Mad Max", "George Miller", "Mel Gibson"),
    5: ("Star Trek: The Motion Picture", "Robert Wise", "William Shatner"),
    6: ("Apocalypse Now", "Francis Ford Coppola", "Martin Sheen"),
    7: ("Escape from Alcatraz", "Don Siegel", "Clint Eastwood"),
    8: ("The Goonies", "Richard Donner", "Sean Astin"),  # primary hypothesis per user, 2026-08-19; Shutter Island kept as a probability, see analysis/leads.md
    9: ("Duel in the Sun", "King Vidor", "Jennifer Jones"),
    10: ("Mission: Impossible", "Brian De Palma", "Tom Cruise"),
    11: ("Ace Ventura: When Nature Calls", "Steve Oedekerk", "Jim Carrey"),
    12: ("Life of Pi", "Ang Lee", "Suraj Sharma"),
    13: ("Goodfellas", "Martin Scorsese", "Ray Liotta"),
    14: ("Eyes Wide Shut", "Stanley Kubrick", "Tom Cruise"),
    15: ("The Crimson Rivers", "Mathieu Kassovitz", "Jean Reno"),
    16: ("The 13th Warrior", "John McTiernan", "Antonio Banderas"),
    17: ("A Clockwork Orange", "Stanley Kubrick", "Malcolm McDowell"),
    18: ("Star Wars: A New Hope", "George Lucas", "Mark Hamill"),
    19: ("Gravity", "Alfonso Cuaron", "Sandra Bullock"),
    20: ("First Man", "Damien Chazelle", "Ryan Gosling"),
    21: ("Solaris", "Steven Soderbergh", "George Clooney"),  # 2002; version uncertain, see films.csv
    22: ("Blade Runner 2049", "Denis Villeneuve", "Ryan Gosling"),
    23: ("Valerian and the City of a Thousand Planets", "Luc Besson", "Dane DeHaan"),
    24: ("Ordinary People", "Robert Redford", "Donald Sutherland"),
    25: ("Barry Lyndon", "Stanley Kubrick", "Ryan O'Neal"),
    26: ("Sharknado", "Anthony C. Ferrante", "Ian Ziering"),
    27: ("The Lost Boys", "Joel Schumacher", "Jason Patric"),
    28: ("Scream 2", "Wes Craven", "Neve Campbell"),
    29: ("The Matrix Reloaded", "Lana Wachowski", "Keanu Reeves"),
    30: ("Toy Story", "John Lasseter", "Tom Hanks"),
    31: ("Ghostbusters II", "Ivan Reitman", "Bill Murray"),
    32: ("Raiders of the Lost Ark", "Steven Spielberg", "Harrison Ford"),
    33: ("The Shining", "Stanley Kubrick", "Jack Nicholson"),
    34: ("The Human Centipede (First Sequence)", "Tom Six", "Dieter Laser"),
}


def main():
    directors, actors = {}, {}
    for panel, (title, director, actor) in FILMS.items():
        directors.setdefault(director, []).append(panel)
        actors.setdefault(actor, []).append(panel)

    repeated_directors = {d: ps for d, ps in directors.items() if len(ps) > 1}
    repeated_actors = {a: ps for a, ps in actors.items() if len(ps) > 1}

    print("=== Repeated directors within the 34-panel set ===")
    for d, ps in sorted(repeated_directors.items(), key=lambda x: -len(x[1])):
        titles = [FILMS[p][0] for p in ps]
        print(f"  {d}: panels {ps} -> {titles}")

    print("\n=== Repeated lead actors within the 34-panel set ===")
    for a, ps in sorted(repeated_actors.items(), key=lambda x: -len(x[1])):
        titles = [FILMS[p][0] for p in ps]
        print(f"  {a}: panels {ps} -> {titles}")

    flagged = set()
    for ps in repeated_directors.values():
        flagged.update(ps)
    for ps in repeated_actors.values():
        flagged.update(ps)

    print(f"\n=== Panels flagged (share a director or lead actor with another panel here) ===")
    print(f"count: {len(flagged)} / 34")
    print(f"panels: {sorted(flagged)}")
    print(f"titles: {[FILMS[p][0] for p in sorted(flagged)]}")

    print(f"\nMatches the puzzle's required 10 intruders: {'YES' if len(flagged) == 10 else 'NO'}")

    keepers = sorted(set(FILMS) - flagged)
    print(f"\n=== Remaining 24 keepers (panel order) ===")
    print(keepers)


if __name__ == "__main__":
    main()
