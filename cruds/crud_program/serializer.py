from . import models
from cruds.crud_institution.serializer import InstitutionSerializer
from cruds.crud_institution.models import Institution
from cruds.crud_courses.serializer import CoursesSerializer
from cruds.crud_users.models import Users


class ProgramSerializer:

    def serialize(self, programs):
        data = []
        for program in programs:
            institution = Institution.query.get(program.institution_id)
            courses =  program.courses
            # coordinator =  Users.query.get(program.coordinator_id)

            data.append({
                'id': program.id,
                'name': program.name,
                'abbreviation': program.abbreviation,
                'total_hours': program.total_hours,
                'total_credits':  program.total_credits,
                'courses': CoursesSerializer().serialize(courses),
                'institution': InstitutionSerializer().serialize([institution])
                # 'coordinator_id': dict(id=coordinator.id, email=coordinator.email, name=coordinator.name)
            })

        return data
