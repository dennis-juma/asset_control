from django import forms

from employees.models import Employee

from django.contrib.auth import get_user_model


User = get_user_model()


class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = Employee

        fields = [
            "company",
            "site",
            "department",
            "job_title",
            "manager",
            "employee_id",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "joining_date",
            "last_working_date",
            "phone",
            "email",
            "photo",
            "user",
            "remarks",
        ]


        widgets = {
            "joining_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "last_working_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "remarks": forms.Textarea(
                attrs={"rows": 3},
            ),
        }
        def __init__(self, *args, **kwargs):

            super().__init__(*args, **kwargs)

            self.fields["user"].queryset = (
                User.objects
                .filter(employee__isnull=True)
                .order_by("username")
            )


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee

        fields = [
            "company",
            "site",
            "department",
            "job_title",
            "manager",
            "employee_id",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "joining_date",
            "last_working_date",
            "phone",
            "email",
            "photo",
            "user",
            "remarks",
            "is_active",
        ]

        widgets = {
            "joining_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "last_working_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "remarks": forms.Textarea(
                attrs={"rows": 3},
            ),
        }