from pickle import load, loads
from subprocess import run, PIPE
from numpy.testing import assert_almost_equal
from shlex import split

import pytest
import numpy as np

cmd = ["python3", "-m" "coherent_point_drift.main"]

def test_align():
    args = split("align tests/fixtures/ref.pickle tests/fixtures/deg.pickle --format pickle")
    with open("tests/fixtures/xform.pickle", "rb") as f:
        expected = load(f)

    r = run(cmd + args, stdout=PIPE, universal_newlines=False)
    assert not r.returncode
    result = loads(r.stdout)

    for r, e in zip(result, expected):
        assert_almost_equal(r, e)

def test_xform_inverse(tmpdir):
    with open("tests/fixtures/ref.pickle", "rb") as f:
        expected = load(f)

    # Generate degraded points (without noise)
    args = split("xform tests/fixtures/ref.pickle tests/fixtures/xform.pickle --format pickle")
    r = run(cmd + args, stdout=PIPE, universal_newlines=False)
    assert not r.returncode
    deg = tmpdir.join("deg.pickle")
    deg.write_binary(r.stdout)

    # Generate alignment
    args = split("align tests/fixtures/ref.pickle '{}' --format pickle".format(str(deg)))
    r = run(cmd + args, stdout=PIPE, universal_newlines=False)
    assert not r.returncode
    xform = tmpdir.join("xform.pickle")
    xform.write_binary(r.stdout)

    # Check alignment xform
    args = split("xform '{}' '{}' --format pickle".format(str(deg), str(xform)))
    r = run(cmd + args, stdout=PIPE, universal_newlines=False)
    assert not r.returncode
    result = loads(r.stdout)
    assert_almost_equal(expected, result)


def test_print(tmpdir):
    with open("tests/fixtures/ref.pickle", "rb") as f:
        expected = load(f)

    # Generate degraded points (without noise)
    args = split("xform tests/fixtures/ref.pickle tests/fixtures/xform.pickle --format pickle")
    r = run(cmd + args, stdout=PIPE, universal_newlines=False)
    assert not r.returncode
    deg = tmpdir.join("deg.pickle")
    deg.write_binary(r.stdout)

    # Generate alignment
    args = split("align tests/fixtures/ref.pickle '{}' --format print".format(str(deg)))
    r = run(cmd + args, stdout=PIPE, universal_newlines=False)
    assert not r.returncode

def test_align_multiple():
    args = split(
        "align tests/fixtures/ref.pickle tests/fixtures/deg.pickle "
        "tests/fixtures/ref.pickle tests/fixtures/deg.pickle "
        "-w {w} --format pickle".format(w=2/3)
    )
    with open("tests/fixtures/xform.pickle", "rb") as f:
        expected = load(f)

    r = run(cmd + args, stdout=PIPE, universal_newlines=False)
    assert not r.returncode
    result = loads(r.stdout)

    for r, e in zip(result, expected):
        assert_almost_equal(r, e)

def test_align_multiple_w():
    args = split(
        "align tests/fixtures/ref.pickle tests/fixtures/deg.pickle "
        "tests/fixtures/ref.pickle tests/fixtures/deg.pickle "
        "-w 0.5 0.8 --format pickle"
    )

    r = run(cmd + args, stdout=PIPE, universal_newlines=False)
    assert not r.returncode

def test_plot_multiple(tmpdir):
    args = split(
        "plot tests/fixtures/ref.pickle tests/fixtures/deg.pickle "
        "tests/fixtures/ref.pickle tests/fixtures/deg.pickle "
        "tests/fixtures/xform.pickle --outfile {}".format(tmpdir.join('test.pdf'))
    )
    r = run(cmd + args, stdout=PIPE, universal_newlines=False)
    assert not r.returncode

def test_global_multiple():
    args = split(
        "align tests/fixtures/ref.pickle tests/fixtures/deg.pickle "
        "tests/fixtures/ref.pickle tests/fixtures/deg.pickle "
        "--format pickle --scope global -w {w}".format(w=2/3)
    )
    with open("tests/fixtures/xform.pickle", "rb") as f:
        expected = load(f)

    r = run(cmd + args, stdout=PIPE, universal_newlines=False)
    assert not r.returncode
    result = loads(r.stdout)

    for r, e in zip(result, expected):
        assert_almost_equal(r, e)

def test_plot_sizes(tmpdir):
    for sizes in ["1.0", "0.5 1.0"]:
        args = split(
            "plot tests/fixtures/ref.pickle tests/fixtures/deg.pickle "
            "tests/fixtures/ref.pickle tests/fixtures/deg.pickle "
            "tests/fixtures/xform.pickle --sizes {} --outfile {}"
            .format(sizes, tmpdir.join('test.pdf'))
        )
        r = run(cmd + args, stdout=PIPE, universal_newlines=False)
        assert not r.returncode
