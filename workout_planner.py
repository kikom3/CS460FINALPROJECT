from functools import lru_cache
from copy import deepcopy

class BaseExercise:
    # constructor
    def __init__(self, name, muscle_group, equipment_type):
        # name of exercise, muscle group it hits, and equipment type
        self.name = name
        self.muscle_group = muscle_group
        self.equipment_type = equipment_type

# used to validate waht the user says, and if it doesnt match options given, will ask to input within what is asked
def get_valid_input(questions, answer):
    
    # makes all of input lowercase so that anything inputted is lowercase and can be accepted
    lowercase_answer = [opt.lower() for opt in answer]

    # keeps going till input is validated
    while True:

        # displays prompt and takes input from user
        response = input(questions).strip().lower()

        # enter the input if it makes sense
        if response in lowercase_answer:
            return response
        
        # if not valid then ask again showing valid options
        else:
            print(f"Invalid input. Please choose from: {', '.join(answer)}")

# gets alternative exercise for the muscle groups if an exercise is taken or you just wanna change it
def get_second_best(exercises, useranswers, scoring, target_muscle, current_name):

    # contains exercises that are in the muscle group of said target muscle group
    potentialexercises = [ex for ex in exercises if ex.muscle_group == target_muscle and ex.name != current_name]

    # gets best score from the second best exercise
    best_score = float('-inf')

    # second best
    second_best = None

    # loops through every exercise that is in the same muscle group as target
    for ex in potentialexercises:

        # gets score
        score = scoring_every_exercise(ex, useranswers, scoring)

        # goes through and finds the second best score to return 
        if score > best_score:
            best_score = score
            second_best = ex
    return second_best


# scores every exercise depending on the user answers for the questions given
def scoring_every_exercise(exercise, useranswers, scoring):
    # total starts at 0 since nothing has been answered yet
    total = 0

    # goes through every question and answer the comes with said question, adding score to total to find out which exercise is best
    for question, answer in useranswers.items():
        exercise_scores = scoring.get(question,{})
        answer_scores = exercise_scores.get(answer, {})
        total += answer_scores.get(exercise.equipment_type, 0)
    return total

# gets all muscle groups from exercises
def getgroups(exercises):
    return sorted(set(ex.muscle_group for ex in exercises))

# finds the best circuit with different equipment types not just one with dp
def optimalcircuitwithdp(exercises, useranswers, scoring):

    # gets all muscle groups needed
    muscle_groups = getgroups(exercises)

    # groups muscle groups with exercises that targets them
    muscle_groups_to_exercises = {}
    for ex in exercises:
        muscle_groups_to_exercises.setdefault(ex.muscle_group, []).append(ex)
    
    # memoization
    @lru_cache(maxsize=None)

    # will return best score and best circuit based off of input
    def dp(index, used_exercises, used_equipment):

        # if all muscle groups have been used, return no score and empty circuit for now
        if index == len(muscle_groups):
            return 0, []

        # selects a muscle group
        muscle = muscle_groups[index]

        # makes a best score and best circuit for said muscle group
        bestscore = float('-inf')
        best_circuit = []

        # goes through every exercise in the muscle group your at
        for ex in muscle_groups_to_exercises[muscle]:

            # gets name of exercise and muscle group it targets, and if its already been used skip so no duplicates
            id_or_name = (ex.name, ex.muscle_group)
            if id_or_name in used_exercises:
                continue
            
            # gets score of exercise from questions asked and input given 
            score = scoring_every_exercise(ex, useranswers, scoring)

            # penalty added for more diversity in equipment type so that if one answer is heavily called on, there is at least some variety
            penalty = -(used_equipment.count(ex.equipment_type) * 2)

            # add penalty to score
            score += penalty

            # calls dp now for a new muscle group where it marks old exercises and equipment types as used
            nextscore, nextcircuit = dp(
                index + 1,
                used_exercises + (id_or_name,),
                used_equipment + (ex.equipment_type,)
            )

            
            total = score + nextscore

            # if total is better than old best score than just update best score and best circuit
            if total > bestscore:
                bestscore = total
                best_circuit = [ex] + nextcircuit

        # return the best score and best circuit
        return bestscore, best_circuit

    # return best circuit
    _, best_circuit = dp(0, (), ())
    return best_circuit


# these are some base exercises that I could think of, basically a base circuit anyone can do with the name of the exercise, the muscle group that it targets, and the type of equipment that is used
base_exercises = [
    BaseExercise("Bench Press", "chest", "barbell"),
    BaseExercise("Bicep Curl", "biceps", "dumbbell"),
    BaseExercise("Tricep Pushdowns", "triceps", "machine"),
    BaseExercise("Overhead Press", "shoulders", "dumbbell"),
    BaseExercise("Squats", "legs", "barbell"),
    BaseExercise("Deadlifts", "legs", "barbell"),
    BaseExercise("Barbell Rows", "back", "barbell"),
]

# if asked for a machine only workout, these are some exercises that I could think of that are machine only, showing name, muscle group it targets, and machine only equipment
machine_only_exercises = [
    BaseExercise("Chest Press Machine", "chest", "machine"),
    BaseExercise("Seated Bicep Curls", "biceps", "machine"),
    BaseExercise("Tricep Pushdown", "triceps", "machine"),
    BaseExercise("Seated Machine Shoulder Presses", "shoulders", "machine"),
    BaseExercise("Leg Press Machine", "legs", "machine"), 
    BaseExercise("Machine Rows", "back", "machine"), 
] 
 
 
 
 
# if asked for a dumbbel only workout, do usual, only dumbbell equipment and hits every muscle group needed (planning to try and implement more things for leg since its so much)
dumbbell_only_exercises = [ 
    BaseExercise("Dumbbell Bench Press", "chest", "dumbbell"), 
    BaseExercise("Bicep Curls", "biceps", "dumbbell"), 
    BaseExercise("Dumbbell Skull Crushers", "triceps", "dumbbell"), 
    BaseExercise("Lateral Raises", "shoulders", "dumbbell"), 
    BaseExercise("Squats", "legs", "dumbbell"), 
    BaseExercise("Deadlifts", "legs", "dumbbell"),
    BaseExercise("Bent Over Dumbbell Rows", "back", "dumbbell"),
]


# Cable only exercises, hits all muscle groups (free to change want more input)
cable_only_exercises = [
    BaseExercise("Cable Chest Press", "chest", "cable"),
    BaseExercise("Cable Bicep Curls", "biceps", "cable"),
    BaseExercise("Cable Tricep Pushdowns", "triceps", "cable"),
    BaseExercise("Cable Shoulder Press", "shoulders", "cable"),
    BaseExercise("Cable Squats", "legs", "cable"),
    BaseExercise("Cable RDL", "legs", "cable"),
    BaseExercise("Seated Cable Rows", "back", "cable"),
]



# bodyweight only, hits all parts (lowkey could not think of other exercises might edit later if given more input)
bodyweight_only_exercises = [
    BaseExercise("Pushups", "chest", "bodyweight"),
    BaseExercise("Chin ups", "biceps", "bodyweight"),
    BaseExercise("Bench Dips", "triceps", "bodyweight"),
    BaseExercise("Pike Pushups", "shoulders", "bodyweight"),
    BaseExercise("Lunges", "legs", "bodyweight"),
    BaseExercise("Pullups", "back", "bodyweight"),
]

# tallying up points for each workout type depending on the way the user answers
# FOR NOW THESE ARE MY OPINIONS CAUSE LOWKEY YOU CANNOT PROVE THIS IS BETTER THAN THAT SO I AM GOING OFF THE INFO I HAVE AND WHAT I THINK IS BEST FOR EACH CATEGORY
# 4 is best, 3 is second best, 2 is third best, 1 is DO NOT DO THIS

# dumbbells are best for building stability while getting strong cause with alot of dumbbell exercises, you need to be able to balance the weight and really be stable to efficently do them (i regret not using dumbbells as much cause now im really unstable and unbalance LMAO)
# machines are the goat for just targeting your muscles, though it really only does that
# Cable is great for consistent resistance as for all the other equipment sometimes there is a decline in resistance as your almost done with the rep or maybe the start etc. 
# thats your own weight of course it doesnt cost money LMAO
scoring_for_priority = {
    "Building Balance and Stability while Strengthening": {"dumbbell": 4, "machine": 2, "cable": 3, "bodyweight": 3},
    "Pure muscle targeting": {"machine": 4, "cable": 3, "dumbbell": 2, "bodyweight": 1},
    "Consistent Resistance": {"cable": 4, "machine": 3, "dumbbell": 2, "bodyweight": 1},
    "Most Cost Effective": {"bodyweight": 4, "dumbbell": 3, "cable": 2, "machine": 1},
}

# if your a beginner just go with machine as you can build muslce without worrying about anything else
# if your intermediate, you ahve done some lifting and most likely have a good amount of strength and balance, stick with dumbbells those are good
# if your advanced cable is great for a lot of diversity you can do alot with it 
scoring_for_experience = {
    "Beginner": {"machine": 4, "cable": 3, "dumbbell": 2, "bodyweight": 1},
    "Intermediate": {"dumbbell": 4, "cable": 3, "bodyweight": 2, "machine": 1},
    "Advanced": {"dumbbell": 3, "cable": 4, "bodyweight": 2, "machine": 1},
}

# if your injury prone do things that are safe so machine would be great as you will only really be working the muscles you want nothing else is needed most of the time
# if your not injury prone that means you can most likely use your bodyweight as a workout tool
scoring_for_injury_prone = {
    "y": {"machine": 4, "cable": 3, "dumbbell": 2, "bodyweight": 1},
    "n": {"bodyweight": 4, "dumbbell": 3, "cable": 2, "machine": 1},
}

# machine is very good for building strength
# cable imo is goated for hypertrophy
# bodyweight is the definiition of endurance
scoring_for_goal = {
    "Strength": {"machine": 4, "dumbbell": 3, "cable": 2, "bodyweight": 1},
    "Hypertrophy": {"cable": 4, "dumbbell": 3, "machine": 2, "bodyweight": 1},
    "Endurance": {"bodyweight": 4, "cable": 3, "dumbbell": 2, "machine": 1},
}

# i mean if you have no weights just use your own weight
# if you have moderate weight options, dumbbells are the cheapest of anything that is not bodyweight so most likely use that
# unlimited options means you have everything so just use machine and cable
scoring_for_limited_weight = {
    "Limited": {"bodyweight": 4, "dumbbell": 3, "cable": 2, "machine": 1},
    "Moderate": {"dumbbell": 4, "bodyweight": 3, "cable": 2, "machine": 1},
    "Unlimited": {"machine": 4, "cable": 3, "dumbbell": 2, "bodyweight": 1},
}

# if you wanna workout at home bodyweight and dumbbells are the most likely youll have
# gym use machine or cable
scoring_for_home_gym = {
    "Home": {"bodyweight": 4, "dumbbell": 3, "cable": 2, "machine": 1},
    "Gym": {"machine": 4, "cable": 3, "dumbbell": 3, "bodyweight": 1},
}

# if you wanna hit everything at once go with bodyweight and dumbbells
# if you wanna hit something new every day go with machine and cable
scoring_for_full_body_split = {
    "Full-Body": {"bodyweight": 4, "dumbbell": 3, "cable": 2, "machine": 1},
    "Split": {"dumbbell": 4, "machine": 3, "cable": 2, "bodyweight": 1},
}

# bodyweight is always great to still be athletic but not super bulky
# machine is good for strength if you do not need to be overly athletic
scoring_for_sport = {
    "y": {"bodyweight": 4, "cable": 3, "dumbbell": 3, "machine": 1},
    "n": {"machine": 4, "dumbbell": 3, "cable": 2, "bodyweight": 1},
}

# dumbbells cables and bodyweight can be used for multiple things and can change
# machine will most likely always target one muslce group, will ahve to change machines to target somethign new
scoring_for_versatile_vs_convenience = {
    "versatile": {"dumbbell": 4, "cable": 3, "bodyweight": 3, "machine": 1},
    "convenient": {"bodyweight": 4, "machine": 3, "dumbbell": 2, "cable": 1},
}


# starts off by just printing a common circuit with common exercises that i made up
print("Some common exercises for your workout circuit would be: ")
for exercise in base_exercises:
    print(f"- {exercise.name} ({exercise.muscle_group}) - Equipment: {exercise.equipment_type}")

# get input about whether or not they wanna change the original circuit given to them
userresponse = get_valid_input("Would you like to make any changes to the exercises? (y/n)", ["y", "n"])

# if they wanna change it you can either change equipment type or be asked questions to get the best workout plan you can
if userresponse == 'y':
    userresponse2 = get_valid_input("Would you want to change the equipmment type of the exercises or maybe go over some questions to get a better workout plan? (equipment/questions) ", ["equipment", "questions"])

    # change equipment
    if userresponse2 == 'equipment':
        userresponse3 = get_valid_input("What type of equipment would you like to use? (machine/dumbbell/cable/bodyweight) ", ["machine", "dumbbell", "cable", "bodyweight"])

        # change to machine workout
        if userresponse3 == 'machine':
            print("Here are the machine only exercises: ")
            for exercise in machine_only_exercises:
                print(f"- {exercise.name} ({exercise.muscle_group}) - Equipment: {exercise.equipment_type}")

        # change to dumbbells only circuit
        elif userresponse3 == 'dumbbell':
            print("Here are the dumbbell only exercises: ")
            for exercise in dumbbell_only_exercises:
                print(f"- {exercise.name} ({exercise.muscle_group}) - Equipment: {exercise.equipment_type}")

        # cable only workout
        elif userresponse3 == 'cable':
            print("Here are the cable only exercises: ")
            for exercise in cable_only_exercises:
                print(f"- {exercise.name} ({exercise.muscle_group}) - Equipment: {exercise.equipment_type}")

        # bodyweight workout
        elif userresponse3 == 'bodyweight':
            print("Here are the bodyweight only exercises: ")
            for exercise in bodyweight_only_exercises:
                print(f"- {exercise.name} ({exercise.muscle_group}) - Equipment: {exercise.equipment_type}")

    # if you pick questions, gives questions to answer to get input for best circuit
    elif userresponse2 == 'questions':

        # print questions
        print("Here are the questions: ")


        # 1st question, trying to grasp goal of working out
        userresponse4 = get_valid_input("What would you say is the most important thing about a workout for you? (Building Balance and Stability while Strengthening, Pure muscle targeting, Consistent Resistance, or Most Cost Effective) ", [
            "Building Balance and Stability while Strengthening", "Pure muscle targeting", "Consistent Resistance", "Most Cost Effective"
        ])

        
        # 2nd question, getting experience in the gym (determines what type of equipment would best suit needs)
        userresponse5 = get_valid_input("How new are you to the gym? (Beginner, Intermediate, or Advanced) ", ["Beginner", "Intermediate", "Advanced"])

        # 3rd question grasp if they have had injuries before or if they need options that lessen chance of injury
        userresponse6 = get_valid_input("Are you injury prone/Want a safe option when working out? (y/n)", ["y", "n"])

        # 4th question see what goal is can determine best equipment
        userresponse7 = get_valid_input("What is your goal? (Strength, Hypertrophy, or Endurance) ", ["Strength", "Hypertrophy", "Endurance"])

        # 5th question determines equipment options 
        userresponse8 = get_valid_input("How limited are your weight options? (Limited, Moderate, or Unlimited) ", ["Limited", "Moderate", "Unlimited"])

        # 6th question can really determine whether to go for dumbbells machine cable or bodyweight
        userresponse9 = get_valid_input("Do you want to work out at home or at the gym? (Home/Gym) ", ["Home", "Gym"])

        # 7th question difference between working out certain parts everyday or everything
        userresponse10 = get_valid_input("Do you prefer full-body or split workouts? (Full-Body/Split) ", ["Full-Body", "Split"])

        # 8th question if sports most likely dont wanna bulk too much but still be athletic
        userresponse11 = get_valid_input("Are you working out for a sport?(y/n)", ["y", "n"])

        # 9th question determines if they want equipment that can be used for multiople different things or need no setting up
        userresponse12 = get_valid_input("Do you prefer your workouts to be more convenient or more versatile? (convenient/versatile)", ["convenient", "versatile"])

        # maps answers from the user to questions
        useranswers = {
            "priority": userresponse4,
            "experience": userresponse5,
            "injury_prone": userresponse6,
            "goal": userresponse7,
            "limited_weight": userresponse8,
            "home_gym": userresponse9,
            "full_body_split": userresponse10,
            "sport": userresponse11,
            "versatile_vs_convenience": userresponse12,
        }

        # gets all exercises together
        allexercises = machine_only_exercises + dumbbell_only_exercises + cable_only_exercises + bodyweight_only_exercises

        # gives all equipment types
        typesofequipment = ['machine', 'cable', 'dumbbell', 'bodyweight']
        total_points = {equipment: 0 for equipment in typesofequipment}

        # puts scores into dictionary
        scoring = {
            "priority": scoring_for_priority,
            "experience": scoring_for_experience,
            "injury_prone": scoring_for_injury_prone,
            "goal": scoring_for_goal,
            "limited_weight": scoring_for_limited_weight,
            "home_gym": scoring_for_home_gym,
            "full_body_split": scoring_for_full_body_split,
            "sport": scoring_for_sport,
            "versatile_vs_convenience": scoring_for_versatile_vs_convenience,
        }

        # goes through answers, adding scores to total
        for question, answer in useranswers.items():

            # gets scoring
            scoring_dictionary = scoring.get(question, {})

            # gets scores for equipment types based on answer
            scores_for_answer = scoring_dictionary.get(answer, {})

            # add scores to total
            for equipment, score in scores_for_answer.items():
                total_points[equipment] += score

        # gets best equipment based on points
        best_equipment = max(total_points, key=total_points.get)

        equipment_to_exercises = {
            "machine": machine_only_exercises,
            "dumbbell": dumbbell_only_exercises,
            "cable": cable_only_exercises,
            "bodyweight": bodyweight_only_exercises,
        }

        # prints best equipment type
        print(f"\nBased on your answers, the best equipment type is: {best_equipment}\n")

        # gives exercises for each muscle group for the best equipment
        print("Here are some recommended exercises for you:")
        recommended_exercises = equipment_to_exercises.get(best_equipment, [])
        for exercise in recommended_exercises:
            print(f"- {exercise.name} ({exercise.muscle_group}) - Equipment: {exercise.equipment_type}")


        # asking for better customization
        bettercustomization = get_valid_input("Would you like to further customize your workout plan? (y/n)", ["y", "n"])

        # if they want better customization this is where you utilize the dp function to get best circuit
        if bettercustomization == 'y':
            print("Here are the exercises with mixed equipment not just the best equipment type: ")
            mixed_circuit = optimalcircuitwithdp(allexercises, useranswers, scoring)

            # prints with numbers so you can check which one you want an alternate exercise from
            for idx, exercise in enumerate(mixed_circuit):
                print(f"{idx + 1}. {exercise.name} ({exercise.muscle_group}) - Equipment: {exercise.equipment_type}")

            # asking for replacement
            wants_change = get_valid_input("Would you like to replace any of these exercises? (y/n)", ["y", "n"])

            # if they want a change, pick number of exercise you wanna change and picks second best
            if wants_change == 'y':

                # loop until no replacement wanted
                while True:
                    try:
                        # ask which you wanna replace with number
                        choice = int(input("Enter the number of the exercise you want to replace (1-{}), or 0 to stop: ".format(len(mixed_circuit))))
                        # if 0 stop
                        if choice == 0:
                            break
                        # if number than replace with second best
                        if 1 <= choice <= len(mixed_circuit):
                            original = mixed_circuit[choice - 1]
                            second_best = get_second_best(allexercises, useranswers, scoring, original.muscle_group, original.name)
                            if second_best:
                                mixed_circuit[choice - 1] = second_best
                                print(f"Replaced with: {second_best.name} ({second_best.muscle_group}) - Equipment: {second_best.equipment_type}")

                            # no replacement found
                            else:
                                print("No alternative found for that muscle group.")
                        
                        # not in range
                        else:
                            print("Invalid choice.")
                    # ask again if not in range or not number
                    except ValueError:
                        print("Please enter a number.")

            print("\nFinal customized circuit:")
            for ex in mixed_circuit:
                print(f"- {ex.name} ({ex.muscle_group}) - Equipment: {ex.equipment_type}")

        else:
            print("Great! Remember, strict form only!")

else:
    print("Great! Remember, strict form only!")
