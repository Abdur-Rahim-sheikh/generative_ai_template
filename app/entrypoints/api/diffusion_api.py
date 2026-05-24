from arq.connections import ArqRedis
from arq.jobs import Job, JobStatus
from fastapi import APIRouter, Depends, HTTPException

from ...dependencies import get_job_queue
from ...schemas.common import JobResponse, StatusResponse
from ...schemas.image import PromptAndImageToImageRequest, PromptToImageRequest
from ...utils.image import decode_base64_to_bytes
from ...utils.watermark import auto_watermark
from ...dependencies.auth import get_user_wallet_id
from typing import Annotated
from ...config import ProductTitle

router = APIRouter()


@router.post("/product-image/enqueue")
async def enqueue_product_image(
    request: PromptAndImageToImageRequest,
    wallet_id: Annotated[str, Depends(get_user_wallet_id)],
    queue: ArqRedis = Depends(get_job_queue),
):

    image = decode_base64_to_bytes(b64=request.base64_image)
    prompt = (
        "Keep the product geometry, branding, and color unchanged. Remove the original background entirely."
        + request.prompt
    )
    job = await queue.enqueue_job(
        "product_photography",
        wallet_id,
        ProductTitle.PRODUCT_IMAGE,
        image,
        prompt,
        request.width,
        request.height,
        request.batch,
    )

    return JobResponse(job_id=job.job_id)


@router.post("/realistic-image/enqueue")
async def enqueue_realistic_image(
    request: PromptToImageRequest,
    wallet_id: Annotated[str, Depends(get_user_wallet_id)],
    queue: ArqRedis = Depends(get_job_queue),
):
    job = await queue.enqueue_job(
        "realistic_image",
        wallet_id,
        ProductTitle.REALISTIC_IMAGE,
        request.prompt,
        request.width,
        request.height,
        request.batch,
    )
    return JobResponse(job_id=job.job_id)


@router.get("/get-status/{job_id}")
async def get_status(job_id: str, queue: ArqRedis = Depends(get_job_queue)):
    job = Job(job_id=job_id, redis=queue)
    status = await job.status()

    if status == JobStatus.not_found:
        # further check here
        raise HTTPException(status_code=400, detail="Job id is invalid")

    message = f"Job is in {status.value} state"
    results = None
    if status == JobStatus.complete:
        result_info = await job.result_info()
        message = "Something went wrong during processing"
        if result_info.success:
            message = "Image processed successfully"
            results = result_info.results
            results = [auto_watermark(r) for r in results]

    return StatusResponse(status=status, message=message, results=results)
