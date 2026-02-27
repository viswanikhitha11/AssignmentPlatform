from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Assignment, Submission, PeerReview


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("dashboard")
        return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def assignment_list(request):
    now = timezone.now()

    if request.user.is_staff:
        assignments = Assignment.objects.filter(created_by=request.user)
    else:
        assignments = Assignment.objects.all()

        # 🔥 Attach student's submission to each assignment
        for a in assignments:
            a.submission = Submission.objects.filter(
                assignment=a,
                student=request.user
            ).first()

    return render(request, "assignment_list.html", {
        "assignments": assignments,
        "now": now
    })

@login_required
def create_assignment(request):
    if not request.user.is_staff:
        return redirect("dashboard")

    if request.method == "POST":
        Assignment.objects.create(
            title=request.POST["title"],
            subject=request.POST["subject"],
            description=request.POST["description"],
            deadline=request.POST["deadline"],
            created_by=request.user
        )
        return redirect("assignment_list")

    return render(request, "create_assignment.html")


@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # 🚫 Block resubmission
    existing = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).exists()

    if existing:
        return redirect("assignment_list")

    if request.method == "POST":
        file = request.FILES.get("file")

        if not file:
            return render(request, "submit_assignment.html", {
                "assignment": assignment,
                "error": "Please upload a file"
            })

        Submission.objects.create(
            assignment=assignment,
            student=request.user,
            file=file
        )

        return redirect("assignment_list")

    return render(request, "submit_assignment.html", {
        "assignment": assignment
    })
@login_required
def review_submissions(request, assignment_id):
    if not request.user.is_staff:
        return redirect("dashboard")

    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = assignment.submissions.select_related("student")

    return render(request, "review_submissions.html", {
        "assignment": assignment,
        "submissions": submissions
    })


@login_required
def grade_submission(request, submission_id):
    if not request.user.is_staff:
        return redirect("dashboard")

    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == "POST":
        submission.grade = request.POST["grade"]
        submission.feedback = request.POST["feedback"]
        submission.save()
        return redirect("review_submissions", submission.assignment.id)

    return render(request, "grade_submission.html", {"submission": submission})