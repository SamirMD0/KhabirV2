from __future__ import annotations

from ..core.extensions import db
from ..models.case import AccidentCase


def get_by_id(id: int) -> AccidentCase | None:
    return db.session.get(AccidentCase, id)


def get_by_user(user_id: int) -> list[AccidentCase]:
    return AccidentCase.query.filter_by(user_id=user_id).order_by(AccidentCase.created_at.desc()).all()


def get_all() -> list[AccidentCase]:
    return AccidentCase.query.order_by(AccidentCase.created_at.desc()).all()


def create(case: AccidentCase) -> AccidentCase:
    db.session.add(case)
    save()
    return case


def save() -> None:
    db.session.commit()


def delete(case: AccidentCase) -> None:
    db.session.delete(case)
    save()

