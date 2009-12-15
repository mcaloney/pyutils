def permute(items):
    permutations = []
    if len(items) == 1:
        return [items]
    for item in items:
        remainder = items[:]
        remainder.remove(item)
        for permute_rest in permute(remainder):
            permutation = [item]
            permutation.extend(permute_rest)
            permutations.append(permutation)
    return permutations

def permute_string(string):
    items = [char for char in string]
    return (''.join(string) for string in permute(items))

def main():
    for string in permute_string('abcde'): print string

if __name__ == '__main__':
    main()

