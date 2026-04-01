from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Any, Optional

class PredictionFeatures(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='forbid')

    age_of_the_girl: float = Field(default=0.0, alias="Age of the girl")
    is_there_a_family_history_of_autism_or_related_neurodevelopmental_conditions: float = Field(default=0.0, alias="Is there a family history of autism or related neurodevelopmental conditions?")
    did_you_experience_any_complications_during_pregnancy_or_childbirth: float = Field(default=0.0, alias="Did you experience any complications during pregnancy or childbirth?")
    at_what_age_did_your_child_first_start_to_walk: float = Field(default=0.0, alias="At what age did your child first start to walk?")
    at_what_age_did_your_child_first_start_to_speak_in_full_words_or_phrases: float = Field(default=0.0, alias="At what age did your child first start to speak in full words or phrases?")
    are_there_any_known_medical_neurological_or_psychological_conditions_your_child_is_currently_experiencing: float = Field(default=0.0, alias="Are there any known medical, neurological, or psychological conditions your child is currently experiencing?")
    appears_comfortable_in_social_settings_e_g_classrooms_birthday_parties: float = Field(default=0.0, alias="Appears comfortable in social settings (e.g., classrooms, birthday parties)")
    prefers_spending_time_with_close_friend_s_over_group_of_people_with_group_activities: float = Field(default=0.0, alias="Prefers spending time with close friend(s) over group of people with group activities")
    seems_emotionally_or_physically_exhausted_after_socializing: float = Field(default=0.0, alias="Seems emotionally or physically exhausted after socializing")
    confidently_initiates_conversations: float = Field(default=0.0, alias="Confidently initiates conversations")
    struggles_to_read_facial_expressions_tone_or_body_language: float = Field(default=0.0, alias="Struggles to read facial expressions, tone, or body language")
    recognizes_familiar_people_when_seeing_them_unexpectedly: float = Field(default=0.0, alias="Recognizes familiar people when seeing them unexpectedly")
    is_able_to_put_up_with_go_along_with_inaccuracies_guestimations_approximation: float = Field(default=0.0, alias="Is able to put up with / go along with inaccuracies / guestimations / approximation?")
    frequently_feels_misunderstood_during_conversations: float = Field(default=0.0, alias="Frequently feels misunderstood during conversations")
    becomes_upset_or_frustrated_when_misunderstood: float = Field(default=0.0, alias="Becomes upset or frustrated when misunderstood")
    struggles_to_express_emotions_with_words: float = Field(default=0.0, alias="Struggles to express emotions with words")
    finds_it_difficult_to_calm_down_after_becoming_upset_or_stressed: float = Field(default=0.0, alias="Finds it difficult to calm down after becoming upset or stressed")
    demonstrates_ritualized_patterns_of_verbal_or_nonverbal_behavior_with_extreme_distress_at_small_changes_prefers_routines_in_daily_life: float = Field(default=0.0, alias="Demonstrates ritualized patterns of verbal or nonverbal behavior with extreme distress at small changes (Prefers routines in daily life)")
    rehearses_or_plans_their_conversations_phrases_always_greet_good_morning_evening_etc_in_advance: float = Field(default=0.0, alias="Rehearses or plans their conversations (phrases, always greet Good Morning/Evening, etc.) in advance")
    monitors_others_reactions_to_her_actions_to_get_a_validation_that_she_is_acting_appropriately: float = Field(default=0.0, alias="Monitors others’ reactions to her actions to get a validation that she is acting appropriately")
    engages_in_stimming_i_e_certain_repetitive_movements_or_actions_twirling_rocking_waving_hands_wiggling_legs_humming_etc: float = Field(default=0.0, alias="Engages in “stimming” i.e. certain repetitive movements or actions: Twirling, rocking, waving hands, wiggling legs, humming, etc.")
    appears_confused_by_social_expectations_or_unwritten_rules: float = Field(default=0.0, alias="Appears confused by social expectations or 'unwritten rules'")
    mimics_others_behavior_to_fit_in: float = Field(default=0.0, alias="Mimics others’ behavior to fit in")
    avoids_or_struggles_to_maintain_eye_contact: float = Field(default=0.0, alias="Avoids or struggles to maintain eye contact")
    fnds_it_difficult_to_follow_multiple_conversations_happening_at_once_e_g_in_a_group_setting: float = Field(default=0.0, alias="Fnds it difficult to follow multiple conversations happening at once (e.g., in a group setting)?")
    feels_overwhelmed_by_the_need_to_communicate_in_social_situations: float = Field(default=0.0, alias="Feels overwhelmed by the need to communicate in social situations?")
    feels_overwhelmed_stressed_when_something_changes_on_them_at_the_last_minute_or_gets_upset_when_others_do_not_follow_through_on_plans_promises_made: float = Field(default=0.0, alias="Feels overwhelmed / stressed when something changes on them at the last minute or gets upset when others do not follow through on plans/promises made")
    appears_anxious_or_withdrawn_in_unfamiliar_social_settings: float = Field(default=0.0, alias="Appears anxious or withdrawn in unfamiliar social settings")
    finds_it_difficult_to_manage_emotions_during_stressful_interactions: float = Field(default=0.0, alias="Finds it difficult to manage emotions during stressful interactions")
    internalizes_anxiety_or_stress_without_showing_it: float = Field(default=0.0, alias="Internalizes anxiety or stress without showing it")
    sensitive_to_loud_noises_and_or_bright_lights_or_visual_clutter: float = Field(default=0.0, alias="Sensitive to loud noises and/or bright lights or visual clutter")
    avoids_certain_fabrics_or_textures_due_to_discomfort: float = Field(default=0.0, alias="Avoids certain fabrics or textures due to discomfort")
    affected_by_strong_smells_that_others_seem_to_tolerate: float = Field(default=0.0, alias="Affected by strong smells that others seem to tolerate")
    appears_overwhelmed_in_crowded_or_noisy_environments: float = Field(default=0.0, alias="Appears overwhelmed in crowded or noisy environments")
    uses_the_same_phrases_or_greetings_in_different_situations: float = Field(default=0.0, alias="Uses the same phrases or greetings in different situations")
    demonstrates_strong_emotional_reactions_in_intense_situations_e_g_anger_crying_withdrawal: float = Field(default=0.0, alias="Demonstrates strong emotional reactions in intense situations (e.g., anger, crying, withdrawal)")

class PredictionRequest(BaseModel):
    features: PredictionFeatures

class PredictionResponse(BaseModel):
    prediction: int
    Recommendation: str
    model_used: str
    probability: Dict[str, float]
