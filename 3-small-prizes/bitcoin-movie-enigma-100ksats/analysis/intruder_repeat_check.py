#!/usr/bin/env python3
"""
intruder_repeat_check.py -- test the "shares a director or lead actor with another
panel" hypothesis (H1) for the 10 intruders, against the full 34-panel corpus.

Updated 2026-08-20 for the major dataset revision (data/films.csv): with the
corrected film list, this criterion flags 14 of 34 panels, not 10. See
analysis/tested.md, "Major dataset revision," and analysis/leads.md for the full
breakdown. Kept here (not deleted) as the reference computation for H1 against the
current dataset, and as the starting point for any refined sub-criterion.

Usage:
    python analysis/intruder_repeat_check.py
"""

# panel: (title, director, lead_actor)
FILMS = {
    1: ("Die Hard", "John McTiernan", "Bruce Willis"),
    2: ("Paths of Glory", "Stanley Kubrick", "Kirk Douglas"),
    3: ("Aliens", "James Cameron", "Sigourney Weaver"),
    4: ("Mad Max", "George Miller", "Mel Gibson"),
    5: ("Alien", "Ridley Scott", "Sigourney Weaver"),
    6: ("Apocalypse Now", "Francis Ford Coppola", "Martin Sheen"),
    7: ("Escape from Alcatraz", "Don Siegel", "Clint Eastwood"),
    8: ("The Goonies", "Richard Donner", "Sean Astin"),
    9: ("Spartacus", "Stanley Kubrick", "Kirk Douglas"),
    10: ("Mission: Impossible", "Brian De Palma", "Tom Cruise"),
    11: ("Godzilla", "Roland Emmerich", "Matthew Broderick"),
    12: ("Life of Pi", "Ang Lee", "Suraj Sharma"),
    13: ("Leon: The Professional", "Luc Besson", "Jean Reno"),
    14: ("The Man in the Iron Mask", "Randall Wallace", "Leonardo DiCaprio"),
    15: ("The Crimson Rivers", "Mathieu Kassovitz", "Jean Reno"),
    16: ("The Visitors", "Jean-Marie Poire", "Christian Clavier"),
    17: ("A Clockwork Orange", "Stanley Kubrick", "Malcolm McDowell"),
    18: ("Star Wars: A New Hope", "George Lucas", "Mark Hamill"),
    19: ("Gravity", "Alfonso Cuaron", "Sandra Bullock"),
    20: ("First Man", "Damien Chazelle", "Ryan Gosling"),
    21: ("Solaris", "Andrei Tarkovsky", "Donatas Banionis"),
    22: ("Blade Runner 2049", "Denis Villeneuve", "Ryan Gosling"),
    23: ("Guardians of the Galaxy", "James Gunn", "Chris Pratt"),
    24: ("Close Encounters of the Third Kind", "Steven Spielberg", "Richard Dreyfuss"),
    25: ("Barry Lyndon", "Stanley Kubrick", "Ryan O'Neal"),
    26: ("Sharknado", "Anthony C. Ferrante", "Ian Ziering"),
    27: ("Terminator 2: Judgment Day", "James Cameron", "Arnold Schwarzenegger"),
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
    print(f"\n=== Remaining keepers (panel order) ===")
    print(keepers)


if __name__ == "__main__":
    main()
