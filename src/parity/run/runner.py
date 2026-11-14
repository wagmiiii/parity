"""Resumable and idempotent model runner across conditions and splits."""

from pathlib import Path

from parity.schemas import Response, RunConfig


class Runner:
    """Manages prompt execution, checkpointing, and idempotency."""

    def __init__(self, run_config: RunConfig, output_dir: Path | str = "runs"):
        self.config = run_config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.output_file = self.output_dir / f"{run_config.run_id}.jsonl"
        self._completed_keys: set[tuple[str, str, str]] = set()
        self._load_existing_checkpoint()

    def _load_existing_checkpoint(self) -> None:
        """Read existing responses to allow resuming interrupted runs."""
        if self.output_file.exists():
            with open(self.output_file, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        r = Response.model_validate_json(line)
                        self._completed_keys.add((r.run_id, r.prompt_id, r.variant))

    def is_completed(self, prompt_id: str, variant: str) -> bool:
        """Check if this specific variant has already been executed."""
        return (self.config.run_id, prompt_id, variant) in self._completed_keys

    def record_response(self, response: Response) -> None:
        """Append response to output file and update in-memory key set."""
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(response.model_dump_json() + "\n")
        self._completed_keys.add((response.run_id, response.prompt_id, response.variant))
