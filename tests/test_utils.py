"""Tests for search URL generation and result file locations."""

from pathlib import Path

from src.bot import config, utils


def test_data_path_follows_configured_folder(tmp_path: Path) -> None:
    utils.set_data_dir(tmp_path / "chris")

    assert utils.data_path() == str(tmp_path / "chris")
    assert utils.data_path("urlData.txt") == str(tmp_path / "chris" / "urlData.txt")


def test_results_and_failures_are_written_to_data_folder(tmp_path: Path) -> None:
    utils.set_data_dir(tmp_path / "chris")

    utils.log_failed_job("https://www.linkedin.com/jobs/view/42", "No Easy Apply")
    utils.write_results("1 | Dev | Acme | * Just Applied to this job: https://www.linkedin.com/jobs/view/7")

    assert utils.get_applied_jobs() == {"42", "7"}


def test_generated_urls_use_active_settings() -> None:
    config.apply_settings(
        {
            "KEYWORDS": ["Python", "Go"],
            "LOCATION": ["Europe"],
            "JOB_TYPE": ["Internship", "Full-time"],
            "REMOTE": ["Remote"],
            "EXPERIENCE_LEVELS": ["Entry level"],
            "SORT": ["Relevant"],
        }
    )

    urls = utils.LinkedinUrlGenerate().generate_url_links()

    assert len(urls) == 2
    assert "keywords=Python" in urls[0] and "keywords=Go" in urls[1]
    assert "geoId=100506914" in urls[0]
    assert "f_JT=I%2CF" in urls[0]
    assert "sort_by=R" in urls[0]


def test_legacy_spellings_still_match() -> None:
    config.apply_settings({"JOB_TYPE": ["Intership"], "SORT": ["Relevent"]})

    assert utils.LinkedinUrlGenerate.job_type() == "&f_JT=I&"
    assert utils.LinkedinUrlGenerate.sort_by() == "&sort_by=R"
