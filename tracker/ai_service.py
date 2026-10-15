from google import genai

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("api_key")

client = genai.Client(api_key=api_key)


def get_dietplan(response_data):

    monthly_total_calorie = response_data.get("monthly_total_calorie")

    monthly_category_summary = response_data.get("monthly_category_summary")

    monthly_category_summary_text = ""

    for d in monthly_category_summary:
        monthly_category_summary_text += (
            f". {d.get('meal_type')}: {d.get('total')} calories\n"
        )

    prompt = f"""
    Act as an expert nutrition advisor specializing in practical,
    healthy eating habits and Kerala cuisine.

    Here is my food consumption summary for the past month:

    - Total Monthly Calories Consumed: {monthly_total_calorie}
    - Meal-wise Calorie Breakdown:{monthly_category_summary_text}

    Based on this data, provide a practical diet improvement plan
    suitable for someone living in Kerala, India.

    1. Food Intake Analysis:
       Analyze my total monthly calorie intake and meal-wise calorie
       distribution. Identify potential areas for improvement.

    2. Daily Eating Plan:
       Suggest a balanced daily meal plan with breakfast, lunch,
       evening snacks, and dinner using affordable Kerala foods.
       Include approximate portion sizes and estimated calories.

    3. Meal Distribution:
       Recommend a practical distribution of daily calories across
       meals, explaining how it could help maintain balanced eating habits.

    4. Kerala-Specific Recommendations:
       Suggest 3-4 practical healthy eating tips using locally available
       foods such as rice, puttu, idli, dosa, eggs, fish, pulses,
       vegetables, and seasonal fruits.

    5. Improvement Suggestions:
       Provide realistic recommendations to improve food variety,
       protein intake, fiber intake, and overall dietary balance.

    Important Guidelines:
    - Do not assume that my goal is weight loss or weight gain.
    - Do not assume my age, gender, height, weight, or activity level.
    - Monthly calorie totals alone cannot establish my daily calorie needs.
    - If the number of days covered by the food log is unknown,
      do not assume it represents a complete month of eating.
    - Clearly explain that recommendations are general because
      personal health and body measurements are unavailable.
    - Treat calorie estimates as approximate.
    - Avoid extreme diets and unnecessary calorie restrictions.
    - Format the response with clear headings and practical suggestions.
    """

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )

    return response.text
