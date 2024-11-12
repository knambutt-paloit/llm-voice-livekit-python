import json
import os
from typing import Annotated, Dict, List

from livekit.agents import llm

from db.consultant_db import PALO_IT_CONSULTANTS


class PaloConsultFunction(llm.FunctionContext):
    """
    Function to get PALO IT Consultants/Employee information based on criteria.
    """

    @llm.ai_callable()
    async def consult_info(
        self,
        department: Annotated[
            str, llm.TypeInfo(description="Department of the consultant. Options: Technology, Sustainability, Agile, Design, DevOps")
        ],
        skill: Annotated[str, llm.TypeInfo(description="Required skill of the consultant")],
        certification: Annotated[str, llm.TypeInfo(description="Required certification of the consultant")]
    ) -> List[Dict[str, str]]:
        """Get PALO IT Consultants/Employee information based on department, skill, and certification."""

        print(f"Executing PALO Consultants function with department={department}, skill={skill}, certification={certification}")

        # Filter consultants by department
        filtered_consultants = [
            consultant for consultant in PALO_IT_CONSULTANTS
            if department.lower() in (consultant.get("department") or "").lower()
        ] if department else PALO_IT_CONSULTANTS

        # Filter by skill
        if skill:
            skill_parts = skill.lower().split()
            filtered_consultants = [
                consultant for consultant in filtered_consultants
                if any(
                    all(sub_skill in consultant_skill.lower() for sub_skill in skill_parts)
                    for consultant_skill in consultant.get("skills", [])
                )
            ]

        # Filter by certification
        if certification:
            cert_parts = certification.lower().split()
            filtered_consultants = [
                consultant for consultant in filtered_consultants
                if any(
                    all(sub_cert in consultant_cert.lower() for sub_cert in cert_parts)
                    for consultant_cert in consultant.get("certifications", [])
                )
            ]

        # If no consultants match, return the full list as fallback
        if not filtered_consultants:
            filtered_consultants = PALO_IT_CONSULTANTS

        # Convert the result to JSON string to match the TypeScript behavior
        return json.dumps(filtered_consultants)