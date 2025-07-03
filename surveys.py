import sqlalchemy as sa

from orm import ORMUnitOfWork
from surveys_model import MVSurveysStatus


def get_surveys_by_loaded_at():
    sql_model = sa.select(MVSurveysStatus).order_by(MVSurveysStatus.loaded_at)
    sql_text = sa.text(
        "SELECT * FROM analysis.mview_surveys_loaded_at_status ORDER BY loaded_at"
    )

    # print(sql_model, sql_text, sep="\n\n", end="\n\n")

    with ORMUnitOfWork() as db:
        result_model = db.execute(sql_model).all()
        result_text = db.execute(sql_text).all()

    count = 0
    print(
        "Seq. |",
        " ",
        " sa.select(Model)       |",
        " sa.text('select ...')",
        sep="\t",
    )
    while count < 30:
        print(
            f"  {count}  |",
            f"{result_model[count][0].loaded_at} => {result_model[count][0].status}",
            "|",
            f"{result_text[count].loaded_at} => {result_text[count].status}",
            sep="\t",
        )
        count += 1


if __name__ == "__main__":
    get_surveys_by_loaded_at()
