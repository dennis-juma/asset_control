from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from employees.repositories.employee import EmployeeRepository


@method_decorator(login_required, name="dispatch")
class EmployeeAutocompleteView(View):

    def get(self, request):
        q = request.GET.get("q", "").strip()
        repo = EmployeeRepository()
        # reuse repository search but limit results for autocomplete
        page = repo.list(query=q, page=1, per_page=10)

        results = []
        for emp in page.object_list:
            results.append({
                "id": str(emp.pk),
                "text": f"{emp.employee_id} - {emp.full_name}",
                "employee_id": emp.employee_id,
                "email": emp.email or "",
            })

        return JsonResponse({
            "results": results,
        })
