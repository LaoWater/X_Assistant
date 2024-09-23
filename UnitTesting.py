def predominant_pattern_and_distribution(predominant_pattern, scale, patterns, directions, default_probabilities):
    if predominant_pattern in patterns:
        predominant_pattern_directions = patterns[predominant_pattern]
        other_directions = [d for d in directions if d not in predominant_pattern_directions]
    else:
        predominant_pattern_directions = []
        other_directions = directions.copy()

    # Validate & Normalize scale
    normalized_scale = float(scale / 100)
    # scale = max(0, min(normalized_scale, 1))

    # Calculate pattern total default probabilities
    predominant_pattern_total_default_prob = sum(default_probabilities[d] for d in predominant_pattern_directions)
    other_total_default_prob = sum(default_probabilities[d] for d in other_directions)

    # Step 1: Calculate total increase for predominant pattern directions
    predominant_increase = 0  # Store the total increase for predominant pattern directions
    adjusted_probabilities = {}

    print(f"\nStep 1: Adjusting probabilities for predominant pattern {predominant_pattern} "
          f"directions with scale {normalized_scale}")
    for d in directions:
        if d in predominant_pattern_directions:
            p_d_pattern = default_probabilities[d] / predominant_pattern_total_default_prob
            # Calculate the adjusted probability (limit the increase to a reasonable amount based on scale)
            adjusted_probabilities[d] = ((1 - normalized_scale) * default_probabilities[d]
                                         + normalized_scale * p_d_pattern)
            predominant_increase += (adjusted_probabilities[d] - default_probabilities[d])  # Track increase
        else:
            adjusted_probabilities[d] = default_probabilities[d]  # Initialize with default

    print(f"Adjusted probabilities: {adjusted_probabilities}")
    print(f"Total Increase for Predominant Directions: {predominant_increase}")

    # Step 2: Redistribute the increase across non-predominant directions
    if predominant_increase > 0:
        total_non_pattern_prob = sum(default_probabilities[d] for d in other_directions)
        print(f"Step 2: Redistributing the increase ({predominant_increase}) among non-predominant directions...")
        print(f"Total Probability for Non-Predominant Directions: {total_non_pattern_prob}")

        for d in other_directions:
            # Calculate the proportion of the non-predominant pattern this direction occupies
            redistribution_factor = default_probabilities[d] / total_non_pattern_prob
            redistribution_amount = min(predominant_increase, default_probabilities[d] * 0.5)  # Limit reduction
            # Subtract the redistribution amount proportionally
            adjusted_probabilities[d] -= redistribution_amount

    print(f"Step 2 Completed: Adjusted probabilities redistributed: {adjusted_probabilities}")

    # Step 3: Ensure total probability sums to 1 by adjusting any residuals
    total_adjusted_prob = sum(adjusted_probabilities.values())
    residual = 1 - total_adjusted_prob

    print(f"Step 3: Ensuring total probability sums to 1...")
    print(f"Total Adjusted Probability before residual adjustment: {total_adjusted_prob}, Residual: {residual}")

    # Distribute the residual back proportionally across all directions to make the sum exactly 1
    for d in adjusted_probabilities:
        adjusted_probabilities[d] += residual * (adjusted_probabilities[d] / total_adjusted_prob)

    print("Final Adjusted Probabilities:", adjusted_probabilities)

    return adjusted_probabilities


#################
## Main Starts ##
#################

coords = {
    'left': (911, 551),
    'up_left': (911, 519),
    'up_right': (1005, 513),
    'right': (1013, 551),
    'up': (960, 528),
    'down': (960, 576),
    'down_left': (916, 559),
    'down_right': (990, 573)
}

patterns = {
    'U-D': ['up', 'down'],
    'R-L': ['left', 'right'],
    'UL-DR': ['up-left', 'down-right'],
    'UR-DL': ['up-right', 'down-left']
}

# All possible directions
directions = list(coords.keys())

# Relative speeds (higher means faster) due to Game mechanics (Character and Maps knowledge base)
# Higher-Speed = character will finish a full map run on target direction faster
# Therefore, the probability distribution for balanced movement must be inversed to Speed
speeds = {
    'up': 1.0,  # Fastest
    'down': 1.0,  # Fastest
    'left': 0.8,
    'right': 0.8,
    'up_left': 0.74,
    'up_right': 0.74,
    'down_left': 0.74,
    'down_right': 0.74
}

# Calculate default probabilities inversely proportional to speeds
inverse_speeds = {d: 1.0 / speeds[d] for d in directions}
total_inverse_speed = sum(inverse_speeds.values())
default_probabilities = {d: inverse_speeds[d] / total_inverse_speed for d in directions}

results = []

for scale in range(0, 102, 2):  # Loop over scales from 0 to 100 with a step of 2

    # Call the function with the scale and a given pattern (for example, 'R-L')
    adjusted_probabilities = predominant_pattern_and_distribution('R-L', scale, patterns, directions,
                                                                  default_probabilities)

    # Format the adjusted probabilities for output
    formatted_probabilities = ', '.join(
        [f"'{d}' = {adjusted_probabilities[d] * 100:.1f}%" for d in adjusted_probabilities])

    # Append the result to the results list
    results.append(f"Scale: {scale}, Probability Distribution: {formatted_probabilities}")

# Print the results list to view all the final results
for result in results:
    print(result)

