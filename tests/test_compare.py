import pytest

from helpers import claim, coef, peak, results
from repro_check.compare import NOT_CHECKABLE, NOT_REPRODUCED, PARTLY, REPRODUCED, compare_claim, tally, compare_all
from repro_check.results import Profile


def verdict(c, r):
    return compare_claim(c, r).verdict


class TestPeakPosition:
    def test_peak_at_claimed_position_is_reproduced(self):
        assert verdict(claim(), results([peak()])) == REPRODUCED

    def test_exactly_at_tolerance_edge_passes(self):
        # 34 + 5 = 39; narrow CI so only the distance rule can pass it
        assert verdict(claim(), results([peak(pos=39.0, ci=(38.9, 39.1))])) == REPRODUCED

    def test_just_outside_tolerance_fails(self):
        assert verdict(claim(), results([peak(pos=39.5, ci=(39.4, 39.6))])) == NOT_REPRODUCED

    def test_claimed_position_inside_support_interval_passes(self):
        assert verdict(claim(), results([peak(pos=42.0, ci=(30.0, 45.0))])) == REPRODUCED

    def test_paper_rounding_widens_window(self):
        c = claim(pos_reported_precision_mb=10.0)
        assert verdict(c, results([peak(pos=43.0, ci=(42.9, 43.1))])) == REPRODUCED

    def test_wrong_chromosome_is_not_reproduced(self):
        assert verdict(claim(), results([peak(chr="2")])) == NOT_REPRODUCED

    def test_picks_highest_peak_in_window(self):
        v = compare_claim(claim(), results([peak(pos=31.0, lod=6.5), peak(pos=36.0, lod=9.0)]))
        assert v.observed["pos"] == 36.0


class TestThreshold:
    def test_peak_below_paper_threshold_is_not_reproduced(self):
        v = compare_claim(claim(), results([peak(lod=5.9)]))
        assert v.verdict == NOT_REPRODUCED
        assert [c.passed for c in v.checks] == [True, False]  # position, threshold

    def test_threshold_is_inclusive(self):
        assert verdict(claim(), results([peak(lod=6.0)])) == REPRODUCED

    def test_engine_threshold_above_claim_threshold_is_not_checkable(self):
        assert verdict(claim(), results([peak()], report_threshold=7.0)) == NOT_CHECKABLE


class TestLod:
    def test_lod_within_one(self):
        assert verdict(claim(lod=7.4), results([peak(lod=8.4)])) == REPRODUCED

    def test_lod_outside_one_is_partly(self):
        v = compare_claim(claim(lod=7.4), results([peak(lod=8.5)]))
        assert v.verdict == PARTLY
        assert v.checks[2].name == "LOD" and not v.checks[2].passed

    def test_relative_band_above_ten(self):
        # claimed 20 -> allowance 3.0
        assert verdict(claim(lod=20.0), results([peak(lod=22.9)])) == REPRODUCED
        assert verdict(claim(lod=20.0), results([peak(lod=23.1)])) == PARTLY


class TestFounderPattern:
    def test_single_high_founder_must_be_top(self):
        assert verdict(claim(founders_high=["F"]), results([peak(c=coef(high="F"))])) == REPRODUCED
        assert verdict(claim(founders_high=["F"]), results([peak(c=coef(order="AFBCDEGH"))])) == PARTLY

    def test_single_low_founder_must_be_bottom(self):
        assert verdict(claim(founders_low=["F"]), results([peak(c=coef(order="ABCDEGHF"))])) == REPRODUCED
        assert verdict(claim(founders_low=["F"]), results([peak(c=coef(order="ABCDEGFH"))])) == PARTLY

    def test_several_founders_must_be_in_the_right_half(self):
        c = claim(founders_high=["D", "H"], founders_low=["F", "G"])
        assert verdict(c, results([peak(c=coef(order="DAHBCEFG"))])) == REPRODUCED
        assert verdict(c, results([peak(c=coef(order="DABCHEFG"))])) == PARTLY

    def test_pattern_failure_does_not_rescue_missing_peak(self):
        assert verdict(claim(founders_high=["F"]), results([])) == NOT_REPRODUCED


class TestEffectPattern:
    def test_pattern_only_claim(self):
        c = claim(kind="effect_pattern", founders_low=["F"])
        assert verdict(c, results([peak(c=coef(low="F"))])) == REPRODUCED
        assert verdict(c, results([peak(c=coef(high="F"))])) == NOT_REPRODUCED

    def test_needs_a_peak(self):
        assert verdict(claim(kind="effect_pattern", founders_low=["F"]), results([])) == NOT_REPRODUCED


class TestAbsent:
    def test_flat_profile_reproduces_absence(self):
        assert verdict(claim(kind="qtl_absent"), results([])) == REPRODUCED

    def test_peak_above_threshold_in_window_breaks_absence(self):
        assert verdict(claim(kind="qtl_absent"), results([peak(lod=6.5)])) == NOT_REPRODUCED

    def test_peak_just_below_threshold_keeps_absence(self):
        assert verdict(claim(kind="qtl_absent"), results([peak(lod=5.99)])) == REPRODUCED

    def test_peak_outside_window_is_ignored(self):
        assert verdict(claim(kind="qtl_absent"), results([peak(pos=80.0, lod=12.0)])) == REPRODUCED

    def test_no_markers_in_window_is_not_checkable(self):
        prof = Profile(chr=["2"], pos=[10.0], lod={"t": [1.0]})
        assert verdict(claim(kind="qtl_absent"), results(profile=prof)) == NOT_CHECKABLE

    def test_nan_lod_is_skipped(self):
        prof = Profile(chr=["1", "1"], pos=[34.0, 35.0], lod={"t": [float("nan"), 2.0]})
        v = compare_claim(claim(kind="qtl_absent"), results(profile=prof))
        assert v.verdict == REPRODUCED and v.observed["window_max_pos"] == 35.0


class TestCount:
    def test_count_within_twenty_percent(self):
        r = results([peak(lod=7), peak(pos=60, lod=8), peak(chr="2", lod=5)])
        c = claim(kind="count", trait=None, traits=["t"], value=2.0)
        assert verdict(c, r) == REPRODUCED
        assert verdict(claim(kind="count", trait=None, traits=["t"], value=5.0), r) == NOT_REPRODUCED

    def test_unknown_trait_not_checkable(self):
        c = claim(kind="count", trait=None, traits=["nope"], value=2.0)
        assert verdict(c, results([])) == NOT_CHECKABLE


def test_missing_trait_is_not_checkable_never_reproduced():
    assert verdict(claim(trait="other"), results([peak()])) == NOT_CHECKABLE


def test_tally_counts_every_verdict():
    r = results([peak()])
    vs = compare_all([claim(), claim(id="C2", chr="2"), claim(id="C3", trait="x")], r)
    assert tally(vs) == {REPRODUCED: 1, PARTLY: 0, NOT_REPRODUCED: 1, NOT_CHECKABLE: 1}


@pytest.mark.parametrize("lod", [6.0, 8.0, 12.0])
def test_verdicts_are_deterministic(lod):
    r = results([peak(lod=lod)])
    assert compare_claim(claim(lod=8.0), r) == compare_claim(claim(lod=8.0), r)
