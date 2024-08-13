import concurrent.futures
from multiprocessing import Manager
from pathlib import Path

from rich.progress import Progress

from plateaukit import parallel


class ParallelWriter:
    def __init__(self, writer_cls):
        self.writer = writer_cls()

    def transform(
        self,
        readable,
        outfile: str,
        split=2,
        **kwargs,
    ):
        batches = readable.split(split)

        progress_state = {}
        writer = self.writer

        with Progress() as rprogress:
            overall_progress_description = progress_state.get(
                "description", "Processing..."
            )
            overall_task_id = rprogress.add_task(overall_progress_description)

            with Manager() as manager:
                quit = manager.Event()
                _progress = manager.dict()

                with concurrent.futures.ProcessPoolExecutor(max_workers=None) as pool:
                    futures = []
                    futures_status = dict()
                    for i, batch in enumerate(batches):
                        stem = Path(outfile).stem
                        if split > 1:
                            batch_outfile = Path(outfile).with_stem(f"{stem}.{i + 1}")
                        else:
                            batch_outfile = outfile

                        # task_id = rprogress.add_task(
                        #     f"[cyan]Progress #{i + 1}", total=len(batch)
                        # )

                        # logger.debug(f"batch_outfile: {batch_outfile}")

                        future = pool.submit(
                            writer.write_to,
                            batch,
                            batch_outfile,
                            **kwargs,
                        )

                        futures.append(future)
                        futures_status[future] = {
                            "task_id": i + 1,
                            "counter": i + 1,
                            "failed": False,
                        }

                    parallel.wait_futures(
                        futures,
                        pool,
                        quit,
                        futures_status,
                        overall_progress={
                            "task_id": overall_task_id,
                            "description": overall_progress_description,
                        },
                        rich_progress=rprogress,
                        shared_progress_status=_progress,
                    )
