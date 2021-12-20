def add_info_pos_answer(label):
    model_a = ['museum', 'theatre', 'zoo', 'tower', 'monument', 'temple', 'statue', 'palace', 'stadium', 'square', 'fountain', 'park']
    model_b = ['opera', 'theme park', 'market', 'gallery', 'cemetery', 'sculpture', 'skyscraper']
    model_c = ['music']
    model_d = ['event', 'exhibition', 'concert']
    model_e = ['art', 'history', 'architecture', 'science', 'sport']
    model_f = ['modern', 'art nouveau', 'culture']
    model_g = ['painting', 'experiment']
    model_h = ['egypt', 'catalonia', 'gaudí']
    model_i = ['kid']
    model_j = ['animal', 'rollercoaster']
    model_k = ['outdoors']
    model_l = ['mountain']
    model_m = ['activity']
    model_n = ['sea']
    model_o = ['fish']
    model_p = ['church', 'beach']
    model_q = ['archaeology', 'chocolate', 'basketball', 'football']
    model_r = ['ice']
    model_s = ['walk']
    model_t = ['town hall']
    model_u = ['barça']

    if label in model_a:
         return f"We have a couple of good {label}s in Barcelona."

    if label in model_b:
        return f"There's one fine {label} in Barcelona."

    if label in model_c:
        return f"There's some nice places to listen to good {label}."

    if label in model_d:
        return f"There are some installations that hold {label}s in Barcelona."

    if label in model_e:
        return f"I know some good places to enjoy {label} in Barcelona."

    if label in model_f:
        return f"I know some places to enjoy {label} stuff around here."

    if label in model_g:
        return f"There's some nice places to enjoy good {label}s."

    if label in model_h:
        return f"We have some places related to {label.capitalize()} in Barcelona."

    if label in model_i:
        return f"There's plenty of attractions for {label}s around here."

    if label in model_j:
        return f"I know where to find {label}s in Barcelona."

    if label in model_k:
        return f"I know some good places {label}."

    if label in model_l:
        return f"There's plenty of attractions in Barcelona's {label}s."

    if label in model_m:
        return "There's plenty of activities to do in Barcelona."

    if label in model_n:
        return f"We have some places related to the {label} in Barcelona."

    if label in model_o:
        return f"We have some good places to see {label}."

    if label in model_p:
        return f"We have a couple of good {label}es in Barcelona."

    if label in model_q:
        return f"I know a good place to enjoy {label} in Barcelona."

    if label in model_r:
        return f"We have one place related to {label} in Barcelona."

    if label in model_s:
        return f"I know some places to have a {label} over here."

    if label in model_t:
        return f"I know where the {label} is."

    if label in model_u:
        return f"We have one place related to {label.capitalize()}."