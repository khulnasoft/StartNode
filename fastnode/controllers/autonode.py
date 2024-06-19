from fastapi_sqlalchemy import db
from fastapi import APIRouter
from fastnode.logger.logger import logger
from fastnode.models.requests import Requests
from fastnode.models.types.requests.initiate_fastnode import InitiateFastNodeRequest
from fastnode.utils.helpers.naming_helper import NamingHelper

router = APIRouter()


@router.post("/initiate")
def initiate_fastnode(request: InitiateFastNodeRequest):
    try:
        req = Requests.add_request(session=db.session,
                                   description=request.objective,
                                   url=request.site_url,
                                   graph_path=request.graph_path,
                                   requests_dir=f"requests/{NamingHelper.request_folder_name_generator()}")

        from fastnode.worker import initiate_fastnode

        initiate_fastnode.delay(request_id=req.id,
                                url=request.site_url,
                                objective=request.objective,
                                graph_path=request.graph_path,
                                planner_prompt=request.planner_prompt,
                                screenshots_dir=f"requests/{NamingHelper.request_folder_name_generator()}")

        return {"success": True, "message": f"Initiated FastNode for Request ID {req.id} successfully"}

    except Exception as e:
        logger.error(f"Error initiating Fastnode: {str(e)}")
        return {"success": False, "message": f"Error initiating Fastnode: {e}"}
