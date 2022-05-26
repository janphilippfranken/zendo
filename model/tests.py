def get_tests(n_tests):
    test_scenes = []
    with open('../data/INSERT_RANDOM_TESTS', 'r') as filehandle:
        filecontents = filehandle.readlines()
        for line in filecontents:
            current_place = line[:-1]
            test_scenes.append(eval(current_place))
    return test_scenes[:n_tests]