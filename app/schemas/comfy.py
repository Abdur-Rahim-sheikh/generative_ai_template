from enum import Enum


class ComfyStatus(str, Enum):
    STATUS = "status"
    PROGRESS_STATE = "progress_state"
    PROGRESS = "progress"
    EXECUTING = "executing"
    EXECUTION_CACHED = "executing_cached"
    EXECUTED = "executed"
    EXECUTION_ERROR = "executing_error"
    PROMPT_QUEUED = "prompt_queued"
    EXECUTION_SUCCESS = "execution_success"

    # this below status to show backend received and now is in pending
    PENDING = "pending"
    # There are others which we won't consider now
    # binary_data, executing_batch, node_output_updated
