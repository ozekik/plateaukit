import traceback
from concurrent.futures import Future
from multiprocessing import Event
from multiprocessing.pool import Pool

from plateaukit.logger import logger


def wait_futures(
    futures: Future,
    pool: Pool,
    quit: Event,
    futures_status: dict,
    overall_progress,
    rich_progress,
    shared_progress_status,
):
    def catch_exception(future):
        try:
            future.result()
        except KeyboardInterrupt:
            quit.set()
            pool.shutdown(wait=True, cancel_futures=True)
            raise
        except Exception as e:
            # logger.error(e)
            traceback.print_exc()
            futures_status[future]["failed"] = True

    for future in futures:
        future.add_done_callback(catch_exception)

    try:
        n_futures = len(futures)
        while (n_finished := sum([future.done() for future in futures])) < len(futures):
            for task_id, status in shared_progress_status.items():
                latest = status["progress"]
                total = status["total"]

                rich_progress.update(
                    task_id,
                    completed=latest,
                    total=total,
                    visible=latest < total,
                )

            rich_progress.update(
                overall_progress["task_id"],
                completed=sum(
                    [
                        1
                        for future, f in futures_status.items()
                        if future.done() and f["failed"] is not True
                    ]
                ),
                total=n_futures,
            )

        for f in futures_status.values():
            if f["failed"] is True:
                rich_progress.update(
                    f["task_id"],
                    description=f"[cyan]Progress #{f['counter']} [red]Failed",
                )

        # Finish up the overall progress bar
        rich_progress.update(
            overall_progress["task_id"],
            completed=sum(
                [
                    1
                    for future, f in futures_status.items()
                    if future.done() and f["failed"] is not True
                ]
            ),
            total=n_futures,
            description=f"{overall_progress['description']} [green]Done",
        )

    except KeyboardInterrupt:
        quit.set()
        pool.shutdown(wait=True, cancel_futures=True)
        # pool._processes.clear()
        # concurrent.futures.thread._threads_queues.clear()
        raise