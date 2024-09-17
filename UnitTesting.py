def testing_adjusted_probabilities():
    """Tests how the probability distribution adjusts with the 'scale' parameter from 0 to 1."""
    import numpy as np

    # Define patterns and directions as in the main function
    patterns = {
        'U-D': ['up', 'down'],
        'R-L': ['left', 'right'],
        'UL-DR': ['up-left', 'down-right'],
        'UR-DL': ['up-right', 'down-left']
    }

    directions = ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right']

    # Relative speeds
    speeds = {
        'up': 1.0,
        'down': 1.0,
        'left': 0.8,
        'right': 0.8,
        'up-left': 0.74,
        'up-right': 0.74,
        'down-left': 0.74,
        'down-right': 0.74
    }

    # Calculate default probabilities
    inverse_speeds = {d: 1.0 / speeds[d] for d in directions}
    total_inverse_speed = sum(inverse_speeds.values())
    default_probabilities = {d: inverse_speeds[d] / total_inverse_speed for d in directions}

    predominant_pattern = 'U-D'  # Change as needed
    pattern_directions = patterns[predominant_pattern]
    other_directions = [d for d in directions if d not in pattern_directions]

    # Generate scale values from 0 to 1
    scales = np.linspace(0, 1, 10)

    print(f"Testing predominant pattern '{predominant_pattern}'")
    print("Scale\tPattern Prob\tOther Prob\tIndividual Direction Probabilities")
    for scale in scales:
        # Calculate total default probabilities for pattern and others
        pattern_total_default_prob = sum(default_probabilities[d] for d in pattern_directions)
        other_total_default_prob = sum(default_probabilities[d] for d in other_directions)

        adjusted_probabilities = {}
        for d in directions:
            if scale == 0 or not pattern_directions:
                adjusted_probabilities[d] = default_probabilities[d]
            else:
                if d in pattern_directions:
                    p_d_pattern = (default_probabilities[d] / pattern_total_default_prob) * 0.8
                else:
                    p_d_pattern = (default_probabilities[d] / other_total_default_prob) * 0.2
                adjusted_probabilities[d] = (1 - scale) * default_probabilities[d] + scale * p_d_pattern

        # Sum probabilities assigned to pattern and other directions
        total_pattern_prob = sum(adjusted_probabilities[d] for d in pattern_directions)
        total_other_prob = sum(adjusted_probabilities[d] for d in other_directions)

        # Prepare probabilities for display
        direction_probs = ', '.join(f"{d}: {adjusted_probabilities[d]:.3f}" for d in directions)

        print(f"{scale:.2f}\t{total_pattern_prob:.2f}\t\t{total_other_prob:.2f}\t\t{direction_probs}")


testing_adjusted_probabilities()
