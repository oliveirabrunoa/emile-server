from . import models


class CourseTypeSerializer:

    def serialize(self, course_types):
        data = []
        for course_type in course_types:
            data.append({
                'id': course_type.id,
                'description': course_type.description
            })

        return data if len(data) > 1 else data[0]
