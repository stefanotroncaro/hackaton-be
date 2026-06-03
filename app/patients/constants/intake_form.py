from app.patients.schemas.intake_schema import (
    IntakeQuestion,
    IntakeQuestionType,
    PsychiatricIntakeFormDefinition,
    Symptom,
    SymptomDuration,
)

# The psychiatric intake form presented to invited patients.
#
# This is hardcoded question-by-question on purpose. It is NOT built by
# iterating over a config, so it cannot be extended by appending to a list.
# Every question below is wired by hand to a field on `IntakeAnswers` and to a
# column on the `Patient` model. Keep all of them in sync manually.
PSYCHIATRIC_INTAKE_FORM = PsychiatricIntakeFormDefinition(
    title="Psychiatric Intake Form",
    description=(
        "Please answer the following questions as accurately as possible. "
        "This information helps your provider prepare for your first session."
    ),
    chief_complaint=IntakeQuestion(
        id="chief_complaint",
        label="What is the main reason you are seeking care today?",
        type=IntakeQuestionType.LONG_TEXT,
    ),
    symptom_duration=IntakeQuestion(
        id="symptom_duration",
        label="How long have you been experiencing these symptoms?",
        type=IntakeQuestionType.SINGLE_CHOICE,
        options=[duration.value for duration in SymptomDuration],
    ),
    mood_rating=IntakeQuestion(
        id="mood_rating",
        label="On a scale of 1 to 10, how would you rate your mood over the "
        "past two weeks?",
        type=IntakeQuestionType.SCALE,
        help_text="1 = very low, 10 = very good",
    ),
    symptoms=IntakeQuestion(
        id="symptoms",
        label="Which of the following have you experienced recently?",
        type=IntakeQuestionType.MULTI_CHOICE,
        required=False,
        options=[symptom.value for symptom in Symptom],
    ),
    current_medications=IntakeQuestion(
        id="current_medications",
        label="List any medications you are currently taking.",
        type=IntakeQuestionType.LONG_TEXT,
        required=False,
    ),
    past_psychiatric_history=IntakeQuestion(
        id="past_psychiatric_history",
        label="Have you previously received psychiatric treatment?",
        type=IntakeQuestionType.LONG_TEXT,
        required=False,
    ),
    family_psychiatric_history=IntakeQuestion(
        id="family_psychiatric_history",
        label="Is there any family history of mental health conditions?",
        type=IntakeQuestionType.LONG_TEXT,
        required=False,
    ),
    substance_use=IntakeQuestion(
        id="substance_use",
        label="Do you currently use alcohol, tobacco, or other substances?",
        type=IntakeQuestionType.LONG_TEXT,
        required=False,
    ),
    suicidal_ideation=IntakeQuestion(
        id="suicidal_ideation",
        label="Have you had thoughts of harming yourself recently?",
        type=IntakeQuestionType.BOOLEAN,
    ),
)
