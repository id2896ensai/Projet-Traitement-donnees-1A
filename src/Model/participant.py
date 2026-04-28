class Participant:
    """Common base for any entity that can take part in a Match.

    Both Team (collective sports) and Player (individual sports) inherit
    from this class so Match can accept either without caring about the
    distinction.

    Subclasses must expose:
        full_name (str): display name shown in results.
        sport (Sport):   sport practiced by this participant.
    """
    pass
