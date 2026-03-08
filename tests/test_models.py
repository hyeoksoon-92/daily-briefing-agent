from api.models.briefing import Briefing
from sqlalchemy import inspect as sa_inspect


def test_briefing_model_has_required_columns():
    mapper = sa_inspect(Briefing)
    columns = {col.key for col in mapper.columns}
    assert {"id", "date", "content", "created_at"}.issubset(columns)

def test_briefing_table_name():
    assert Briefing.__tablename__ == "briefings"
