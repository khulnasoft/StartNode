from fastapi_sqlalchemy import db
from fastapi import APIRouter
from startnode.logger.logger import logger
from startnode.models.requests import Requests
from startnode.models.types.requests.initiate_startnode import InitiateAutoNodeRequest
from startnode.utils.helpers.naming_helper import NamingHelper

router = APIRouter()


@router.post("/initiate")
def initiate_startnode(request: InitiateAutoNodeRequest):
    try:
        req = Requests.add_request(session=db.session,
                                   description=request.objective,
                                   url=request.site_url,
                                   graph_path=request.graph_path,
                                   requests_dir=f"requests/{NamingHelper.request_folder_name_generator()}")

        from startnode.worker import initiate_startnode

        initiate_startnode.delay(request_id=req.id,
                                url=request.site_url,
                                objective=request.objective,
                                graph_path=request.graph_path,
                                planner_prompt=request.planner_prompt,
                                screenshots_dir=f"requests/{NamingHelper.request_folder_name_generator()}")

        return {"success": True, "message": f"Initiated AutoNode for Request ID {req.id} successfully"}

    except Exception as e:
        logger.error(f"Error initiating Startnode: {str(e)}")
        return {"success": False, "message": f"Error initiating Startnode: {e}"}
