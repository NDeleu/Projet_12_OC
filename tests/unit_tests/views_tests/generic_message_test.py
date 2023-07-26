from app.views.general_views.generic_message import (
    display_message_error,
    display_message_success,
    display_message_correction,
    display_message_info
)


def test_display_message_success(capsys):
    display_message_success("This is a success message.")
    captured_stdout = capsys.readouterr().out
    assert "SUCCESS: This is a success message." in captured_stdout


def test_display_message_error(capsys):
    display_message_error("This is an error message.")
    captured_stdout = capsys.readouterr().out
    assert "ERROR: This is an error message." in captured_stdout


def test_display_message_info(capsys):
    display_message_info("This is an info message.")
    captured_stdout = capsys.readouterr().out
    assert "This is an info message." in captured_stdout


def test_display_message_correction(capsys):
    display_message_correction("This is a correction message.")
    captured_stdout = capsys.readouterr().out
    assert "CARE: This is a correction message." in captured_stdout
