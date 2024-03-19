def get_coord(id, t, plankton_dict):
    x = np.array(plankton_dict[id]['x'])[np.array(plankton_dict[id]['t'])==t]
    y = np.array(plankton_dict[id]['y'])[np.array(plankton_dict[id]['t'])==t]
    return [x,y]

def get_min_len_ids(min_len,plankton_dict):
    '''extract plankton IDs with min lenght'''
    traj_len = []
    for id in plankton_dict:
        traj_len.append(len(plankton_dict[id]['t']))
    
    # plankton ids with min trajectory length
    plankton_ids = np.where(np.array(traj_len)>=min_len)[0]
    return plankton_ids

def get_training_data(plankton_dict, min_len):
    '''extract training data'''
    plankton_ids = get_min_len_ids(min_len,plankton_dict)
    
    training_data = []
    
    for i,id1 in enumerate(plankton_min):
        for id2 in plankton_min[i+1:]:
            traj_intersec = set(plankton_dict[id1]['t']).intersection(set(plankton_dict[id2]['t']))
            if (len(traj_intersec) >= min_len):
                #print(id1,id2)
                #print(traj_times[id1], traj_times[id2], traj_intersec)
                traj_intersec = list(traj_intersec)[:min_len] #cutting longer intersections
                t1 = traj_intersec[0] 
                t2 = traj_intersec[-1]
                a1 = get_coord(id1, t1, plankton_dict)
                a2 = get_coord(id1, t2, plankton_dict)
                b1 = get_coord(id2, t1, plankton_dict)
                b2 = get_coord(id2, t2, plankton_dict)
                training_data.append((np.array((a1,b1,a2,b2)).squeeze()))
    return training_data