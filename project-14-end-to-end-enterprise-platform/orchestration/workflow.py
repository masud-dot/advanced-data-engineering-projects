import time


class PipelineWorkflow:
    """Orchestrates enterprise data-platform pipeline stages."""

    def __init__(self, retries=3, retry_delay_seconds=5):
        self.retries = retries
        self.retry_delay_seconds = retry_delay_seconds

    def run_stage(self, name, function):
        attempts = 0
        last_error = None

        while attempts <= self.retries:
            attempts += 1

            try:
                result = function()

                return {
                    "stage": name,
                    "status": "SUCCESS",
                    "attempts": attempts,
                    "result": result,
                }

            except Exception as exc:
                last_error = str(exc)

                if attempts <= self.retries:
                    time.sleep(self.retry_delay_seconds)

        return {
            "stage": name,
            "status": "FAILED",
            "attempts": attempts,
            "error": last_error,
        }


    def run(self, stages):
        results = []

        for name, function in stages:
            result = self.run_stage(name, function)
            results.append(result)

            if result["status"] == "FAILED":
                return {
                    "status": "FAILED",
                    "stages": results,
                }

        return {
            "status": "SUCCESS",
            "stages": results,
        }
