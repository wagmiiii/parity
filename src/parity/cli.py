"""Command-line interface for the Parity audit and repair pipeline."""

from typing import Annotated

import typer
from rich.console import Console

app = typer.Typer(
    name="parity",
    help="Parity: Audit and repair identity-based treatment gaps in small multilingual LLMs.",
    no_args_is_help=True,
)
console = Console()


@app.command("build")
def build(
    groups_config: Annotated[
        str, typer.Option("--groups", "-g", help="Path to groups.yaml configuration")
    ] = "configs/groups.yaml",
    seeds_dir: Annotated[
        str, typer.Option("--seeds", "-s", help="Path to seed templates directory")
    ] = "data/seeds",
    output_dir: Annotated[
        str, typer.Option("--output", "-o", help="Output directory for generated benchmark")
    ] = "data/build/v0.1",
) -> None:
    """Build benign minimal pairs, harmful prompts, and control prompts."""
    console.print(f"[bold green]Building benchmark[/bold green] from {seeds_dir} -> {output_dir}")
    # Skeleton stub


@app.command("validate")
def validate(
    input_dir: Annotated[
        str, typer.Option("--input", "-i", help="Directory containing built benchmark datasets")
    ] = "data/build/v0.1",
    freeze_dir: Annotated[
        str, typer.Option("--freeze", "-f", help="Target directory for frozen benchmark")
    ] = "data/frozen/v0.1",
) -> None:
    """Validate minimal pair properties, human review flags, and freeze with checksums."""
    console.print(
        f"[bold green]Validating and freezing[/bold green] from {input_dir} -> {freeze_dir}"
    )
    # Skeleton stub


@app.command("run")
def run(
    condition: Annotated[
        str,
        typer.Option(
            "--condition", "-c", help="Execution condition: baseline | steered | sysprompt"
        ),
    ] = "baseline",
    split: Annotated[
        str, typer.Option("--split", help="Target dataset split: dev | test | pilot")
    ] = "dev",
    model_id: Annotated[
        str, typer.Option("--model", "-m", help="Target Hugging Face model ID")
    ] = "CohereLabs/tiny-aya-global",
    output_dir: Annotated[
        str, typer.Option("--output", "-o", help="Directory to save run responses")
    ] = "runs",
) -> None:
    """Execute model inference over benchmark prompts and record responses."""
    console.print(
        f"[bold green]Running model[/bold green] {model_id} on condition={condition}, split={split}"
    )
    # Skeleton stub


@app.command("label")
def label(
    run_dir: Annotated[
        str, typer.Option("--run-dir", "-r", help="Directory of run responses")
    ] = "runs",
    split: Annotated[
        str, typer.Option("--split", help="Target dataset split: dev | test | pilot")
    ] = "dev",
    use_judge: Annotated[
        bool,
        typer.Option("--judge/--no-judge", help="Whether to run LLM judge for ambiguous cases"),
    ] = False,
) -> None:
    """Label model responses using refusal detector rules and optional LLM judge."""
    console.print(f"[bold green]Labeling responses[/bold green] in {run_dir} for split={split}")
    # Skeleton stub


@app.command("analyze")
def analyze(
    run_dir: Annotated[
        str, typer.Option("--run-dir", "-r", help="Directory of labeled responses")
    ] = "runs",
    output_dir: Annotated[
        str, typer.Option("--output", "-o", help="Directory to save report tables and metrics")
    ] = "reports/results",
    split: Annotated[
        str, typer.Option("--split", help="Split to analyze: dev | test | pilot")
    ] = "dev",
) -> None:
    """Compute IRG, THC, CORR, and QPG with bootstrap confidence intervals and McNemar tests."""
    console.print(f"[bold green]Analyzing metrics[/bold green] for split={split} -> {output_dir}")
    # Skeleton stub


@app.command("repair-fit")
def repair_fit(
    config_path: Annotated[
        str, typer.Option("--config", "-c", help="Path to repair.yaml configuration")
    ] = "configs/repair.yaml",
    dev_data: Annotated[
        str, typer.Option("--data", "-d", help="Dev split responses and labels")
    ] = "runs",
    output_artifact: Annotated[
        str, typer.Option("--output", "-o", help="Output path for fitted repair artifact")
    ] = "artifacts/steering_vectors.pt",
) -> None:
    """Fit inference-time steering vectors or LoRA adapter on dev split only."""
    console.print(f"[bold green]Fitting repair[/bold green] on dev split -> {output_artifact}")
    # Skeleton stub


@app.command("publish")
def publish(
    results_dir: Annotated[
        str, typer.Option("--results", "-r", help="Directory containing final metrics and figures")
    ] = "reports/results",
    repo_prefix: Annotated[
        str, typer.Option("--prefix", "-p", help="Hugging Face repo prefix")
    ] = "parity",
) -> None:
    """Publish frozen benchmark, responses, labels, model cards, and Space to Hugging Face."""
    console.print(
        f"[bold green]Publishing artifacts[/bold green] to Hugging Face under prefix {repo_prefix}"
    )
    # Skeleton stub


if __name__ == "__main__":
    app()
