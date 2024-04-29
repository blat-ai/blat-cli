from blat_cli.init.command import install_playwright


def test_install_playwright(tmp_path):
    install_playwright(tmp_path, with_deps=False)

    assert len(list(tmp_path.glob("*chromium*"))) == 1
