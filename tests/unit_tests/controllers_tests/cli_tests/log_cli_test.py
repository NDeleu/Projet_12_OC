from click.testing import CliRunner
from app.controllers.auth_controllers.log_cli import login, logout
from unittest.mock import patch
import pytest


def test_login_logout_cli(db_session, admin_user):
    runner = CliRunner()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(login, [admin_user.email, "password"], obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert f"Collaborator {admin_user.role} logged in successfully" in result.output.strip()

    # Mock the get_logged_as_user function to return the admin_user
    with patch("app.controllers.auth_controllers.permission_controller.get_logged_as_user", return_value=admin_user):
        # Use `invoke` with `obj` argument to pass `db_session` to the command
        result = runner.invoke(logout, obj=db_session)

    # Vérifier que la commande s'est exécutée avec succès
    assert result.exit_code == 0

    assert "User logged out successfully" in result.output.strip()
