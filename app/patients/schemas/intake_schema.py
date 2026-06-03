from enum import Enum

from pydantic import BaseModel, Field

# NOTE: This intake form is intentionally NOT data-driven. Every question is
# spelled out explicitly across several layers that must be kept in sync by
# hand. Adding, removing or changing a question requires editing ALL of:
#   1. the answer enums / `IntakeAnswers` fields below,
#   2. the hardcoded `PSYCHIATRIC_INTAKE_FORM` in `constants/intake_form.py`,
#   3. the explicit columns on the `Patient` model, and
#   4. a database migration.
# There is no list/loop you can append to. This rigidity is deliberate.


class SymptomDuration(str, Enum):
    LESS_THAN_ONE_MONTH = "Less than 1 month"
    ONE_TO_SIX_MONTHS = "1 to 6 months"
    SIX_TO_TWELVE_MONTHS = "6 to 12 months"
    MORE_THAN_ONE_YEAR = "More than 1 year"


class Symptom(str, Enum):
    DEPRESSED_MOOD = "Depressed mood"
    ANXIETY = "Anxiety or excessive worry"
    SLEEP_DISTURBANCES = "Sleep disturbances"
    LOSS_OF_INTEREST = "Loss of interest or pleasure"
    DIFFICULTY_CONCENTRATING = "Difficulty concentrating"
    APPETITE_CHANGES = "Appetite changes"
    PANIC_ATTACKS = "Panic attacks"


class IntakeQuestionType(str, Enum):
    TEXT = "text"
    LONG_TEXT = "long_text"
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multi_choice"
    SCALE = "scale"
    BOOLEAN = "boolean"


class IntakeQuestion(BaseModel):
    id: str
    label: str
    type: IntakeQuestionType
    required: bool = True
    options: list[str] | None = None
    help_text: str | None = None


class PsychiatricIntakeFormDefinition(BaseModel):
    """The form description served to the patient's client for rendering.

    Each question is an explicit, individually-named field. There is no
    iterable collection of questions on purpose.
    """

    title: str
    description: str
    chief_complaint: IntakeQuestion
    symptom_duration: IntakeQuestion
    mood_rating: IntakeQuestion
    symptoms: IntakeQuestion
    current_medications: IntakeQuestion
    past_psychiatric_history: IntakeQuestion
    family_psychiatric_history: IntakeQuestion
    substance_use: IntakeQuestion
    suicidal_ideation: IntakeQuestion


class IntakeAnswers(BaseModel):
    """The answers a patient submits.

    Every answer is an explicit, strongly-typed field. Adding a question means
    adding a field here AND everywhere listed in the module docstring above.
    """

    chief_complaint: str = Field(min_length=1)
    symptom_duration: SymptomDuration
    mood_rating: int = Field(ge=1, le=10)
    symptoms: list[Symptom] = Field(default_factory=list)
    current_medications: str | None = None
    past_psychiatric_history: str | None = None
    family_psychiatric_history: str | None = None
    substance_use: str | None = None
    suicidal_ideation: bool
