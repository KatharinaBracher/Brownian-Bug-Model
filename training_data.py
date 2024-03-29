from trajectory import run_simulation_trajectory

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

def write_training_data(plankton_dict, min_len, outputfile):
    '''extract training data'''
    plankton_ids = get_min_len_ids(min_len,plankton_dict)
    
    training_data = []
    count = 0
    count_total = 0
    file = outputfile+'.npy'
    with open(file, 'wb') as f:
        for i,id1 in enumerate(plankton_ids):
            for id2 in plankton_min[i+1:]:
                traj_intersec = set(plankton_dict[id1]['t']).intersection(set(plankton_dict[id2]['t']))
                if (len(traj_intersec) >= min_len):
                    #print(id1,id2)
                    #print(traj_times[id1], traj_times[id2], traj_intersec)
                    traj_intersec = list(traj_intersec)[:min_len] #cutting longer intersections
                    t1 = traj_intersec[0] 
                    t2 = traj_intersec[-1]
                    a1 = get_coord(id1, t1)
                    a2 = get_coord(id1, t2)
                    b1 = get_coord(id2, t1)
                    b2 = get_coord(id2, t2)
                    training_data.append(np.array((a1,b1,a2,b2)).squeeze())
                    count+=1
                    count_total += 1
                    if count == 3000000: # save in batches that don't kill memory
                        np.save(f, training_data)
                        training_data = []
                        count = 0
        np.save(f, training_data) # save remaining samples

def create_training_data(n,iters, min_len, outputfile):
    L_max = 1 # Size of square domain.
    plankton_dict = run_simulation_trajectory(n, iters, L_max, False)
    write_training_data(plankton_dict, min_len, outputfile)

def load_training_data(file, N=np.inf):
    data = np.empty([1, 4, 2])
    with open(file, 'rb') as f:
        while True:
            try:
                # Load the next array and append it to the list
                loaded_array = np.load(f)
                data = np.vstack((data,loaded_array))
                print('load', loaded_array.shape)
                if data.shape[0]>=N:
                    break
            except EOFError:
                # End of file reached
                break
    if N<np.inf: 
        data = data[:N]
    return data