from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

def create_progress_bar():
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None, style="bold orange3"),
        TaskProgressColumn(),
        TextColumn("({task.completed}/{task.total})"),
    )
