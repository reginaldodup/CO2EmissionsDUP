def list_to_cols(l, num_cols):
    """
    This function displays a list (l) in num_cols columns
    """
    l = [x if isinstance(x, str) else str(x) for x in l] # make sure only str
    num_lines = len(l) // num_cols + 1  # Number of lines
    max_len = len(max(l, key=len))  # Maximum string len
    result = ""
    for line in range(num_lines):
        for col in range(num_cols):
            l_position = line * num_cols + col
            if l_position < len(l):
                if col < num_cols - 1:
                    result += f"{l_position:03}: {l[l_position]:<30}"
                    # print(f"{l_position:03}: {l[l_position]:<30}", end="")
                else:
                    result += f"{l_position:03}: {l[l_position]:<30}\n"
                    # print(f"{l_position:03}: {l[l_position]:<30}", end="\n")
    return result
