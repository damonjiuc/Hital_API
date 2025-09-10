from sqlalchemy import Integer, DateTime, func, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.utcnow())


class Question(Base):
    __tablename__ = 'questions'

    text: Mapped[str] = mapped_column(String, nullable=False)

    answers: Mapped[list['Answer']] = relationship(
        'Answer',
        back_populates='question',
        cascade='all, delete-orphan'
    )


class Answer(Base):
    __tablename__ = 'answers'

    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)

    question: Mapped["Question"] = relationship(
        'Question',
        back_populates='answers'
    )