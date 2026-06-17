# ============================================
# WORKOUT APP CONFIGURATION
# ============================================
# This file stores workout task definitions and
# all user-facing text used by the app.

DEFAULT_REST = 5  # default rest time between exercises in seconds
MIN_REST = 5  # minimum allowed rest time in seconds
DEFAULT_EXERCISE_COUNT = 8  # number of exercises to randomly select from the pool

WORKOUT_TASKS = [
    {"name": "Burpees", "duration": 45, "encouragement": "Push through, keep your form strong!"},
    {"name": "Running on the Spot", "duration": 45, "encouragement": "Drive those knees, stay light on your feet!"},
    {"name": "Jumping Jacks", "duration": 45, "encouragement": "Stay bouncing, open those arms wide!"},
    {"name": "Mountain Climbers", "duration": 45, "encouragement": "Keep the pace, feel that core burn!"},
    {"name": "High Knees", "duration": 45, "encouragement": "Lift those knees, keep the energy high!"},
    {"name": "Plank Jacks", "duration": 45, "encouragement": "Hold strong, keep your core tight!"},
    {"name": "Squat Jumps", "duration": 45, "encouragement": "Explode up and land softly!"},
    {"name": "Push-up Plank Taps", "duration": 45, "encouragement": "Keep the hips steady and keep moving!"},
    {"name": "Skater Hops", "duration": 45, "encouragement": "Stay light and powerful with each hop!"},
    {"name": "Bicycle Crunches", "duration": 45, "encouragement": "Twist through the core with control!"},
    {"name": "Lunge Jumps", "duration": 45, "encouragement": "Stay low, then launch into each jump!"},
    {"name": "Side Plank Dips", "duration": 45, "encouragement": "Hold the line and feel the burn on the side!"},
    {"name": "Butt Kicks", "duration": 45, "encouragement": "Pull those heels up and keep the tempo up!"},
    {"name": "Triceps Dips", "duration": 45, "encouragement": "Control the motion and feel the back of the arm!"},
    {"name": "Flutter Kicks", "duration": 45, "encouragement": "Keep the core engaged and legs moving!"},
    {"name": "Arm Circles", "duration": 45, "encouragement": "Warm up those shoulders with big, strong circles!"},
    {"name": "Standing Ab Twists", "duration": 45, "encouragement": "Rotate with control and stay tall!"},
    {"name": "Wall Sit", "duration": 45, "encouragement": "Press into the wall and own that burn!"},
    {"name": "Toe Touches", "duration": 45, "encouragement": "Reach high and feel the stretch!"},
    {"name": "Inchworm Walkouts", "duration": 45, "encouragement": "Move with a strong core and steady pace!"},
]

MESSAGES = {
    "welcome_title": "=== Welcome to the Workout Timer App ===",
    "welcome_text": "Today you will move through a few heart-pumping exercises.",
    "voice_enabled": "Voice coaching is enabled.",
    "voice_disabled": "Voice coaching is not available; text prompts will be shown.",
    "session_prompt": "Relax! Your workout will be randomly selected from 20 exercises.",
    "use_all_option": "",
    "rest_prompt": "Enter rest time between exercises in seconds (default {default_rest}): ",
    "too_short_rest": "Rest time too short, using default {default_rest} seconds.",
    "invalid_rest": "Invalid number entered. Using default {default_rest} seconds.",
    "random_selection": "Randomly choosing {count} exercises from the full workout pool.",
    "session_summary": "Great! You'll complete {count} exercise(s) with {rest}s rest between each.",
    "out_of_range": "Skipping out-of-range selection: {selection}",
    "invalid_selection": "Skipping invalid selection: {selection}",
    "no_valid_selection": "No valid selection found. Using all exercises.",
    "workout_complete": "Workout complete! You crushed it today.",
}
