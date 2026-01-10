from app.main import normalize_text

def test_normalization():
    assert normalize_text("Héllo") == "hello"
    assert normalize_text("  DRILL  ") == "drill"