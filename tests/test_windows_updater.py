import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class WindowsUpdaterSourceTests(unittest.TestCase):
    def test_embedded_python_uses_temporary_script_instead_of_dash_c(self):
        script = (PROJECT_ROOT / "update_fork.ps1").read_text(
            encoding="utf-8-sig"
        )
        merge_code = script.split("$mergeCode = @'", 1)[1].split("\n'@", 1)[0]

        self.assertIn("function Invoke-UpdatePythonCode", script)
        self.assertIn("[IO.File]::WriteAllText", script)
        self.assertIn("Remove-Item -LiteralPath $tempScriptPath", script)
        self.assertIn("Invoke-UpdatePythonCode -Code $validateCode", script)
        self.assertIn("Invoke-UpdatePythonCode -Code $mergeCode", script)
        self.assertNotIn('"-c", $mergeCode', script)
        self.assertNotIn('"-c", $validateCode', script)
        self.assertIn("legacy_schedule_defaults", merge_code)
        compile(merge_code, "<update_fork.ps1 merge code>", "exec")

    def test_untracked_config_probe_does_not_emit_pathspec_error(self):
        script = (PROJECT_ROOT / "update_fork.ps1").read_text(
            encoding="utf-8-sig"
        )

        self.assertIn("function Test-GitTrackedPath", script)
        self.assertNotIn('"ls-files", "--error-unmatch"', script)

    def test_backup_retention_is_bounded_and_noop_is_detected(self):
        script = (PROJECT_ROOT / "update_fork.ps1").read_text(
            encoding="utf-8-sig"
        )

        self.assertIn('"bestcfcdn_backup_latest"', script)
        self.assertNotIn('Get-Date -Format "yyyyMMdd_HHmmss_fff"', script)
        self.assertIn("UPDATE_BACKUP_RETENTION", script)
        self.assertIn("Set-ManagedBackupRetention", script)
        self.assertIn("Remove-ManagedBackupDirectories", script)
        self.assertIn("未创建新备份", script)
        self.assertLess(
            script.index("未创建新备份"),
            script.index('$BackupDir = Join-Path $HOME "bestcfcdn_backup_latest"'),
        )


if __name__ == "__main__":
    unittest.main()
