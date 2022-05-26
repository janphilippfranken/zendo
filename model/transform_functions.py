import math
# hard-coded functions restructuring zendo data

def compute_orientation(rot, epsilon = math.pi/6):
    orientations = []
    while rot > 2 * math.pi:
          rot = rot -2*math.pi
    while rot < 0:
          rot = rot+2*math.pi
    if abs(rot - math.pi) < epsilon:
         orientations.append('upright')
    elif abs(rot-1.2475) < epsilon:
        orientations.append('lhs')
    elif abs(rot-5.0375) < epsilon:
          orientations.append('rhs')
    else:
          orientations.append('strange')
    return orientations

def compute_contact(contact):
    contact_corrected = []
    for key in contact.keys():
        cone = key[1]
        if isinstance(contact[key], int):
            contact_corrected.append(int(cone) - 1)
        elif isinstance(contact[key], list):
            contact_corrected.append(contact[key])
    return contact_corrected

def check_structure(contact, i):
    if isinstance(contact[0], dict):
        key = list(contact[0].keys())[i]
        contact = compute_contact({key: contact[0][key]})
        contact = contact[0]
    elif isinstance(contact, list):
        contact = contact[i]
        if isinstance(contact, int):
               contact = [contact]
    if (isinstance(contact,int)):
        contact = [contact]
    return contact

def check_feat_change_both_directions(features, follow, magnitude=1):
    val_set = set([val for sublist in features for val in sublist])
    val_score_dict = {el:0 for el in val_set}
    ind_next = 0
    change_sum = []
    for i in features:
        change = []
        ind_next += 1
        if ind_next == len(features):
            ind_next = 0
        if set(i) == set(features[ind_next]) and len(i) == len(features[ind_next]):
            change.append(0)
        else:
            change.append(1)
            set_init = set(i).difference(set(features[ind_next]))
            set_next = set(features[ind_next]).difference(set(i))
            if follow[features.index(i)] == True and follow[ind_next] == False:
                for value in set_init:
                    val_score_dict[value] += 1 * magnitude
                for value in set_next:
                    val_score_dict[value] += 1 * magnitude
            if follow[ind_next]== True and follow[features.index(i)]== False:
                for value in set_next:
                    val_score_dict[value] += 1 * magnitude
                for value in set_init:
                    val_score_dict[value] += 1 * magnitude
        if sum(change) == 0:
            change_sum.append(False)
        else:
            change_sum.append(True)
    return {'feat_change': change_sum, 'val_change': val_score_dict, 'sum_values': sum(val_score_dict.values())}

def check_feat_change_single_comparison_both_directions(features,follow):
    set_follow = []
    set_no_follow = []
    val_set = set([val for sublist in features for val in sublist])
    val_score_dict = {el:0 for el in val_set}
    for feature in features:
        if follow[features.index(feature)] == True:
            set_follow.append(feature)
        elif follow[features.index(feature)] == False:
            set_no_follow.append(feature)
    set_follow = [val for sublist in set_follow for val in sublist]
    set_no_follow = [val for sublist in set_no_follow for val in sublist]
    set_follow = set(set_follow).difference(set(set_no_follow))
    set_no_follow = set(set_no_follow).difference(set(set_follow))
    for value in set_follow:
        val_score_dict[value] += 1
    for value in set_no_follow:
        val_score_dict[value] += 1
    return {'val_change': val_score_dict, 'sum_values': sum(val_score_dict.values())}

def check_feat_change_single_comparison_presence(features, follow):
    set_follow = []
    set_no_follow = []
    val_set = set([val for sublist in features for val in sublist])
    val_score_dict = {el:0 for el in val_set}
    for feature in features:
        if follow[features.index(feature)] == True:
            set_follow.append(feature)
        elif follow[features.index(feature)] == False:
            set_no_follow.append(feature)
    set_follow = [val for sublist in set_follow for val in sublist]
    set_no_follow = [val for sublist in set_no_follow for val in sublist]
    set_follow = set(set_follow).difference(set(set_no_follow))
    set_no_follow = set(set_no_follow).difference(set(set_follow))
    for value in set_follow:
        val_score_dict[value] += 1
    return {'val_change': val_score_dict, 'sum_values': sum(val_score_dict.values())}

def check_feat_change_single_comparison_absence(features,follow):
    set_follow = []
    set_no_follow = []
    val_set = set([val for sublist in features for val in sublist])
    val_score_dict = {el:0 for el in val_set}
    for feature in features:
        if follow[features.index(feature)] == True:
            set_follow.append(feature)
        elif follow[features.index(feature)] == False:
            set_no_follow.append(feature)
    set_follow = [val for sublist in set_follow for val in sublist]
    set_no_follow = [val for sublist in set_no_follow for val in sublist]
    set_follow = set(set_follow).difference(set(set_no_follow))
    set_no_follow = set(set_no_follow).difference(set(set_follow))
    for value in set_no_follow:
        val_score_dict[value] += 1
    return {'val_change': val_score_dict, 'sum_values': sum(val_score_dict.values())}

def check_feat_change_presence(features,follow,default='set'):
    val_set = set([val for sublist in features for val in sublist])
    val_score_dict = {el:0 for el in val_set}
    ind_next = 0
    yes = 0
    no = 0
    change_sum = []
    for i in features:
        change = []
        ind_next += 1
        if ind_next == len(features):
            ind_next = 0
        if default == 'set':
            if set(i) == set(features[ind_next]) and len(i) == len(features[ind_next]):
                change.append(0)
            else:
                change.append(1)
                set_init = set(i).difference(set(features[ind_next]))
                set_next = set(features[ind_next]).difference(set(i))
                if follow[features.index(i)] == True and follow[ind_next] == False:
                    for value in set_init:
                        val_score_dict[value] += 1
                        yes +=1
                if follow[ind_next]== True and follow[features.index(i)]== False:
                    for value in set_next:
                        val_score_dict[value] += 1
                        yes +=1
        if sum(change) == 0:
            change_sum.append(False)
        else:
            change_sum.append(True)
    return {'feat_change': change_sum, 'val_change': val_score_dict, 'sum_values': sum(val_score_dict.values())}

def check_feat_change_absence(features,follow,default='set'):
    val_set = set([val for sublist in features for val in sublist])
    val_score_dict = {el:0 for el in val_set}
    ind_next = 0
    yes = 0
    no = 0
    change_sum = []
    for i in features:
        change = []
        ind_next += 1
        if ind_next == len(features):
            ind_next = 0
        if default == 'set':
            if set(i) == set(features[ind_next]) and len(i) == len(features[ind_next]):
                change.append(0)
            else:
                change.append(1)
                set_init = set(i).difference(set(features[ind_next]))
                set_next = set(features[ind_next]).difference(set(i))
                if follow[features.index(i)] == True and follow[ind_next] == False:
                    for value in set_next:
                        val_score_dict[value] += 1
                        no +=1
                if follow[ind_next]== True and follow[features.index(i)]== False:
                    for value in set_init:
                        val_score_dict[value] += 1
                        no +=1
        if sum(change) == 0:
            change_sum.append(False)
        else:
            change_sum.append(True)
    return {'feat_change': change_sum, 'val_change': val_score_dict, 'sum_values': sum(val_score_dict.values())}


def get_production_probs_seq(data, type, magnitude=1,truth=None, cond=None):
    grounded = []
    colours = []
    sizes = []
    orientations = []
    follows = []
    scene_count = 0
    for trial in data:
        if scene_count < 8 or cond=='3':
            colours.append(trial['colours'])
            sizes.append(trial['sizes'])
            grounded.append(trial['grounded'])
            follows.append(trial['follow_rule'])
            orientations.append(trial['orientations'])
        elif scene_count >= 8 and scene_count < 16:
            colours.append(trial['colours'])
            sizes.append(trial['sizes'])
            grounded.append(trial['grounded'])
            orientations.append([compute_orientation(i)[0] for i in trial['rotations']])
            follows.append(truth[data.index(trial) - 8])
        elif scene_count > 16:
            colours.append(trial['colours'])
            sizes.append(trial['sizes'])
            grounded.append(trial['grounded'])
            follows.append(trial['follow_rule'])
            orientations.append([compute_orientation(i)[0] for i in trial['rotations']])
        scene_count+=1
    feat_scores = [check_feat_change_both_directions(colours,follows,magnitude)['sum_values'],
                   check_feat_change_both_directions(sizes,follows,magnitude)['sum_values'],
                   check_feat_change_both_directions(orientations,follows,magnitude)['sum_values'],
                   check_feat_change_both_directions(grounded,follows,magnitude)['sum_values']]
    val_scores = [check_feat_change_both_directions(colours,follows,magnitude)['val_change'],
                  check_feat_change_both_directions(sizes,follows,magnitude)['val_change'],
                  check_feat_change_both_directions(orientations,follows,magnitude)['val_change'],
                  check_feat_change_both_directions(grounded,follows,magnitude)['val_change']]
    val_defaults = [{'red':1,'blue':1,'green':1},
                   {'1':1,'2':1,'3':1},
                   {'upright':1, 'lhs':1, 'rhs':1, 'strange':1},
                   {'no':1,'yes':1}]
    for val_score in val_scores:
        for key in val_score.keys():
            val_defaults[val_scores.index(val_score)][str(key)] += val_score[key]
    color_probs = list(val_defaults[0].values())
    color_probs = [float(zzz)/sum(color_probs) for zzz in color_probs]
    size_probs = list(val_defaults[1].values())
    size_probs = [float(zzz)/sum(size_probs) for zzz in size_probs]
    orientation_probs= list(val_defaults[2].values())
    orientation_probs = [float(zzz)/sum(orientation_probs) for zzz in orientation_probs]
    grounded_probs = list(val_defaults[3].values())
    grounded_probs = [float(zzz)/sum(grounded_probs) for zzz in grounded_probs]
    feat_probs = [color_probs,size_probs,orientation_probs,grounded_probs]
    Dwin= [(1+feat_scores[0]),
           (1+feat_scores[1]),
           (1+feat_scores[2]),
           (1+feat_scores[3])]
    Dwin = [float(raw)/sum(Dwin) for raw in Dwin]
    return [Dwin, feat_probs]

def get_production_probs_prototype(data, type, magnitude=1, truth=None, cond=None, feat_only = True):
    prot_follow = {'colours': {'red': 0, 'blue': 0, 'green': 0},
                   'sizes': {'1':0,'2':0,'3':0},
                   'orientations': {'upright': 0, 'lhs': 0, 'rhs': 0, 'strange': 0},
                   'grounded': {'yes': 0, 'no': 0}}
    prot_n_follow = {'colours': {'red': 0, 'blue': 0, 'green': 0},
                   'sizes': {'1':0,'2':0,'3':0},
                   'orientations': {'upright': 0, 'lhs': 0, 'rhs': 0, 'strange': 0},
                   'grounded': {'yes': 0, 'no': 0}}
    scene_count = 0
    count_follow = 0
    count_n_follow = 0
    for trial in data:
        if scene_count < 8 or cond!='3':
            if trial['follow_rule'] == True:
                for feat in trial:
                    if feat in prot_follow:
                        for val in trial[feat]:
                            prot_follow[feat][str(val)] += 1
                count_follow +=1
            if trial['follow_rule'] == False:
                for feat in trial:
                    if feat in prot_follow:
                        for val in trial[feat]:
                            prot_n_follow[feat][str(val)] += 1
                count_n_follow +=1
        elif scene_count >= 8 and cond=='3':
            if truth[data.index(trial) - 8] == True:
                for feat in trial:
                    if feat in prot_follow:
                        for val in trial[feat]:
                            prot_follow[feat][str(val)] += 1
                count_follow +=1
            if truth[data.index(trial) - 8] == False:
                for feat in trial:
                    if feat in prot_follow:
                        for val in trial[feat]:
                            prot_n_follow[feat][str(val)] += 1
                count_n_follow +=1
        scene_count+=1
    diff_dict = {}
    diff_dict_2 = {}
    count_follow = max(count_follow, 1)
    count_n_follow = max(count_n_follow,1)
    for feat in prot_follow.keys():
        diff_dict[feat] = {key: prot_follow[feat][key]/count_follow - prot_n_follow[feat][key]/count_n_follow     for key in prot_follow[feat]}
        for val in prot_follow[feat]:
            if prot_follow[feat][val] == 0:
                diff_dict[feat][val] = diff_dict[feat][val] * -1
            max_min = (max(diff_dict[feat].values()) - min(diff_dict[feat].values()))
            if max_min == float(0):
                max_min=1
            diff_dict[feat][val] = (diff_dict[feat][val]  - min(diff_dict[feat].values())) / max_min
            diff_dict[feat][val] += float(1/3)
        raw_probs = list(diff_dict[feat].values())
        norm_probs = [float(raw)/sum(raw_probs) for raw in raw_probs]
        diff_dict_2[feat] = norm_probs
    feat_probs = []
    for val in list(diff_dict_2.values()):
        feat_probs.append(val)
    Dwin = [.25,.25,.25,.25]
    if feat_only == False:
        Dwin[0] += max(feat_probs[0]) - min(feat_probs[0])
        Dwin[1] += max(feat_probs[1]) - min(feat_probs[1])
        Dwin[2] += max(feat_probs[2]) - min(feat_probs[2])
        Dwin[3] += max(feat_probs[3]) - min(feat_probs[3])
    Dwin = [float(raw)/sum(Dwin) for raw in Dwin]
    return [Dwin, feat_probs]














