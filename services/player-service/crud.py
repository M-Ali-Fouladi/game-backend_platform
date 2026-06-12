from sqlalchemy.orm import Session
from models import Player


def create_player(
    db: Session,
    username: str,
    email: str
):
    player = Player(
        username=username,
        email=email
    )

    db.add(player)
    db.commit()
    db.refresh(player)

    return player


def get_player(
    db: Session,
    player_id: int
):
    return (
        db.query(Player)
        .filter(Player.id == player_id)
        .first()
    )


def add_xp(
    db: Session,
    player_id: int,
    amount: int
):
    player = get_player(db, player_id)

    player.xp += amount

    db.commit()
    db.refresh(player)

    return player


def update_mmr(
    db: Session,
    player_id: int,
    amount: int
):
    player = get_player(db, player_id)

    player.mmr += amount

    db.commit()
    db.refresh(player)

    return player