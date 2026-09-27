"""
Demo data seeder for the SIH26135 Skilling-to-Employment backend.

Populates: 1 admin, 2 employers, 3 trainees, 4 job roles, 10 skills,
4 jobs with job_requirements, trainee_skills for each trainee, and one
progressed application (APPLIED -> SELECTED) with a matching Employment
record for Phase 8 testing.

Uses the existing SQLAlchemy models, the existing password hashing
function (app.core.security.hash_password), and the existing
DATABASE_URL / session setup. Does NOT touch models, routers, schemas,
auth, matching, recommendation, application, or employment logic.

Idempotent: every entity is looked up by its natural/unique key first
(email, skill name, job_role title, employer+job title, the various
unique-constrained pairs) and only created if missing. Re-running this
script is safe and will not create duplicates or crash on unique
constraint violations. A couple of mutable fields (proficiency/required
level, application status) are refreshed on re-run so the demo data
stays consistent with this script if you tweak the values below.

Run with (see README section this script prints at the end, or the
chat instructions, for exact Windows commands):

    python seed.py
"""

from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.application import JobApplication
from app.models.employer import Employer
from app.models.employment import Employment
from app.models.enums import ApplicationStatus, UserRole
from app.models.job import Job, JobRequirement, JobRole
from app.models.skill import Skill, TraineeSkill
from app.models.trainee import Trainee
from app.models.user import User

DEMO_PASSWORD = "Demo@1234"


# ---------------------------------------------------------------------------
# get-or-create helpers (idempotency)
# ---------------------------------------------------------------------------

def get_or_create_user(db: Session, *, email: str, name: str, role: UserRole) -> tuple[User, bool]:
    user = db.scalar(select(User).where(User.email == email))
    if user is not None:
        return user, False
    user = User(name=name, email=email, password_hash=hash_password(DEMO_PASSWORD), role=role)
    db.add(user)
    db.flush()
    return user, True


def ensure_trainee_profile(db: Session, user: User, *, district: str, education: str, phone: str) -> Trainee:
    trainee = db.scalar(select(Trainee).where(Trainee.user_id == user.id))
    if trainee is None:
        trainee = Trainee(user_id=user.id, district=district, education=education, phone=phone)
        db.add(trainee)
        db.flush()
    return trainee


def ensure_employer_profile(db: Session, user: User, *, company_name: str, location: str) -> Employer:
    employer = db.scalar(select(Employer).where(Employer.user_id == user.id))
    if employer is None:
        employer = Employer(user_id=user.id, company_name=company_name, location=location)
        db.add(employer)
        db.flush()
    return employer


def get_or_create_skill(db: Session, *, name: str, description: str) -> Skill:
    skill = db.scalar(select(Skill).where(Skill.name == name))
    if skill is None:
        skill = Skill(name=name, description=description)
        db.add(skill)
        db.flush()
    return skill


def get_or_create_job_role(db: Session, *, title: str, description: str) -> JobRole:
    role = db.scalar(select(JobRole).where(JobRole.title == title))
    if role is None:
        role = JobRole(title=title, description=description)
        db.add(role)
        db.flush()
    return role


def get_or_create_job(
    db: Session,
    *,
    employer: Employer,
    job_role: JobRole,
    title: str,
    location: str,
    salary_min: float,
    salary_max: float,
    description: str,
) -> Job:
    job = db.scalar(
        select(Job).where(Job.employer_id == employer.id, Job.title == title)
    )
    if job is None:
        job = Job(
            employer_id=employer.id,
            job_role_id=job_role.id,
            title=title,
            location=location,
            salary_min=salary_min,
            salary_max=salary_max,
            description=description,
        )
        db.add(job)
        db.flush()
    return job


def upsert_job_requirement(db: Session, *, job: Job, skill: Skill, required_level: int, required: bool) -> JobRequirement:
    req = db.scalar(
        select(JobRequirement).where(JobRequirement.job_id == job.id, JobRequirement.skill_id == skill.id)
    )
    if req is None:
        req = JobRequirement(job_id=job.id, skill_id=skill.id, required_level=required_level, required=required)
        db.add(req)
        db.flush()
    else:
        req.required_level = required_level
        req.required = required
    return req


def upsert_trainee_skill(db: Session, *, trainee: Trainee, skill: Skill, proficiency_level: int) -> TraineeSkill:
    row = db.scalar(
        select(TraineeSkill).where(TraineeSkill.trainee_id == trainee.id, TraineeSkill.skill_id == skill.id)
    )
    if row is None:
        row = TraineeSkill(trainee_id=trainee.id, skill_id=skill.id, proficiency_level=proficiency_level)
        db.add(row)
        db.flush()
    else:
        row.proficiency_level = proficiency_level
    return row


def get_or_create_application(db: Session, *, job: Job, trainee: Trainee) -> tuple[JobApplication, bool]:
    application = db.scalar(
        select(JobApplication).where(JobApplication.job_id == job.id, JobApplication.trainee_id == trainee.id)
    )
    if application is not None:
        return application, False
    application = JobApplication(job_id=job.id, trainee_id=trainee.id, status=ApplicationStatus.APPLIED)
    db.add(application)
    db.flush()
    return application, True


def get_or_create_employment(db: Session, *, job: Job, trainee: Trainee, joining_date: date, salary: float) -> tuple[Employment, bool]:
    employment = db.scalar(
        select(Employment).where(Employment.job_id == job.id, Employment.trainee_id == trainee.id)
    )
    if employment is not None:
        return employment, False
    employment = Employment(
        trainee_id=trainee.id,
        employer_id=job.employer_id,
        job_role_id=job.job_role_id,
        job_id=job.id,
        joining_date=joining_date,
        salary=salary,
        location=job.location,
        verified=True,
    )
    db.add(employment)
    db.flush()
    return employment, True


# ---------------------------------------------------------------------------
# seed
# ---------------------------------------------------------------------------

def run() -> None:
    db = SessionLocal()
    try:
        # --- users ---------------------------------------------------------
        admin, _ = get_or_create_user(db, email="admin@sih26135-demo.com", name="Platform Admin", role=UserRole.ADMIN)

        emp1_user, _ = get_or_create_user(db, email="employer1@sih26135-demo.com", name="TechNova HR", role=UserRole.EMPLOYER)
        employer1 = ensure_employer_profile(db, emp1_user, company_name="TechNova Solutions", location="Bengaluru")

        emp2_user, _ = get_or_create_user(db, email="employer2@sih26135-demo.com", name="DataWorks HR", role=UserRole.EMPLOYER)
        employer2 = ensure_employer_profile(db, emp2_user, company_name="DataWorks Analytics", location="Pune")

        tr1_user, _ = get_or_create_user(db, email="trainee1@sih26135-demo.com", name="Ayaan Sharma", role=UserRole.TRAINEE)
        trainee1 = ensure_trainee_profile(
            db, tr1_user, district="Bengaluru Urban", education="B.Tech Computer Science", phone="9876500001"
        )

        tr2_user, _ = get_or_create_user(db, email="trainee2@sih26135-demo.com", name="Priya Verma", role=UserRole.TRAINEE)
        trainee2 = ensure_trainee_profile(
            db, tr2_user, district="Pune", education="B.Sc Statistics", phone="9876500002"
        )

        tr3_user, _ = get_or_create_user(db, email="trainee3@sih26135-demo.com", name="Rahul Nair", role=UserRole.TRAINEE)
        trainee3 = ensure_trainee_profile(
            db, tr3_user, district="Ernakulam", education="MCA", phone="9876500003"
        )

        db.commit()

        # --- skills ----------------------------------------------------------
        skill_defs = [
            ("Python", "General-purpose programming language"),
            ("SQL", "Relational database querying"),
            ("JavaScript", "Web scripting language"),
            ("React", "Frontend UI library"),
            ("FastAPI", "Python web framework for APIs"),
            ("Docker", "Containerization tool"),
            ("Git", "Version control"),
            ("Data Analysis", "Extracting insights from data"),
            ("Machine Learning", "Building predictive models"),
            ("Communication", "Verbal and written communication"),
        ]
        skills = {name: get_or_create_skill(db, name=name, description=desc) for name, desc in skill_defs}
        db.commit()

        # --- job roles ---------------------------------------------------------
        role_backend = get_or_create_job_role(db, title="Backend Developer", description="Server-side APIs and services")
        role_frontend = get_or_create_job_role(db, title="Frontend Developer", description="Client-side web interfaces")
        role_data_analyst = get_or_create_job_role(db, title="Data Analyst", description="Business data insights")
        role_data_scientist = get_or_create_job_role(db, title="Data Scientist", description="ML-driven products")
        db.commit()

        # --- jobs ----------------------------------------------------------
        job_backend = get_or_create_job(
            db,
            employer=employer1,
            job_role=role_backend,
            title="Backend Developer - Python APIs",
            location="Bengaluru",
            salary_min=600000,
            salary_max=900000,
            description="Build and maintain FastAPI services backed by PostgreSQL.",
        )
        job_frontend = get_or_create_job(
            db,
            employer=employer1,
            job_role=role_frontend,
            title="Frontend Developer - React",
            location="Bengaluru",
            salary_min=500000,
            salary_max=800000,
            description="Build React interfaces for internal tools.",
        )
        job_data_analyst = get_or_create_job(
            db,
            employer=employer2,
            job_role=role_data_analyst,
            title="Data Analyst - Business Insights",
            location="Pune",
            salary_min=500000,
            salary_max=750000,
            description="Turn raw data into dashboards and reports.",
        )
        job_data_scientist = get_or_create_job(
            db,
            employer=employer2,
            job_role=role_data_scientist,
            title="Data Scientist - ML Products",
            location="Pune",
            salary_min=800000,
            salary_max=1200000,
            description="Design and ship ML models for production use.",
        )
        db.commit()

        # --- job requirements ------------------------------------------------
        requirements = [
            (job_backend, "Python", 4, True),
            (job_backend, "SQL", 3, True),
            (job_backend, "FastAPI", 3, True),
            (job_backend, "Docker", 2, False),
            (job_backend, "Git", 2, False),
            (job_frontend, "JavaScript", 4, True),
            (job_frontend, "React", 4, True),
            (job_frontend, "Git", 2, True),
            (job_frontend, "Communication", 2, False),
            (job_data_analyst, "SQL", 4, True),
            (job_data_analyst, "Data Analysis", 4, True),
            (job_data_analyst, "Communication", 3, True),
            (job_data_analyst, "Python", 2, False),
            (job_data_scientist, "Python", 4, True),
            (job_data_scientist, "Machine Learning", 4, True),
            (job_data_scientist, "SQL", 3, True),
            (job_data_scientist, "Data Analysis", 3, False),
        ]
        for job, skill_name, level, required in requirements:
            upsert_job_requirement(db, job=job, skill=skills[skill_name], required_level=level, required=required)
        db.commit()

        # --- trainee skills ------------------------------------------------
        # trainee1: strong backend match
        trainee1_skills = [("Python", 4), ("SQL", 3), ("FastAPI", 3), ("Git", 3), ("Docker", 2)]
        # trainee2: strong data-analyst match
        trainee2_skills = [("SQL", 4), ("Data Analysis", 4), ("Communication", 3), ("Python", 2)]
        # trainee3: partial frontend match, weak elsewhere (shows skill gaps)
        trainee3_skills = [("JavaScript", 3), ("React", 2), ("Git", 2)]

        for skill_name, level in trainee1_skills:
            upsert_trainee_skill(db, trainee=trainee1, skill=skills[skill_name], proficiency_level=level)
        for skill_name, level in trainee2_skills:
            upsert_trainee_skill(db, trainee=trainee2, skill=skills[skill_name], proficiency_level=level)
        for skill_name, level in trainee3_skills:
            upsert_trainee_skill(db, trainee=trainee3, skill=skills[skill_name], proficiency_level=level)
        db.commit()

        # --- Phase 8 demo: trainee1 -> SELECTED application -> Employment ---
        application, app_created = get_or_create_application(db, job=job_backend, trainee=trainee1)
        if application.status != ApplicationStatus.SELECTED:
            application.status = ApplicationStatus.SELECTED
        db.commit()

        employment, employment_created = get_or_create_employment(
            db,
            job=job_backend,
            trainee=trainee1,
            joining_date=date.today() + timedelta(days=14),
            salary=750000,
        )
        db.commit()

        # --- summary ---------------------------------------------------------
        print("Seed complete.\n")
        print(f"Demo password for every seeded account: {DEMO_PASSWORD}\n")
        print("Accounts:")
        print(f"  ADMIN    admin@sih26135-demo.com")
        print(f"  EMPLOYER employer1@sih26135-demo.com  (TechNova Solutions, id={employer1.id})")
        print(f"  EMPLOYER employer2@sih26135-demo.com  (DataWorks Analytics, id={employer2.id})")
        print(f"  TRAINEE  trainee1@sih26135-demo.com   (Ayaan Sharma, id={trainee1.id})")
        print(f"  TRAINEE  trainee2@sih26135-demo.com   (Priya Verma, id={trainee2.id})")
        print(f"  TRAINEE  trainee3@sih26135-demo.com   (Rahul Nair, id={trainee3.id})")
        print()
        print("Jobs:")
        print(f"  {job_backend.id}  Backend Developer - Python APIs (TechNova)")
        print(f"  {job_frontend.id}  Frontend Developer - React (TechNova)")
        print(f"  {job_data_analyst.id}  Data Analyst - Business Insights (DataWorks)")
        print(f"  {job_data_scientist.id}  Data Scientist - ML Products (DataWorks)")
        print()
        print("Phase 8 demo data:")
        print(f"  Application {application.id}: trainee1 -> Backend Developer job, status=SELECTED")
        print(f"  Employment  {employment.id}: trainee1 employed at TechNova as Backend Developer")
        print()
        print("Suggested match/skill-gap/recommendation checks:")
        print(f"  trainee1 vs Backend job  {job_backend.id}   -> expect a high match_percentage")
        print(f"  trainee2 vs Data Analyst {job_data_analyst.id} -> expect a high match_percentage")
        print(f"  trainee3 vs Frontend job {job_frontend.id}  -> expect a partial match with visible skill_gaps")
    finally:
        db.close()


if __name__ == "__main__":
    run()