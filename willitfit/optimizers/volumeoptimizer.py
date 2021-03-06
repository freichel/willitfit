"""
Receives list of package dimensions, weights and counts
Receives available volume
Optimizes stacking of packages in available volume
Returns 3D numeric representation of occupied space as well as article coordinates

RELEVANT CALLABLE FUNCTION:
generate_optimizer(
    article_list (list of IKEA articles),
    volume_space (available space as numpy array),
    generator_sorters (pre-defined sorters),
    generator_random_lists (how many random lists on top of sorted ones to try and optimize),
    optimizer_max_attempts (number of times optimizer will try to fill space using different approaches)
    )
"""

from willitfit.params import (
    ERRORS_OPTIMIZER,
    GEN_SORTERS,
    OPT_MAX_ATTEMPTS,
    RANDOM_LIST_COUNT,
    VOL_INTERIOR,
    VOL_UNAVAILABLE,
    VOL_BORDER,
    VOL_EMPTY,
    INSUFFICIENT_SPACE,
    INSUFFICIENT_DIMENSION,
    OPT_INSUFFICIENT_SPACE,
    OPT_UNSUCCESSFUL,
    BIAS_STACKS,
)
import numpy as np
from scipy.ndimage.measurements import label
from scipy.special import factorial as fctrl
import multiprocessing
import time

"""
General functions
"""


def binarize_space(volume_space):
    """
    Sets empty space to 1 and rest to 0.
    Needed to be able to identify clusters.
    """
    return np.isin(volume_space, VOL_EMPTY).astype(int)


"""
Volume fit functions
"""


def calculate_package_volume(package):
    """
    Returns volume in cm cubed for package
    """
    return np.prod(package)


def find_total_package_volume(article_list):
    """
    Establishes total volume of packages in list in cm cubed.
    Loops through each article in article_list, and each package in article.
    Multiplies length, height and width (elements 1-3).
    Sums up individual products and returns them as int
    """
    return sum(
        [
            calculate_package_volume(package[1:4]) * article[1]
            for article in article_list
            for package in article[2]
        ]
    )


def find_available_space(volume_space):
    """
    Returns total available volume in cm cubed by subtracting non-zero values from total array size
    """
    return volume_space.size - np.count_nonzero(
        binarize_space(volume_space - VOL_UNAVAILABLE)
    )


def is_space_sufficient(article_list, volume_space):
    """
    Returns True if package volume is smaller than or equal to available volume
    """
    return find_total_package_volume(article_list) <= find_available_space(volume_space)


"""
Dimension fit functions
"""


def find_longest_package_dimension(article_list):
    """
    Finds single longest dimension in cm among all packages.
    """
    return max(
        [max(package[1:4]) for article in article_list for package in article[2]]
    )


def find_longest_space_dimension(volume_space):
    """
    Determines the longest continuous stretch of empty space in all three dimensions.
    """
    # Linear structures in all three axes
    structure_y = [
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ]
    structure_x = np.rot90(structure_y, axes=(1, 2))
    structure_z = np.rot90(structure_y, axes=(0, 1))
    structures = [structure_x, structure_y, structure_z]

    # Run along each dimension
    results = []
    for structure in structures:
        # Binarize the space, then label along given dimension
        dim_result = label(input=binarize_space(volume_space), structure=structure)[0]
        # Turn into a 1-dimensional array
        dim_result = np.reshape(dim_result, dim_result.size)
        # Remove zeros
        dim_result = np.delete(dim_result, np.where(dim_result == 0))
        # Find most frequent occurrence
        most_freq = np.bincount(dim_result).argmax()
        # Return number of occurrences, which is equal to dimension in cm
        results.append(np.count_nonzero(dim_result == most_freq))
    # Return largest value from the three dimensions
    return max(results)


def is_longest_dimension_sufficient(article_list, volume_space):
    """
    Returns True if longest package dimension is smaller than or equal to longest space dimension
    """
    return find_longest_package_dimension(article_list) <= find_longest_space_dimension(
        volume_space
    )


"""
Penalizer/scorer functions
"""


def find_empty_space(volume_space):
    """
    Identifies contiguous pockets of empty space.
    Returns number of empty spaces, their total volume and the volume of the largest empty space.
    """
    # Set up structure - this treats as one contiguous space when...
    # ...there are diagonal gaps as it might make the stack unstable
    structure = np.ones((3, 3, 3), dtype=int)
    # Binarize the space, then label pockets
    dim_result = label(input=binarize_space(volume_space), structure=structure)[0]
    # How many empty spaces are there?
    number_spaces = np.max(dim_result)
    # What's the total volume of empty space?
    empty_volume = np.count_nonzero(dim_result)
    # What's the volume of the largest empty space?
    largest_volume = np.count_nonzero(dim_result == number_spaces)
    return number_spaces, empty_volume, largest_volume


def find_open_surfaces(volume_space):
    """
    Identifies and sums all surface areas.
    A surface area is defined as the 1 cm squared edge between something (unavailable space or a package) and empty space.
    Returns an integer.
    """
    # This is what we're searching for
    EDGE_STRUCTURE = np.array([1, 0])
    # Initialize counter
    surfaces = 0

    # Find matches for both the edge structure and its opposite in each dimension
    surfaces += len(
        np.where(
            (binarize_space(volume_space)[:, :, :-1] == EDGE_STRUCTURE[0])
            & (binarize_space(volume_space)[:, :, 1:] == EDGE_STRUCTURE[1])
        )[0]
    )
    surfaces += len(
        np.where(
            (binarize_space(volume_space)[:, :, :-1] == EDGE_STRUCTURE[1])
            & (binarize_space(volume_space)[:, :, 1:] == EDGE_STRUCTURE[0])
        )[0]
    )
    surfaces += len(
        np.where(
            (binarize_space(volume_space)[:, :-1 ,:] == EDGE_STRUCTURE[0])
            & (binarize_space(volume_space)[:, 1:, :] == EDGE_STRUCTURE[1])
        )[0]
    )
    surfaces += len(
        np.where(
            (binarize_space(volume_space)[:, :-1, :] == EDGE_STRUCTURE[1])
            & (binarize_space(volume_space)[:, 1:, :] == EDGE_STRUCTURE[0])
        )[0]
    )
    surfaces += len(
        np.where(
            (binarize_space(volume_space)[:-1, :, :] == EDGE_STRUCTURE[0])
            & (binarize_space(volume_space)[1:, :, :] == EDGE_STRUCTURE[1])
        )[0]
    )
    surfaces += len(
        np.where(
            (binarize_space(volume_space)[:-1, :, :] == EDGE_STRUCTURE[1])
            & (binarize_space(volume_space)[1:, :, :] == EDGE_STRUCTURE[0])
        )[0]
    )

    return surfaces


def score_space(volume_space, article_list):
    """
    This function assigns a score to the empty space left by the optimization algorithm.
    There is a penalty for having more empty spaces as well as a relatively smaller largest empty space, and too many surfaces.
    """
    # Get number of empty spaces, their total volume and the volume of the largest empty space
    number_spaces, empty_volume, largest_volume = find_empty_space(volume_space)
    # Get maximum possible empty space (assumes everything can be stacked perfectly)
    max_largest_volume = find_available_space(volume_space) - find_total_package_volume(
        article_list
    )
    """INITIAL IDEA:
    - Linear penalty for each empty space
    - Log penalty for how much largest empty space is smaller than maximum possible
    - Log penalty for open surfaces
    """
    score = (
        number_spaces
        + np.log(max(max_largest_volume - largest_volume, 0.001))
        + np.log(find_open_surfaces(volume_space))
    )
    return score


"""
Optimizer functions
"""


def sort_packages(article_list, sort_by="volume", direction="descending"):
    """
    Returns 2-dimensional list of packages sorted by sort_by in the shape of
    [(article_code, article_id, package_id)]
    """
    # Initialize list
    return_list = []
    # Loop through articles
    for article in article_list:
        # If articles exist more than once, loop here too
        for article_id in range(article[1]):
            # Loop through packages
            for package in article[2]:
                # So far only sorting by volume has been implemented.
                if sort_by == "volume":
                    return_list.append(
                        [
                            article[0],
                            article_id + 1,
                            package[0],
                            calculate_package_volume(package),
                        ]
                    )
    # Turn into a numpy array for easier sorting
    return_list = np.array(return_list, dtype="str")
    # Sort by volume (4th column)
    return_list = return_list[return_list[:, 3].astype(float).astype(int).argsort()]
    # This gives an ascending order. Reverse if needed
    if direction == "descending":
        return_list = np.flip(return_list, axis=0)
    # Remove volume column
    return return_list[:, :3]


def hash_list(article_list):
    """
    Creates an element-wise list of hashes
    """
    return [hash(article.tobytes()) for article in article_list]


def generate_package_lists(article_list, sorters=GEN_SORTERS, random_lists=RANDOM_LIST_COUNT):
    """
    Returns list of package lists for the optimizer.
    Lists can be pre-defined or randomized.
    """

    package_lists = []
    # First generate pre-defined lists
    sorters = set(sorters)
    for sorter in sorters:
        # Split by delimiter
        sort_by, direction = sorter.split("|")
        package_lists.append(
            sort_packages(article_list, sort_by=sort_by, direction=direction)
        )
    # Add random lists
    # But first check if any are needed
    if random_lists == 0:
        return package_lists
    # Create starting point if there is none, i.e. no pre-defined lists
    if len(package_lists) == 0:
        starter_list = sort_packages(article_list)
    else:
        starter_list = np.copy(package_lists[0])

    # What is the actual maximum number of unique lists?
    # It's the factorial of the number of packages divided by the product of the factorials for each package's count
    # Hoorray for high school mathematics
    max_permut = int(np.round(fctrl(len(starter_list))/np.prod(fctrl(np.unique(np.array(starter_list)[:,0], return_counts=True)[1])),0))
    
    # Now add as many random lists as needed
    while True:
        # Shuffle starter list and copy data
        np.random.shuffle(starter_list)
        new_list = np.copy(starter_list)
        # Check if this particular permutation exists already by looking at hashes
        if hash_list([new_list])[0] not in hash_list(package_lists):
            package_lists.append(new_list)
        # Check if length requirement (smaller of pre-defined lists + random_lists and max_permut) is fulfilled
        if len(package_lists) >= min(len(sorters) + random_lists, max_permut - 2):
            break

    return package_lists


def choose_orientation(package_length, package_width, package_height, biased=False, bias_tendency=0.8):
    """
    A 3-dimensional object (with exceptions like cubes) that needs to align...
    ...with the grid can have six degrees of freedom.
    Returns one random orientation for a given package.
    Can also be biased, where package will most likely be placed as flat as possible (two largest dimensions first)
    """
    # Get dimensions
    dimensions = [package_length, package_width, package_height]

    # If there is a bias to the orientation
    if biased == True:
        # Check if the threshold for using the biased orientation has been reached
        if np.random.uniform(0, 1) <= bias_tendency:
            # Flat stacking
            return sorted(dimensions, reverse=True)
    # Otherwise, choose a truly random orientation
    np.random.shuffle(dimensions)
    return (dimensions[0], dimensions[1], dimensions[2])


def find_first_space(package_x, package_y, package_z, volume_space):
    """
    Finds first suitable space for package dimensions.
    Returns x,y,z starting coordinates.
    """
    # Binarize volume space - empty areas shown as ones
    bin_space = binarize_space(volume_space)

    start_time = time.time()
    # Original shape
    orig_x, orig_y, orig_z = bin_space.shape
    # Find all occurrences in all three dimensions where package COULD fit.
    # That is, where the first and nth (as defined by the package_ dimensions) element are ones, i.e. empty.
    # It's not ideal but a good enough approximation.
    # The slicing at the end makes sure the arrays have the same dimensions, which is important for the following np.where step.
    potential_x = ((bin_space[int(np.floor(package_x/2)):-int(np.ceil(package_x/2)),:,:] == 1) & (bin_space[:-package_x,:,:] == 1) & (bin_space[package_x:,:,:] == 1))[:orig_x-package_x,:orig_y-package_y,:orig_z-package_z]
    potential_y = ((bin_space[:,int(np.floor(package_y/2)):-int(np.ceil(package_y/2)),:] == 1) & (bin_space[:,:-package_y,:] == 1) & (bin_space[:,package_y:,:] == 1))[:orig_x-package_x,:orig_y-package_y,:orig_z-package_z]
    potential_z = ((bin_space[:,:,int(np.floor(package_z/2)):-int(np.ceil(package_z/2))] == 1) & (bin_space[:,:,:-package_z] == 1) & (bin_space[:,:,package_z:] == 1))[:orig_x-package_x,:orig_y-package_y,:orig_z-package_z]
    #print(f"Occurrence search {time.time()-start_time}")
    # Find all matches between the three dimensions searched in.
    potentials = np.transpose(np.nonzero((potential_x == potential_y) & (potential_x == potential_z) & potential_x))
    # Now sort along the three dimensions/axes to ensure we stack from the correct corner of the trunk.
    potentials = potentials[np.lexsort((potentials[:,1], potentials[:,0], potentials[:,2])), :]
    #print(f"Identify potentials {time.time()-start_time}")
    # Loop through one by one until we find an appropriate solution
    i = 0
    for potential in potentials:
        x,y,z = potential
        i += 1
        # Verify if entire space is empty
        test_section = bin_space[x:x+package_x, y:y+package_y, z:z+package_z]
        if np.all(test_section == 1) and (test_section.shape == (package_x, package_y, package_z)):
            #print(f"Done. This took {time.time()-start_time}. (Attempt {i})")
            return x,y,z
    return OPT_INSUFFICIENT_SPACE


def place_package(package_dimensions, volume_space):
    """
    Attempt to place next package.
    If successful, return filled volume_space and start/end coordinates,
    if not, return error code.
    """
    # Unpack package dimensions
    package_x, package_y, package_z = package_dimensions
    package_volume = calculate_package_volume(package_dimensions)
    # Find space for package
    return_value = find_first_space(package_x, package_y, package_z, volume_space)
    # Check for error codes
    if return_value == OPT_INSUFFICIENT_SPACE:
        return OPT_INSUFFICIENT_SPACE
    x, y, z = return_value
    # Check available space - there need to be as many zeros as the package_volume for it to fit
    available_space = volume_space[
        x : x + package_x, y : y + package_y, z : z + package_z
    ]
    # If the package cannot be placed, return
    if package_volume != available_space.size - np.count_nonzero(
        binarize_space(binarize_space(available_space))
    ):
        return OPT_INSUFFICIENT_SPACE
    # Otherwise populate the array
    # Surfaces first
    # z-plane
    volume_space[x : x + package_x, y : y + package_y, z] = VOL_BORDER
    volume_space[x : x + package_x, y : y + package_y, z + package_z - 1] = VOL_BORDER
    # y-plane
    volume_space[x : x + package_x, y, z : z + package_z] = VOL_BORDER
    volume_space[x : x + package_x, y + package_y - 1, z : z + package_z] = VOL_BORDER
    # x-plane
    volume_space[x, y : y + package_y, z : z + package_z] = VOL_BORDER
    volume_space[x + package_x - 1, y : y + package_y, z : z + package_z] = VOL_BORDER
    # Fill interior area
    volume_space[
        x + 1 : x + package_x - 1, y + 1 : y + package_y - 1, z + 1 : z + package_z - 1
    ] = VOL_INTERIOR

    return (
        volume_space,
        x,
        y,
        z,
        x + package_x - 1,
        y + package_y - 1,
        z + package_z - 1,
    )


def optimizer(
    package_list,
    article_list,
    volume_space,
    empty_space,
    queue=None,
    max_attempts=OPT_MAX_ATTEMPTS,
    biased=True,
    bias_tendency=0.8,
):
    """
    Places packages sequentially into available space.
    If at any point a package can no longer be placed, try again up to max_attempts times.
    Returns score, attempts taken, filled volume_space and package coordinates.
    """
    # Attempts taken
    attempts_counter = 1
    # Package counter variable
    package_counter = 0
    # Package coordinates
    package_coordinates = []
    # Loop while there are still packages to place
    while True:
        #print(f"attempts_counter {attempts_counter}")
        # Pick up first package
        package = package_list[package_counter]
        # Find article index
        idx = sum(
            [i for i, article in enumerate(article_list) if article[0] == package[0]]
        )
        # Get package dimensions: Looks up article by its index (idx),
        # package definitions are the 3rd element (2),
        # packages are listed, so it's the n-1th element.
        pkg = article_list[idx][2][int(package[2]) - 1]
        package_length, package_width, package_height = pkg[1], pkg[2], pkg[3]
        # Obtain package orientation (random)
        package_dimensions = choose_orientation(
            package_length,
            package_width,
            package_height,
            biased=biased,
            bias_tendency=bias_tendency,
        )
        # Attempt to place package in space
        placement_result = place_package(package_dimensions, volume_space)
        # Check if placement was successful
        if placement_result != OPT_INSUFFICIENT_SPACE:
            # Extract return variables and append to package_coordinates
            (
                volume_space,
                x_start,
                y_start,
                z_start,
                x_end,
                y_end,
                z_end,
            ) = placement_result
            return_list = [
                package[0],
                package[1],
                package[2],
                x_start,
                y_start,
                z_start,
                x_end,
                y_end,
                z_end,
            ]
            package_coordinates.append(return_list)
        else:
            # If unsuccessful, increase counter of attempts taken
            attempts_counter += 1
            # See if this is too many attempts already
            if attempts_counter > max_attempts:
                # print("max attempts reached")
                # Return error code
                if queue is not None:
                    queue.put(OPT_UNSUCCESSFUL)
                return OPT_UNSUCCESSFUL
            else:
                # Try again
                package_counter = 0
                package_coordinates = []
                volume_space = np.copy(empty_space)
                continue
        #print(f"package_counter {package_counter}")
        # Increase counter to move to next package
        package_counter += 1
        # Once all packages have been placed
        if package_counter == len(package_list):
            # Score stacking
            score = score_space(volume_space, article_list)
            # Return
            if queue is not None:
                queue.put((score, attempts_counter, volume_space, package_coordinates))
            return score, attempts_counter, volume_space, package_coordinates


def generate_optimizer(
    article_list,
    volume_space,
    generator_sorters=GEN_SORTERS,
    generator_random_lists=RANDOM_LIST_COUNT,
    optimizer_max_attempts=OPT_MAX_ATTEMPTS,
    bias_options=BIAS_STACKS
):
    """
    Main function to run this module.
    First checks if packages can fit at all, then generates various package lists.
    Runs optimizers in parallel on each list.
    Finds lowest achieved score.
    Returns filled volume_space and package coordinates.
    """
    begin_time = time.time()
    # Check if package volume is smaller than or equal to available space, otherwise return error
    if not is_space_sufficient(article_list, volume_space):
        return INSUFFICIENT_SPACE
    #print("Space sufficient")
    # Check if longest package dimension is smaller than or equal to longest space dimension, otherwise return error
    if not is_longest_dimension_sufficient(article_list, volume_space):
        return INSUFFICIENT_DIMENSION
    #print("Dimension sufficient")
    # Generate list of package lists
    package_lists = generate_package_lists(
        article_list, sorters=generator_sorters, random_lists=generator_random_lists
    )
    #print("Package lists generated")
    # Set up threads
    threads = []
    queue = multiprocessing.Queue()
    # Set up an empty list
    return_vals = []
    # Also copy the volume_space once, so that each optimizer thread has a point it can start from again if needed
    empty_space = np.copy(volume_space)
    # Call optimizer function for each package list
    for package_list in package_lists:
        # Set up new threads
        # One for each defined bias in params.py
        for bias in bias_options:
            optimizer_thread = multiprocessing.Process(
                target=optimizer,
                args=(
                    package_list,
                    article_list,
                    np.copy(volume_space),
                    empty_space,
                    queue,
                    optimizer_max_attempts,
                    bias[0],
                    bias[1],
                ),
            )
            # Append to thread list
            threads.append(optimizer_thread)
            # Start thread
            optimizer_thread.start()
    # Receive return values back for each thread
    for thread in threads:
        response = queue.get()
        if response not in ERRORS_OPTIMIZER:
            return_vals.append(response)
    # Find lowest score
    scores = [return_val[0] for return_val in return_vals]
    print(f"Scores: {scores}")
    if len(scores) == 0:
        return OPT_UNSUCCESSFUL
    score_index = scores.index(min(scores))
    print(f"Total optimizer time: {time.time()-begin_time}")
    # Return
    return return_vals[score_index][2:]
