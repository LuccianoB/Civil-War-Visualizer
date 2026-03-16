from scripts.wikipedia_battles import parse_date_range

class TestParseDateRange:
    def test_single_day(self):
        out = parse_date_range("July 11, 1861")
        assert out["start_date"] == "1861-07-11"
        assert out["end_date"] == "1861-07-11"

    def test_same_month_range(self):
        out = parse_date_range("April 12-13, 1861")
        assert out["start_date"] == "1861-04-12"
        assert out["end_date"] == "1861-04-13"

    def test_cross_month_range(self):
        out = parse_date_range("April 25- May 1, 1862")
        assert out["start_date"] == "1862-04-25"
        assert out["end_date"] == "1862-05-01"