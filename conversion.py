"""
example facts:
    1 m = 3.28 ft
    1 ft = 12 in
    1 hr = 60 min
    1 min = 60 sec
example queries:
    2 m = ? in --> answer = 78.72
    13 in = ? m --> answer = 0.330 (roughly)
    13 in = ? hr --> "not convertible!"
"""

def parse_facts(facts):
    facts_dict = {}

    for line in facts.split('\n'):
        l, r = line.split("=")
        l_rate, l_unit = l.strip().split(" ")
        r_rate, r_unit = r.strip().split(" ")

        l_rate = float(l_rate)
        r_rate = float(r_rate)

        if l_unit not in facts_dict:
            facts_dict[l_unit] = [(r_unit, r_rate)]
        else:
            facts_dict[l_unit].append((r_unit, r_rate))
        
        if r_unit not in facts_dict:
            facts_dict[r_unit] = [(l_unit, 1/r_rate)]
        else:
            facts_dict[r_unit].append((l_unit, 1/r_rate))

    return facts_dict


def dfs(facts_dict, curr_unit, goal_unit, rate, visited):
    if curr_unit is None or curr_unit in visited:
        return None

    if curr_unit == goal_unit:
        return rate
    
    visited.add(curr_unit)

    for conversion in facts_dict[curr_unit]:
        new_unit, new_rate = conversion
        
        result = dfs(facts_dict, new_unit, goal_unit, rate*new_rate, visited)

        if result is not None:
            return result
    
    return None


def answer_query(query, facts):
    facts_dict = parse_facts(facts)

    # Parse query
    l_query, r_query = query.split("=")
    l_amount, l_unit = l_query.strip().split(" ")
    r_amount, r_unit = r_query.strip().split(" ")

    visited = set()
    total_conversion = dfs(facts_dict, l_unit, r_unit, 1, visited)
    
    if total_conversion is not None:
        return total_conversion * float(l_amount)
    else:
        return "not convertible!"


if __name__ == "__main__":
    with open("facts.txt") as f:
        facts = f.read()
        query = "15.6 ft = ? mm"
        answer = answer_query(query, facts)
        print(answer)
